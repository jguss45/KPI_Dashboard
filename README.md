# H&M KPIs Project

### Project Overview
This project consists of a backend REST API, a frontend Streamlit dashboard, and a SQL database hosted on Google Cloud.

## API for Streamlit Dashboard

This is a REST API that is built with the Flask and Flask-RESTX libraries. The API serves a frontend Streamlit dashboard.

### Authentication Endpoints
The following endpoints are used for authentication.

/users
-This route is for development use only and is not used in the app.

/users/login
-This endpoint handles user login. It receives the user login input and validates the login details against the database. If the login details are valid, it generates a JSON Web Token (JWT) and sends it as part of the response. The JWT is used to authenticate subsequent requests.

/users/register
-This endpoint handles user registration. It receives the user registration input and checks if the username already exists in the database. If the username already exists, it returns an error. If the username doesn't exist, it proceeds with generating a new user. If the database insert is successful, it generates a JWT and sends it as part of the response.

### Customers Endpoints
-The following endpoints are used for querying customers.

/customers/gender
-This endpoint is used to query customers by gender. It returns a list of distinct genders sorted in descending order.

/customers/filter
-This endpoint is used to filter customers by gender and age range. It receives the gender and age range as query parameters and returns a filtered list of customers. If no gender or age range is specified, it returns all customers.

## Streamlit Application
### main.py

Login() function:
Allows users to login by providing username and password. If user enters valid login credentials and clicks login, function sends a GET request to the backend API to authenticate the user. If user user is authenticated, function stores the JWT token in session state and displays success message. If authentication fails, error message is displayed.

Register() function:
Allows new users to register by providing username and password. If user registers valid details and clicks Register, function sends POST request to backend API to create a new user account. If account is successfully created, function stores the JWT token in session state and displays success image. If registration fails, error message is displayed.

login_or_register():
Displays radio button allowing users to select whether they want to login or register. Depending on the user's selection, the appropriate function is called to handle the login or registration process.

present_dashboard():
Displays the contents of the dashboard.py file. This is where all of the KPIs are presented.

main():
Main entrypoint of the Streamlit app. Displays logo and dashboard title. If user is not authenticated with a token, the login_or_register function is called. If user is authenticated with token then display_dashboard() is called to show the dashboard to the user.

### dashboard.py
display_Dashboard(token):
Function which contains entirety of code for H&M KPIs

## Link to deployed website:
https://frontend-dot-capstoneproject-376415.oa.r.appspot.com
***Link no longer active as I shutdown my Google SQL Database and App Engine services due to Gcloud credit constraints 
