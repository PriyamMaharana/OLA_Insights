import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from tqdm import tqdm
import os

# ------------------ CONFIG ------------------
DB_URL = os.getenv("DATABASE_URL", "postgresql://ola_db_8s3u_user:2xwQYvZ46zhTFaQxwZPZNOlUfQSQwYqS@dpg-d37qu495pdvs7384vdi0-a.singapore-postgres.render.com/ola_db_8s3u")

# ------------------ FUNCTIONS ------------------
def get_connection():
    """
    Connect to Render PostgreSQL using single DATABASE_URL.
    Returns psycopg2 connection and cursor.
    """
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        print("✅ Connected to Render PostgreSQL successfully.")
        return conn, cur
    except Exception as e:
        print("❌ Error connecting to Render PostgreSQL:", e)
        raise

# ------------------ LOAD CSV ------------------
csv_file = "dataset/ola_cleaned.csv"
df = pd.read_csv(csv_file)
print(f"CSV file loaded successfully. Total rows: {len(df)}")

# Force driver & customer ratings to object and convert NaN → None
for col in ["Driver_Ratings", "Customer_Rating"]:
    if col in df.columns:
        df[col] = df[col].astype(object)
        df[col] = df[col].where(pd.notnull(df[col]), None)

# Convert rest of DataFrame NaN → None
df = df.astype(object).where(pd.notnull(df), None)

# ------------------ CONNECT TO DB ------------------
conn, cur = get_connection()

# ------------------ CREATE TABLE ------------------
create_table_query = """
CREATE TABLE IF NOT EXISTS rides_ola (
    id SERIAL PRIMARY KEY,
    Date TIMESTAMP,
    Time TIME,
    Booking_Id VARCHAR(50),
    Booking_Status VARCHAR(50),
    Customer_Id VARCHAR(50),
    Vehicle_Type VARCHAR(50),
    Pickup_Location VARCHAR(100),
    Drop_Location VARCHAR(100),
    V_Tat FLOAT,
    C_Tat FLOAT,
    Canceled_Rides_By_Customer TEXT,
    Canceled_Rides_By_Driver TEXT,
    Incomplete_Rides TEXT,
    Incomplete_Rides_Reason TEXT,
    Booking_Value FLOAT,
    Payment_Method VARCHAR(50),
    Ride_Distance FLOAT,
    Driver_Ratings FLOAT,
    Customer_Rating FLOAT,
    Vehicle_Images TEXT,
    Is_Completed BOOLEAN,
    Is_Canceled BOOLEAN,
    DayOfWeek VARCHAR(20),
    Month INT,
    Hour INT
);
"""
cur.execute(create_table_query)
conn.commit()
print("Table 'rides_ola' created successfully (if it did not exist).")

# ------------------ INSERT DATA IN BATCHES ------------------
from math import ceil
from psycopg2.extras import execute_values

insert_query = """
INSERT INTO rides_ola (
    Date, Time, Booking_Id, Booking_Status, Customer_Id, Vehicle_Type,
    Pickup_Location, Drop_Location, V_Tat, C_Tat,
    Canceled_Rides_By_Customer, Canceled_Rides_By_Driver,
    Incomplete_Rides, Incomplete_Rides_Reason, Booking_Value,
    Payment_Method, Ride_Distance, Driver_Ratings, Customer_Rating,
    Vehicle_Images, Is_Completed, Is_Canceled, DayOfWeek, Month, Hour
) VALUES %s;
"""

batch_size = 10000
total_rows = len(df)
num_batches = ceil(total_rows / batch_size)

print(f"Inserting {total_rows} rows in {num_batches} batches of {batch_size}...")

for i in tqdm(range(num_batches), desc="Batch inserting"):
    start_idx = i * batch_size
    end_idx = min(start_idx + batch_size, total_rows)
    batch = df.iloc[start_idx:end_idx]
    values = [tuple(x) for x in batch.to_numpy()]
    execute_values(cur, insert_query, values)
    conn.commit()  # commit after each batch

print("✅ All data loaded successfully into Render PostgreSQL!")

# Close connection
cur.close()
conn.close()
