import streamlit as st
import requests
import jwt
from dashboard import display_dashboard

#Backend API URL
base_url = 'http://127.0.0.1:5000/api/v1'

#Streamlit app title
st.set_page_config(page_title="H&M KPI Dashboard")

#Defining function to authenticate user
def login():
    st.header("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        payload = {"username": username, "password": password}
        response = requests.get(base_url+'/users/login', json=payload)

        if response.status_code == 200:
            data = response.json()
            token = data["access_token"]
            st.session_state.token = token
            st.success("Logged in successfully!")
            return st.session_state.token
        else:
            st.error("Invalid credentials.")

def register():
    st.header("Register")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        payload = {"username": username, "password": password}
        response = requests.post(base_url+'/users/register', json=payload)

        if response.status_code == 200:
            token = response.content
            st.session_state.token = token
            st.success("Logged in successfully!")
            return st.session_state.token
        else:
            st.error("Invalid credentials.")

def present_dashboard(token):
    display_dashboard(token)

def login_or_register():
    #prompt login or register
    auth_choice = st.radio("Select an option", ("Login", "Register"))

    #show form
    if auth_choice == "Login":
            token = login()
    else:
        token = register()
    
    # If the user has a valid JWT token, show the restricted content
    if token:
        try:
            display_dashboard(token)
            st.experimental_rerun()
        except jwt.exceptions.InvalidSignatureError:
            st.write("Invalid token")

def main():
    
    image_url = "https://upload.wikimedia.org/wikipedia/commons/5/53/H%26M-Logo.svg"
    st.image(image_url, width=200)
    st.title("KPI Dashboard")

    if "token" not in st.session_state:
        login_or_register()


if __name__ == "__main__":
    main()