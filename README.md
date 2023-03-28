# H&M KPIs Project

### Project Overview
This project consists of a backend REST API, a frontend Streamlit dashboard, and a SQL database hosted on Google Cloud.

## API for Streamlit Dashboard

This is a REST API that is built with the Flask and Flask-RESTX libraries. The API serves a frontend Streamlit dashboard.

Authentication Endpoints

The following endpoints are used for authentication.

/users
This route is for development use only and is not used in the app.

/users/login
This endpoint handles user login. It receives the user login input and validates the login details against the database. If the login details are valid, it generates a JSON Web Token (JWT) and sends it as part of the response. The JWT is used to authenticate subsequent requests.

/users/register
This endpoint handles user registration. It receives the user registration input and checks if the username already exists in the database. If the username already exists, it returns an error. If the username doesn't exist, it proceeds with generating a new user. If the database insert is successful, it generates a JWT and sends it as part of the response.

Customers Endpoints
The following endpoints are used for querying customers.

/customers/gender
This endpoint is used to query customers by gender. It returns a list of distinct genders sorted in descending order.

/customers/filter
This endpoint is used to filter customers by gender and age range. It receives the gender and age range as query parameters and returns a filtered list of customers. If no gender or age range is specified, it returns all customers.
