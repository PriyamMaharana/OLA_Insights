import psycopg2
from psycopg2.extras import RealDictCursor

DB_USER = "postgres"
DB_PASS = "1234"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "ola_db"

DB_URL = "postgresql://ola_db_8s3u_user:2xwQYvZ46zhTFaQxwZPZNOlUfQSQwYqS@dpg-d37qu495pdvs7384vdi0-a.singapore-postgres.render.com/ola_db_8s3u"

def get_connection():
    """
    Returns a psycopg2 connection and cursor.
    Cursor uses RealDictCursor for dictionary-like results.
    """
    # try:
    #     conn = psycopg2.connect(
    #         host=DB_HOST,
    #         database=DB_NAME,
    #         user=DB_USER,
    #         password=DB_PASS,
    #         port=DB_PORT
    #     )
    #     cur = conn.cursor(cursor_factory=RealDictCursor)
    #     print("Database connected successfully.")
    #     return conn, cur
    # except Exception as e:
    #     print("Error connecting to the database:", e)
    #     raise

    try:
        conn = psycopg2.connect(DB_URL, cursor_factory=RealDictCursor)
        return conn
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None
        
