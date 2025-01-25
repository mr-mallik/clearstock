""" 
Author: Gulger Mallik
Github: https://github.com/mr-mallik
Date: 2025-01-25
"""

import streamlit as st
from sqlalchemy import create_engine, text
import pandas as pd

def connect():
    # Get database credentials from secrets
    credentials = st.secrets["mysql"]
    
    # Create connection string using secrets
    connection_string = (
        f'mysql+mysqlconnector://{credentials["user"]}:{credentials["password"]}'
        f'@{credentials["host"]}:{credentials["port"]}/{credentials["database"]}'
    )
    
    conn = create_engine(connection_string)
    return conn

def query(conn, query, params=None):
    if params:
        return pd.read_sql(text(query), conn, params=params)
    else:
        return pd.read_sql(text(query), conn)

def execute(conn, query, params=None):
    with conn.connect() as connection:
        if params:
            connection.execute(text(query), params)
            connection.commit()
        else:
            connection.execute(text(query))
            connection.commit()

def close(conn):
    conn.dispose()
