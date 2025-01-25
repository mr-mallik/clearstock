""" 
Author: Gulger Mallik
Github: https://github.com/mr-mallik
Date: 2025-01-25
"""

import config.mysql as mysql
import streamlit as st

st.set_page_config(page_title="Products", page_icon="🥪")

conn = mysql.connect()

def load_products():
    # get all products
    query = """
    SELECT `name` FROM `products` ORDER BY `name` ASC
    """
    products = mysql.query(conn, query)
    # rename the columns
    products.rename(columns={'name': 'Product Name'}, inplace=True)
    return products

products = load_products()

# form to add a new product
with st.form('add_product_form'):
    product_name = st.text_input("Product Name")
    submitted = st.form_submit_button("Add Product")

    if submitted:
        # check if the product already exists
        if product_name.lower() in [p.lower() for p in products['Product Name'].tolist()]:
            st.error("Product already exists")
        else:
            query = """
            INSERT INTO `products`(`name`) VALUES (:product_name)
            """
            params = {
                'product_name': product_name
            }
            try:
                mysql.execute(conn, query, params)
                st.success("Product added successfully")
                # Reload products after adding new one
                products = load_products()
            except Exception as e:
                st.error(f"Error adding product: {str(e)}")

st.dataframe(products, hide_index=True, use_container_width=True)

# close connection
mysql.close(conn)