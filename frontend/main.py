import streamlit as st
import requests
import jwt
from dashboard import display_dashboard

#Backend API URL
#if these links are no longer hosted, you can launch both main.py files locally and replace with localhost
base_url = 'https://backend-dot-capstoneproject-376415.oa.r.appspot.com/api/v1'

#Frontend URL
frontend_url = 'https://frontend-dot-capstoneproject-376415.oa.r.appspot.com/'

#Streamlit app title
st.set_page_config(page_title="H&M KPI Dashboard")

#Defining function to handle user login
def login():
    st.header("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        payload = {"username": username, "password": password}
        response = requests.post(base_url+'/users/login', json=payload)

        if response.status_code == 200:
            token = response.content
            st.session_state["token"] = token
            st.success("Logged in successfully!")
            return st.session_state.token
        elif response.status_code == 500:
            st.error(response.content)
        else:
            st.error(response.json()['message'])

#function to handle registering new users
def register():
    st.header("Register")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        payload = {"username": username, "password": password}
        response = requests.post(base_url+'/users/register', json=payload)

        if response.status_code == 200:
            token = response.content
            st.session_state["token"] = token
            st.success("Logged in successfully!")
            return st.session_state.token
        elif response.status_code == 500:
            st.error(response.content)
        else:
            st.error(response.json()['message'])


#function to display streanlit dashboard data
def present_dashboard(token):
    display_dashboard(token)

#function to handle taking user input to either login or register
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
            st.experimental_rerun()
        except jwt.exceptions.InvalidSignatureError:
            st.write("Invalid token")

#main function. access to dashboard only granted if user is authenticated with a token
def main():
    
    image_url = "https://upload.wikimedia.org/wikipedia/commons/5/53/H%26M-Logo.svg"
    st.image(image_url, width=200)
    st.title("KPI Dashboard")

    if "token" not in st.session_state:
        login_or_register()
    if "token" in st.session_state:
        display_dashboard(st.session_state.token)


if __name__ == "__main__":
    main()