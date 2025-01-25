""" 
Author: Gulger Mallik
Github: https://github.com/mr-mallik
Date: 2025-01-25
 """


import config.mysql as mysql
import streamlit as st
from datetime import datetime
st.set_page_config(page_title="Clearstock Home", page_icon="📦")

# define units
@st.cache_data
def load_units():
    units = ['kg', 'g', 'ml', 'l', 'pcs', 'unit']
    return units
units = load_units()

st.title("Welcome to Clearstock")
st.write("Manage your inventory efficiently with Clearstock.")

conn = mysql.connect()

query = """
SELECT date_of_purchase, product_name, date_of_expiry, qty FROM stocks ORDER BY date_of_expiry ASC
"""
expiring_products = mysql.query(conn, query)
# rename columns
expiring_products.rename(columns={'date_of_purchase': 'Date of Purchase', 'product_name': 'Product Name', 
                                  'date_of_expiry': 'Date of Expiry', 'qty': 'Quantity'}, inplace=True)

st.header("Expiring Products")
st.dataframe(expiring_products, hide_index=True, use_container_width=True)

# Add month selector with session state
if 'previous_month' not in st.session_state:
    st.session_state.previous_month = datetime.now().month
if 'previous_year' not in st.session_state:
    st.session_state.previous_year = datetime.now().year

current_month = st.session_state.previous_month
current_year = st.session_state.previous_year

col1, col2 = st.columns(2)
with col1:
    selected_month = st.selectbox(
        "Select Month",
        range(1, 13),
        index=current_month - 1,
        format_func=lambda x: datetime(current_year, x, 1).strftime('%B'),
        key='month_selector'
    )
with col2:
    selected_year = st.selectbox(
        "Select Year", 
        range(2020, current_year + 1),
        index=current_year - 2020,
        key='year_selector'
    )

# Check if month or year has changed
if (selected_month != st.session_state.previous_month or 
    selected_year != st.session_state.previous_year):
    st.session_state.previous_month = selected_month
    st.session_state.previous_year = selected_year
    st.rerun()

# Query with month filter
query = """
SELECT date_of_purchase, SUM(price * qty) AS total_value 
FROM stocks 
WHERE MONTH(date_of_purchase) = :month
AND YEAR(date_of_purchase) = :year
GROUP BY date_of_purchase 
ORDER BY date_of_purchase ASC
"""
total_value = mysql.query(conn, query, params={'month': selected_month, 'year': selected_year})

query = """
SELECT market_name, SUM(price * qty) AS total_value 
FROM stocks
WHERE MONTH(date_of_purchase) = :month
AND YEAR(date_of_purchase) = :year
GROUP BY market_name 
ORDER BY market_name ASC
"""
market_value = mysql.query(conn, query, params={'month': selected_month, 'year': selected_year})

col1, col2 = st.columns(2)
with col1:
    st.header("Daily Expenses")
    if not total_value.empty:
        st.line_chart(total_value, x='date_of_purchase', y='total_value')
    else:
        st.write("No data available for selected month")
with col2:
    st.header("Market Value")
    if not market_value.empty:
        st.pie_chart(market_value, values='total_value', names='market_name')
    else:
        st.write("No data available for selected month")