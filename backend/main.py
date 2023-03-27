# -*- coding: utf-8 -*-
"""
api.ipynb
"""

#pip install flask-restx

from flask import Flask, jsonify, request, make_response
from sqlalchemy import create_engine, text
from flask_restx import Api, Namespace, Resource
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

#Database credentials
user = "root"
passw = "food45"
host = '34.175.117.30'
database = "main"

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = host

api = Api(app, version = '1.0',
    title = 'API for Streamlit Dashboard',
    description = """
        This REST API is an API to built with FLASK
        and FLASK-RESTX libraries. This API serves a 
        frontend Streamlit dashboard
        """,
    contact = "jguss45@gmail.com",
    endpoint = "/api/v1"
)

#function to connect to DB
def connect():
    db = create_engine(
    'mysql+pymysql://{0}:{1}@{2}/{3}' \
        .format(user, passw, host, database), \
    connect_args = {'connect_timeout': 10})
    conn = db.connect()
    return conn

#function to disconnect from DB
def disconnect(conn):
    conn.close()

#################################

#Authentication ENDPOINTS


users = Namespace('users',
    description = 'All operations related to users, notably authentication',
    path='/api/v1')
api.add_namespace(users)

@users.route("/users")
@users.doc("This route is for development use, is not used in the app")
class view_users(Resource):
    def get(self):
        conn = connect()
        select = text(f"""
            SELECT * FROM users""")
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

@users.route("/users/login")
class handle_login(Resource):
    def get(self):
        #receive user login input
        username = request.json.get('username')
        password = request.json.get('password')

        #validate login details against database
        try:
            conn = connect()
            select = text(f"""
                SELECT * FROM users
                WHERE username = :username""")
            result = conn.execute(select, username=username)
            user = result.fetchone()
            disconnect(conn)

            if user and check_password_hash(user.password, password):
                # Generate JWT token and send it as part of the response
                token = jwt.encode({'username': username}, "please-dont-hack-me", algorithm='HS256')
                response = make_response(token, 200)
            else:
                response = make_response(jsonify({'message': 'Unable to login. Please ensure your credentials are correct or register a new account.'}), 401)
        except Exception as e:
            response = make_response(e, 500)
        return response
@users.route("/users/register", methods=["POST"])
class handle_register(Resource):
    def post(self):
        #receive user registration input
        username = request.json.get('username')
        password = request.json.get('password')

        hashed_password = generate_password_hash(password)
        try:
            # Check if the username already exists in the database
            conn = connect()
            select_query = text("""
                SELECT * FROM users WHERE username = :username;
            """)
            result = conn.execute(select_query, username=username)
            existing_user = result.fetchone()

            # If the username already exists, return an error
            if existing_user:
                response = make_response(jsonify({'message': 'Username already exists. Please create a new username or login with your existing credentials.'}), 400)
                conn.close()
                return response
            #if username doesn't exist, proceed with generating new user
            insert_query = text("""
                INSERT INTO users (username, password)
                VALUES (:username, :password);""")
            result = conn.execute(insert_query, username=username, password=hashed_password)

            #validate db insert worked 
            if result.rowcount > 0:
            # Generate JWT token and send it as part of the response
                token = jwt.encode({'username': username}, "please-dont-hack-me", algorithm='HS256')
                response = make_response(token, 200)
            else:
                response = make_response(jsonify({'message': 'Unable to create user account. You may already have an account created.'}), 401)
        except Exception as e:
            response = make_response(e, 500)
        return response

#CUSTOMERS ENDPOINTS
customers = Namespace('customers',
    description = 'All operations related to customers',
    path='/api/v1')
api.add_namespace(customers)

@customers.route("/customers/gender")
@customers.doc("To query customers by gender")
class get_cust_genders(Resource):

    def get(self):
        conn = connect()
        select = text("""
            SELECT DISTINCT(UPPER(GENDER)) AS gender
            FROM customer
            ORDER BY gender DESC;""")
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

@customers.route("/customers/age")
@customers.doc("To query customers by age")
class get_cust_age(Resource):

    def get(self):
        conn = connect()
        select = text("""
            SELECT DISTINCT AGE AS age
            FROM customer
            ORDER BY age DESC;""")
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})
    
@customers.route("/customers/filter")
@customers.doc("To filter customers by gender and age range")
class filter_customers(Resource):
    def get(self):
        gender_filtered_lst = request.args.getlist('gender_filtered_lst')
        age_filtered_lst = request.args.getlist('age_filtered_lst')
        
        gender_filtered_str = ', '.join(
            "'{}'".format(gender) for gender in gender_filtered_lst)
        if len(gender_filtered_str) == 0:
            gender_filtered_str = "LIKE '%%'"
        else:
            gender_filtered_str = "IN (" + gender_filtered_str + ")"
            
        conn = connect()
        select = text("""
            SELECT *
            FROM customer
            WHERE UPPER(GENDER) {0}
                AND AGE BETWEEN {1} AND {2}
            LIMIT 1000;""".format(
                gender_filtered_str, 
                age_filtered_lst[0],
                age_filtered_lst[1]))
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})
    
#SUBSCRIPTIONS ENDPOINTS
subscriptions = Namespace('subscriptions',
    description = 'All operations related to subscriptions',
    path='/api/v1')
api.add_namespace(subscriptions)

@subscriptions.route("/subscriptions")
@subscriptions.doc("To query subscriptions")
class get_subscriptions(Resource):

    def get(self):
        conn = connect()
        select = text("""
            SELECT *
            FROM subscription
            ORDER BY signup_date_time DESC
            LIMIT 5000;""")
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

#PRODUCTS ENDPOINTS    
products = Namespace('products',
    description = 'All operations related to products',
    path='/api/v1')
api.add_namespace(products)

@products.route("/products")
class get_all_products(Resource):
    def get(self):
        conn = connect()
        select = text("""
            SELECT *
            FROM product;""")
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

@products.route("/products/<string:id>")
@products.doc(params = {'id': 'The ID of the product'})
class select_product(Resource):

    @api.response(404, "Product not found")
    def get(self, id):
        id = str(id)
        conn = connect()
        select = text(f"""
            SELECT *
            FROM product
            WHERE product_id = '{id}';""")
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

#Revenue ENDPOINTS    
revenue = Namespace('revenue',
    description = 'All operations related to revenue',
    path='/api/v1')
api.add_namespace(revenue)

@revenue.route("/revenue")
class get_all_revenue(Resource):
    def get(self):
        conn = connect()
        select = text("""
            SELECT *
            FROM income;""")
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})


if __name__ == '__main__':
    app.run(debug = True)