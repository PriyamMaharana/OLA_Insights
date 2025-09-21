# db_utils.py

import psycopg2
import psycopg2.extras
import streamlit as st
import pandas as pd

DB_PARAMS = {
    "host": "localhost",
    "port": 5432,
    "database": "ols_db",
    "user": "postgres",
    "password": "1234"
}

@st.cache_data(ttl=600)
def get_data_from_db(query):
    """Execute SQL query and return DataFrame."""
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(query)
        rows = cur.fetchall()
        df = pd.DataFrame(rows)
        cur.close()
        conn.close()
        return df
    except Exception as e:
        st.error(f"Database query failed: {e}")
        return pd.DataFrame()
