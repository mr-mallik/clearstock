""" 
Author: Gulger Mallik
Github: https://github.com/mr-mallik
Date: 2025-01-25
"""

import config.mysql as mysql
import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="Your Current Stock", page_icon="📦")

conn = mysql.connect()

# get all products
query = """
SELECT `name` FROM `products` ORDER BY `name` ASC
"""
products = mysql.query(conn, query)

# get all markets
query = """
SELECT `name` FROM `markets` ORDER BY `name` ASC
"""
markets = mysql.query(conn, query)

st.header('Stock List')
st.write('This is a list of your current stock.')

with st.form('stock_list_form'):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        product_name = st.selectbox("Product Name", options=products['name'].tolist(), index=0)
    with col2:
        market_name = st.selectbox("Market", options=markets['name'].tolist(), index=0)
    with col3:
        date_of_purchase = st.date_input("Date of Purchase")
    with col4:
        date_of_expiry = st.date_input("Date of Expiry")
    
    submitted = st.form_submit_button("Filter")

    if submitted:
        query = """
        SELECT * FROM `stocks` WHERE `product_name` = :product_name AND `market_name` = :market_name AND `date_of_purchase` = :date_of_purchase AND `date_of_expiry` = :date_of_expiry
        """
        params = {
            'product_name': product_name,
            'market_name': market_name,
            'date_of_purchase': date_of_purchase,
            'date_of_expiry': date_of_expiry
        }
        try:
            stocks = mysql.query(conn, query, params)
            st.table(stocks, hide_index=True)
        except Exception as e:
            st.error(f"Error fetching stocks: {str(e)}")

# close connection
mysql.close(conn)