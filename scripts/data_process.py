import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv('dataset/ola_rides.csv')

# 1. Normalize column names (strip spaces, make consistent)
df.columns = df.columns.str.strip().str.replace(' ', '_').str.title()
print("Columns after normalization:", df.columns.tolist())

# 2. Drop duplicate Booking_IDs (if column exists)
if 'Booking_Id' in df.columns:
    df.drop_duplicates(subset='Booking_Id', inplace=True)

# 3. Replace 'null' and empty strings with NaN (only for relevant columns)
for col in df.columns:
    if df[col].dtype == object:
        df[col] = df[col].replace({'null': np.nan, '': np.nan})

# 4. Convert 'Date' column to proper datetime if exists
if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce', infer_datetime_format=True)

# 5. Convert numeric columns safely
num_cols = ['Booking_Value', 'Ride_Distance', 'Driver_Ratings', 'Customer_Rating']
for col in num_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# 6. Standardize categorical columns
category_cols = ['Booking_Status', 'Vehicle_Type', 'Payment_Method']
for col in category_cols:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip().str.title()


# 8. Clean Pickup/Drop locations
for col in ['Pickup_Location', 'Drop_Location']:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()

# 10. Feature engineering: Completed & Canceled flags
if 'Booking_Status' in df.columns:
    df['Is_Completed'] = df['Booking_Status'] == 'Success'
    df['Is_Canceled'] = df['Booking_Status'].str.contains('Canceled', case=False, na=False)

# 11. Outlier handling (optional)
for col in ['Booking_Value', 'Ride_Distance', 'Driver_Ratings', 'Customer_Rating']:
    if col in df.columns:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        df[col] = np.where((df[col] < lower) | (df[col] > upper), np.nan, df[col])

# 12. Derived time features (now using converted Date column)
if 'Date' in df.columns and pd.api.types.is_datetime64_any_dtype(df['Date']):
    df['DayOfWeek'] = df['Date'].dt.day_name()
    df['Month'] = df['Date'].dt.month
    df['Hour'] = df['Date'].dt.hour
else:
    print("⚠️ Date column missing or not converted to datetime — skipping time features.")
    
# ✅ 13. Convert NaN to None for Driver_Ratings and Customer_Rating (so CSV has NULL)
for rating_col in ['Driver_Ratings', 'Customer_Rating']:
    if rating_col in df.columns:
        df[rating_col] = df[rating_col].where(pd.notnull(df[rating_col]), None)

# 13. Final report
print("\n=== Final Null Count ===")
print(df.isnull().sum())
print("\n=== Data Info ===")
print(df.info())
print("\nSample Data:")
print(df.head())

# Save cleaned data
df.to_csv('dataset/ola_cleaned.csv', index=False)
print("\n✅ Cleaned dataset saved to ../dataset/ola_cleaned.csv")
