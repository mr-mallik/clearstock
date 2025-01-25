""" 
Author: Gulger Mallik
Github: https://github.com/mr-mallik
Date: 2025-01-25
"""

import config.mysql as mysql
import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="Add Stock", page_icon="📦")

# past 30 days
past_30_days = datetime.now().date() - timedelta(days=30)

conn = mysql.connect()

# get all products
query = """
SELECT name FROM products ORDER BY name ASC
"""
products = mysql.query(conn, query)

# get all markets
query = """
SELECT name FROM markets ORDER BY name ASC
"""
markets = mysql.query(conn, query)

st.header('Stock')
st.write('This is a list of all products in the database and their last updated price and market.')

new_stock = st.empty()

with st.form("add_product_form"):
    st.write('Add a new purchase of product to the stock.')

    product_name = st.selectbox("Product Name", options=products['name'].tolist(), index=0)
    market_name = st.selectbox("Market", options=markets['name'].tolist(), index=0)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        price = st.number_input("Price", min_value=0.0, step=0.01)
    with col2:
        quantity = st.number_input("Qty", min_value=0.0, step=0.01)
    with col3:
        date_of_expiry = st.date_input("Expiry Date", min_value=past_30_days)
    with col4:
        date_of_purchase = st.date_input("Purchase Date", 
                                        min_value=past_30_days, 
                                        max_value=datetime.now().date(), 
                                        value=datetime.now().date())

    submitted = st.form_submit_button("Add Product")
    
    if submitted:
        # add to new_stock
        new_stock.write(f"Added {quantity} of {product_name} to {market_name} at {price} each.")

        query = """
        INSERT INTO stocks (product_name, price, market_name, date_of_purchase, date_of_expiry, qty) 
        VALUES (:product_name, :price, :market_name, :date_of_purchase, :date_of_expiry, :qty)
        """
        params = {
            'product_name': product_name,
            'price': price,
            'market_name': market_name,
            'date_of_purchase': date_of_purchase,
            'date_of_expiry': date_of_expiry,
            'qty': quantity
        }
        
        try:
            mysql.execute(conn, query, params)
            st.success("Product added successfully!")
        except Exception as e:
            st.error(f"Error adding product: {str(e)}")

# close connection
mysql.close(conn)