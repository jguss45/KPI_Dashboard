import pandas as pd
import numpy as np
import streamlit as st
import datetime
import requests
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import jwt

#JWT Secret Key
SECRET_KEY = "please-dont-hack-me"

#Backend API URL
base_url = 'http://127.0.0.1:5000/api/v1'


def display_dashboard(token):
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        
    #Dashboard Header    
    st.write("Welcome ", decoded_token["username"], ". Hope you find these insights useful!")
    st.write("The goal of this report is provide our company with better insight into how our products are performing in the market, and better understand who our customers are.")


    #Fetch Gender data
    #note: I could definitely hard code genders here to improve performance, but will opt not to
    gender_endpoint = f'{base_url}/customers/gender'
    response = requests.get(gender_endpoint)
    gender_lst = pd.DataFrame(response.json()['result'])['gender'].to_list()

    #Sidebar with filters
    st.sidebar.write("FILTERS")

    gender_filtered_lst = st.sidebar.multiselect(
        label = "GENDER",
        options = gender_lst,
        default = gender_lst,
        key = "multiselect_genders"
    )    
    selected_genders = ', '.join(gender_filtered_lst)

    age_filtered_lst = st.sidebar.slider(
        'Select a range of ages',
        0, 100, (20, 80))

    st.sidebar.write('Showing results for the following chosen filters:')
    st.sidebar.write('Genders: ', selected_genders)
    st.sidebar.write('Age range:', age_filtered_lst)

    #Fetch data for gender and age given chosen filters
    filter_endpoint = f'{base_url}/customers/filter'
    response = requests.get(filter_endpoint, 
                            params={'gender_filtered_lst': gender_filtered_lst,
                                    'age_filtered_lst': age_filtered_lst})

    customer_df = pd.DataFrame(response.json()['result'])

    #working with subscription data
    subscriptions_endpoint = f'{base_url}/subscriptions'
    response = requests.get(subscriptions_endpoint)
    subscription_df = pd.DataFrame(response.json()['result'])
    #convert dates to datetime 
    subscription_df["signup_date_time"] = pd.to_datetime(subscription_df["signup_date_time"])
    subscription_df["cancel_date_time"] = pd.to_datetime(subscription_df["cancel_date_time"])

    last_day_dt = datetime.datetime(year = 2021, month = 12, day = 31)

    #total number of subs per product
    product1_sum = (subscription_df["product"] == "prd_1").sum()
    product2_sum = (subscription_df["product"] == "prd_2").sum()
    total_product_subscriptions = product1_sum + product2_sum

    #subscriptions for each product as a percent
    product1_subs_as_percent = str(round(product1_sum / total_product_subscriptions * 100)) + "%"
    product2_subs_as_percent = str(round(product2_sum / total_product_subscriptions * 100)) + "%"

    #total number of cancellations per product
    product1_cancellations_sum = subscription_df[(subscription_df['cancel_date_time'].notnull()) & (subscription_df['product'] == 'prd_1')].shape[0]
    product2_cancellations_sum = subscription_df[(subscription_df['cancel_date_time'].notnull()) & (subscription_df['product'] == 'prd_2')].shape[0]

    #cancellations for each product as a percent 
    product1_cancellations_as_percent = str(round(product1_cancellations_sum / product1_sum * 100)) + "%"
    product2_cancellations_as_percent = str(round(product2_cancellations_sum / product2_sum * 100)) + "%"

    #total subscriptions and cancellations overall
        #ended up determining these kpis to not really be significant 
    #total_product_cancellations = (subscription_df['cancel_date_time'].notnull()).sum()
    #total_product_cancellations_as_percent = str(round(total_product_cancellations / total_product_subscriptions * 100)) + "%"

    #displaying subscription and cancellation data
    st.header("Subscriptions and Cancellations")

    sub_kpi1, sub_kpi2 = st.columns(2)

    sub_kpi1.metric(
        label = "Total Product 1 Subscriptions",
        value = product1_sum,
    )

    sub_kpi2.metric(
        label = "Total Product 2 Subscriptions",
        value = product2_sum,
    )

    sub_kpi1, sub_kpi2 = st.columns(2)

    sub_kpi1.metric(
        label = "Product 1 Subscriptions (%)",
        value = product1_subs_as_percent,
    )

    sub_kpi2.metric(
        label = "Product 2 Subscriptions (%)",
        value = product2_subs_as_percent,
    )

    #creating bar chart for subscriptions
    subscription_dict = {'Product': ['Product 1', 'Product 2'],
                        'Total Subscriptions': [product1_sum, product2_sum]
                        }
    sub_bar_chart_df = pd.DataFrame(subscription_dict).set_index('Product')
    st.subheader('Comparing Product Subscriptions')
    st.bar_chart(sub_bar_chart_df)

    #display cancellation kpis
    sub_kpi1, sub_kpi2 = st.columns(2)

    sub_kpi1.metric(
        label="Total Product 1 Cancellations",
        value=product1_cancellations_sum,
    )

    sub_kpi2.metric(
        label="Total Product 2 Cancellations",
        value=product2_cancellations_sum,
    )

    sub_kpi1, sub_kpi2 = st.columns(2)

    sub_kpi1.metric(
        label="Product 1 Subscriptions Cancelled (%)",
        value= product1_cancellations_as_percent
    )

    sub_kpi2.metric(
        label = "Product 2 Subscriptions Cancelled (%)",
        value = product2_cancellations_as_percent,
    )

    #creating bar chart for cancellations
    cancellation_dict = {'Product': ['Product 1', 'Product 2'],
                        'Total Cancellations': [product1_cancellations_sum, product2_cancellations_sum]
                        }
    cancel_bar_chart_df = pd.DataFrame(cancellation_dict).set_index('Product')


    st.subheader('Comparing Product Cancellations')
    st.bar_chart(cancel_bar_chart_df)

    #average amount of time subscribed before cancellation
    subscription_df['cancel_date_time'] = subscription_df['cancel_date_time'].fillna(last_day_dt)
    subscription_df["cancel_date_time"] = pd.to_datetime(subscription_df["cancel_date_time"], utc=True)

    subscription_df['diff'] = subscription_df['cancel_date_time'] - subscription_df['signup_date_time']
    subscription_df['diff_days'] = subscription_df['diff'].dt.days.astype(int)
    avg_cancel_days = subscription_df['diff_days'].mean().round()
    prd1_avg_cancel_days = subscription_df.loc[subscription_df['product'] == 'prd_1', 'diff_days'].mean().round()
    prd2_avg_cancel_days = subscription_df.loc[subscription_df['product'] == 'prd_2', 'diff_days'].mean().round()
    subscription_df[["product", "diff_days"]] \
        .groupby(['product']).mean()

    #display avg sub days kpis
    sub_kpi1, sub_kpi2, sub_kpi3 = st.columns(3)

    sub_kpi1.metric(
        label = "Avg sub days Product 1",
        value = round(prd1_avg_cancel_days),
    )

    sub_kpi2.metric(
        label = "Avg sub days Product 2",
        value = round(prd2_avg_cancel_days),
    )

    sub_kpi3.metric(
        label = "Avg sub days all products",
        value = round(avg_cancel_days),
    )

    sub_days_dict = {'Product': ['Product 1', 'Product 2'],
                        'Average Days Subscribed': [prd1_avg_cancel_days, prd2_avg_cancel_days]
                        }
    sub_days_bar_chart_df = pd.DataFrame(sub_days_dict).set_index('Product')
    st.subheader('Comparing Average Days Until Cancellation')
    st.bar_chart(sub_days_bar_chart_df)

    num_customers = len(customer_df["customer_id"])#.nunique()
    avg_age = np.mean(customer_df["age"])
    num_genders = customer_df["gender"].nunique()

    st.header("Analyzing Age Distribution from Sample of Customers")
    st.text("*Note: Use side bar to filter data by gender and age range")
    kpi1, kpi2, kpi3 = st.columns(3)

    #display filtered list kpis
    kpi1.metric(
        label = "Customer sample size",
        value = num_customers,
        delta = num_customers,
    )

    kpi2.metric(
        label = "Number of different genders",
        value = num_genders,
        delta = num_genders,
    )
            
    kpi3.metric(
        label = "Average age",
        value = round(avg_age),
        delta = -10 + avg_age,
    )

    st.bar_chart(customer_df.groupby(["age"])["customer_id"].count())

    #Working with Revenue
    revenue_endpoint = f'{base_url}/revenue'
    response = requests.get(revenue_endpoint)
    revenue_df = pd.DataFrame(response.json()['result'])

    product1_revenues = {}
    product2_revenues = {}

    #creating variables to store revenue for each year by product
    for index, row in revenue_df.iterrows():
        if row["name"] == "annual_subscription":
            var_name = f"annual_income_{row['year']}"
            product1_revenues[var_name] = row["price"]
        
        elif row["name"] == "monthly_subscription":
            var_name = f"monthly_income_{row['year']}"
            product2_revenues[var_name] = row["price"]

    st.header("Analyzing Historical Revenues by Product")

    st.subheader("Product 1 Annual Revenues (in thousands)")

    #display revenue kpis
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

    kpi1.metric(
        label = "2017",
        value = round(product1_revenues['annual_income_2017'] / 1000),
    )

    kpi2.metric(
        label = "2018",
        value = round(product1_revenues['annual_income_2018'] / 1000),
    )
            
    kpi3.metric(
        label = "2019",
        value = round(product1_revenues['annual_income_2019'] / 1000),
    )

    kpi4.metric(
        label = "2020",
        value = round(product1_revenues['annual_income_2020'] / 1000),
    )
            
    kpi5.metric(
        label = "2021",
        value = round(product1_revenues['annual_income_2021'] / 1000),
    )

    st.subheader("Product 2 Annual Revenues (in thousands)")

    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

    kpi1.metric(
        label = "2017",
        value = round(product2_revenues['monthly_income_2017'] / 1000),
    )

    kpi2.metric(
        label = "2018",
        value = round(product2_revenues['monthly_income_2018'] / 1000),
    )
            
    kpi3.metric(
        label = "2019",
        value = round(product2_revenues['monthly_income_2019'] / 1000),
    )

    kpi4.metric(
        label = "2020",
        value = round(product2_revenues['monthly_income_2020'] / 1000),
    )
            
    kpi5.metric(
        label = "2021",
        value = round(product2_revenues['monthly_income_2021'] / 1000),
    )

    def y_axis_formatter(value, _):
        return f"${value:,.0f}"
    # Create a line chart for the annual revenue of product 1
    st.subheader('Annual Revenue of Product 1')
    fig1, ax1 = plt.subplots()
    ax1.plot(product1_revenues.keys(), product1_revenues.values(), marker='o')
    ax1.set_xlabel('Year')
    ax1.set_xticklabels(['2017', '2018', '2019', '2020', '2021'])
    ax1.set_ylabel('Revenue')
    ax1.yaxis.set_major_formatter(FuncFormatter(y_axis_formatter))

    st.pyplot(fig1)

    # Create a line chart for the annual revenue of product 2
    st.subheader('Annual Revenue of Product 2')
    fig2, ax2 = plt.subplots()
    ax2.plot(product2_revenues.keys(), product2_revenues.values(), marker='o')
    ax2.set_xlabel('Year')
    ax2.set_xticklabels(['2017', '2018', '2019', '2020', '2021'])
    ax2.set_ylabel('Revenue')
    ax2.yaxis.set_major_formatter(FuncFormatter(y_axis_formatter))

    st.pyplot(fig2)
