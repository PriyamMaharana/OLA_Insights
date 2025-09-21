import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import psycopg2
from sqlalchemy import create_engine
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="OLA Ride Analytics Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    </style>
""", unsafe_allow_html=True)

# Database connection function
@st.cache_resource
def init_connection():
    """Initialize database connection"""
    try:
        # Replace with your actual database credentials
        connection_string = "postgresql://postgres:1234@localhost:5432/ola_db"
        engine = create_engine(connection_string)
        return engine
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None

# Load sample data function (for demo purposes)
@st.cache_data
def load_sample_data():
    """Load sample OLA booking data"""
    np.random.seed(42)
    n_records = 1000

    data = {
        'Date': pd.date_range('2024-01-01', periods=n_records, freq='H'),
        'Booking_ID': [f'CNR{str(i).zfill(10)}' for i in range(1, n_records+1)],
        'Customer_ID': np.random.randint(1, 200, n_records),
        'Vehicle_Type': np.random.choice(['Auto', 'Prime Plus', 'Prime Sedan', 'Prime SUV', 'Bike'], n_records),
        'Booking_Status': np.random.choice(['Success', 'Cancelled by Customer', 'Cancelled by Driver'], 
                                         n_records, p=[0.65, 0.20, 0.15]),
        'Pickup_Location': np.random.choice(['Koramangala', 'Whitefield', 'Electronic City', 'HSR Layout', 
                                           'Indiranagar', 'Marathahalli', 'Jayanagar'], n_records),
        'Drop_Location': np.random.choice(['Koramangala', 'Whitefield', 'Electronic City', 'HSR Layout', 
                                         'Indiranagar', 'Marathahalli', 'Jayanagar'], n_records),
        'Booking_Value': np.random.normal(150, 50, n_records).clip(50, 500),
        'Ride_Distance': np.random.exponential(8, n_records).clip(1, 50),
        'Payment_Method': np.random.choice(['UPI', 'Cash', 'Card', 'Wallet'], n_records),
        'Driver_Ratings': np.random.choice([3.0, 3.5, 4.0, 4.5, 5.0], n_records, p=[0.05, 0.10, 0.25, 0.35, 0.25]),
        'Customer_Rating': np.random.choice([3.0, 3.5, 4.0, 4.5, 5.0], n_records, p=[0.08, 0.12, 0.30, 0.30, 0.20]),
        'Cancelled_Rides_by_Customer': np.where(np.random.rand(n_records) < 0.2, 'Yes', 'No'),
        'Cancelled_Rides_by_Driver': np.where(np.random.rand(n_records) < 0.15, 'Yes', 'No'),
    }

    df = pd.DataFrame(data)
    df['Hour'] = df['Date'].dt.hour
    df['Day_of_Week'] = df['Date'].dt.day_name()
    df['Month'] = df['Date'].dt.month_name()

    return df

# Main dashboard function
def main_dashboard():
    """Main dashboard layout and content"""

    # Header
    st.markdown('<h1 class="main-header">🚗 OLA Ride Analytics Dashboard</h1>', unsafe_allow_html=True)

    # Load data
    df = load_sample_data()

    # Sidebar filters
    st.sidebar.header("📊 Dashboard Filters")

    # Date range filter
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(df['Date'].min().date(), df['Date'].max().date()),
        min_value=df['Date'].min().date(),
        max_value=df['Date'].max().date()
    )

    # Vehicle type filter
    vehicle_types = st.sidebar.multiselect(
        "Select Vehicle Types",
        options=df['Vehicle_Type'].unique(),
        default=df['Vehicle_Type'].unique()
    )

    # Booking status filter
    booking_status = st.sidebar.multiselect(
        "Select Booking Status",
        options=df['Booking_Status'].unique(),
        default=df['Booking_Status'].unique()
    )

    # Apply filters
    filtered_df = df[
        (df['Date'].dt.date >= date_range[0]) &
        (df['Date'].dt.date <= date_range[1]) &
        (df['Vehicle_Type'].isin(vehicle_types)) &
        (df['Booking_Status'].isin(booking_status))
    ]

    # Key Metrics Row
    st.markdown("## 📈 Key Performance Indicators")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        total_rides = len(filtered_df)
        st.metric("Total Rides", f"{total_rides:,}")

    with col2:
        success_rate = (filtered_df['Booking_Status'] == 'Success').mean() * 100
        st.metric("Success Rate", f"{success_rate:.1f}%")

    with col3:
        total_revenue = filtered_df[filtered_df['Booking_Status'] == 'Success']['Booking_Value'].sum()
        st.metric("Total Revenue", f"₹{total_revenue:,.0f}")

    with col4:
        avg_rating = filtered_df['Driver_Ratings'].mean()
        st.metric("Avg Driver Rating", f"{avg_rating:.2f}⭐")

    with col5:
        unique_customers = filtered_df['Customer_ID'].nunique()
        st.metric("Unique Customers", f"{unique_customers:,}")

    # Dashboard Views
    st.markdown("---")

    # View selector
    view_option = st.selectbox(
        "Select Dashboard View",
        ["Overall", "Vehicle Type", "Revenue", "Cancellation", "Ratings"]
    )

    if view_option == "Overall":
        show_overall_view(filtered_df)
    elif view_option == "Vehicle Type":
        show_vehicle_type_view(filtered_df)
    elif view_option == "Revenue":
        show_revenue_view(filtered_df)
    elif view_option == "Cancellation":
        show_cancellation_view(filtered_df)
    elif view_option == "Ratings":
        show_ratings_view(filtered_df)

def show_overall_view(df):
    """Overall dashboard view"""
    st.markdown("## 🌟 Overall Performance")

    col1, col2 = st.columns(2)

    with col1:
        # Ride Volume Over Time
        st.markdown("### 📊 Ride Volume Over Time")
        hourly_rides = df.groupby('Hour').size().reset_index(name='Rides')
        fig1 = px.line(hourly_rides, x='Hour', y='Rides', 
                      title="Rides by Hour of Day")
        fig1.update_layout(height=400)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        # Booking Status Breakdown
        st.markdown("### 📈 Booking Status Breakdown")
        status_counts = df['Booking_Status'].value_counts()
        fig2 = px.pie(values=status_counts.values, names=status_counts.index,
                     title="Booking Status Distribution")
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, use_container_width=True)

def show_vehicle_type_view(df):
    """Vehicle type analysis view"""
    st.markdown("## 🚙 Vehicle Type Analysis")

    # Top 5 Vehicle Types by Ride Distance
    vehicle_distance = df.groupby('Vehicle_Type')['Ride_Distance'].agg(['sum', 'mean', 'count']).reset_index()
    vehicle_distance.columns = ['Vehicle_Type', 'Total_Distance', 'Avg_Distance', 'Total_Rides']
    vehicle_distance = vehicle_distance.sort_values('Total_Distance', ascending=False).head(5)

    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.bar(vehicle_distance, x='Vehicle_Type', y='Total_Distance',
                     title="Top 5 Vehicle Types by Total Distance")
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.bar(vehicle_distance, x='Vehicle_Type', y='Avg_Distance',
                     title="Average Distance by Vehicle Type")
        st.plotly_chart(fig2, use_container_width=True)

    # Vehicle performance table
    st.markdown("### 📋 Vehicle Performance Summary")
    st.dataframe(vehicle_distance, use_container_width=True)

def show_revenue_view(df):
    """Revenue analysis view"""
    st.markdown("## 💰 Revenue Analysis")

    successful_rides = df[df['Booking_Status'] == 'Success']

    col1, col2 = st.columns(2)

    with col1:
        # Revenue by Payment Method
        payment_revenue = successful_rides.groupby('Payment_Method')['Booking_Value'].sum().reset_index()
        fig1 = px.pie(payment_revenue, values='Booking_Value', names='Payment_Method',
                     title="Revenue by Payment Method")
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        # Top 5 Customers by Total Booking Value
        customer_revenue = successful_rides.groupby('Customer_ID')['Booking_Value'].sum().reset_index()
        top_customers = customer_revenue.nlargest(5, 'Booking_Value')
        fig2 = px.bar(top_customers, x='Customer_ID', y='Booking_Value',
                     title="Top 5 Customers by Revenue")
        st.plotly_chart(fig2, use_container_width=True)

    # Daily revenue trend
    st.markdown("### 📈 Daily Revenue Trend")
    daily_revenue = successful_rides.groupby(successful_rides['Date'].dt.date)['Booking_Value'].sum().reset_index()
    fig3 = px.line(daily_revenue, x='Date', y='Booking_Value',
                  title="Daily Revenue Trend")
    st.plotly_chart(fig3, use_container_width=True)

def show_cancellation_view(df):
    """Cancellation analysis view"""
    st.markdown("## ❌ Cancellation Analysis")

    col1, col2 = st.columns(2)

    with col1:
        # Customer cancellations by hour
        customer_cancel = df[df['Cancelled_Rides_by_Customer'] == 'Yes']
        hourly_cancel = customer_cancel.groupby('Hour').size().reset_index(name='Cancellations')
        fig1 = px.bar(hourly_cancel, x='Hour', y='Cancellations',
                     title="Customer Cancellations by Hour")
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        # Driver cancellations by vehicle type
        driver_cancel = df[df['Cancelled_Rides_by_Driver'] == 'Yes']
        vehicle_cancel = driver_cancel.groupby('Vehicle_Type').size().reset_index(name='Cancellations')
        fig2 = px.bar(vehicle_cancel, x='Vehicle_Type', y='Cancellations',
                     title="Driver Cancellations by Vehicle Type")
        st.plotly_chart(fig2, use_container_width=True)

    # Cancellation rates
    st.markdown("### 📊 Cancellation Rates by Day of Week")
    cancellation_rates = df.groupby('Day_of_Week').agg({
        'Cancelled_Rides_by_Customer': lambda x: (x == 'Yes').mean() * 100,
        'Cancelled_Rides_by_Driver': lambda x: (x == 'Yes').mean() * 100
    }).reset_index()

    fig3 = px.bar(cancellation_rates, x='Day_of_Week', 
                 y=['Cancelled_Rides_by_Customer', 'Cancelled_Rides_by_Driver'],
                 title="Cancellation Rates by Day of Week (%)",
                 barmode='group')
    st.plotly_chart(fig3, use_container_width=True)

def show_ratings_view(df):
    """Ratings analysis view"""
    st.markdown("## ⭐ Ratings Analysis")

    col1, col2 = st.columns(2)

    with col1:
        # Driver Ratings Distribution
        fig1 = px.histogram(df, x='Driver_Ratings', nbins=10,
                           title="Driver Ratings Distribution")
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        # Customer Ratings Distribution
        fig2 = px.histogram(df, x='Customer_Rating', nbins=10,
                           title="Customer Ratings Distribution")
        st.plotly_chart(fig2, use_container_width=True)

    # Average ratings by vehicle type
    st.markdown("### 📊 Average Ratings by Vehicle Type")
    ratings_by_vehicle = df.groupby('Vehicle_Type').agg({
        'Driver_Ratings': 'mean',
        'Customer_Rating': 'mean'
    }).reset_index()

    fig3 = px.bar(ratings_by_vehicle, x='Vehicle_Type', 
                 y=['Driver_Ratings', 'Customer_Rating'],
                 title="Average Ratings by Vehicle Type",
                 barmode='group')
    st.plotly_chart(fig3, use_container_width=True)

# SQL Query Interface
def sql_query_interface():
    """Interactive SQL query interface"""
    st.markdown("## 💻 SQL Query Interface")

    # Predefined queries
    predefined_queries = {
        "All Successful Bookings": "select * from rides_ola WHERE booking_status = 'Success';",
        "Average Distance by Vehicle": "select vehicle_type, trunc(avg(ride_distance)::numeric,1) as avg_ride_km from rides_ola group by vehicle_type;",
        "Total Rides Cancelled by Customers": "select count(*) as ride_cancelled_by_customer from rides_ola where booking_status = 'Canceled By Customer';",
        "Top 5 Customers": "select * from top_5_customers;",
        "Total Rides Cancelled by Drivers": "select * from rides_cancelled_by_driver;",
        "Maximun & Minimum Driver ratings for Prime Sedan": "select * from driver_rating_for_prime_sedan;",
        "All rides with payment": "select * from rides_ola where payment_method = 'Upi';",
        "Average Customer ratings per Vehicle": "select * from avg_customer_ratings_per_vehicle;",
        "Total Revenue by Payment Method": "select sum(booking_value) as total_rides_value from rides_ola where booking_status = 'Success';",
        "List All incomplete rides with reason": "select booking_id, incomplete_rides_reason from rides_ola where incomplete_rides = 'Yes';"
    }

    query_option = st.selectbox(
        "Select a predefined query or write a custom query:", 
        ["Custom"] + list(predefined_queries.keys())
    )

    if query_option == "Custom":
        sql_query = st.text_area("Enter SQL query:", height=150)
    else:
        sql_query = st.text_area("SQL Query:", value=predefined_queries[query_option], height=150)

    if st.button("Execute Query"):
        if sql_query.strip():
            result_df = fetch_data(sql_query)
            st.dataframe(result_df)
        else:
            st.warning("Please enter a SQL query.")

# Power BI Integration placeholder
def power_bi_integration():
    """Power BI dashboard integration"""
    st.markdown("## 📊 Power BI Dashboard Integration")

    st.info("👆 This section would contain embedded Power BI reports in a production environment.")

    # Placeholder for Power BI embed
    st.markdown("""
    ### 🔗 Power BI Reports

    In a production environment, this section would include:

    1. **Overall Performance Dashboard**
       - Key metrics and KPIs
       - Trend analysis
       - Real-time monitoring

    2. **Vehicle Type Analysis**
       - Performance by vehicle category
       - Utilization rates
       - Revenue contribution

    3. **Revenue Analytics**
       - Payment method analysis
       - Customer segment revenue
       - Pricing insights

    4. **Operational Insights**
       - Cancellation patterns
       - Driver performance
       - Customer satisfaction metrics
    """)

# Main app execution
if __name__ == "__main__":
    # Navigation
    st.sidebar.title("🚗 OLA Analytics")
    page = st.sidebar.radio("Navigate to:", 
                           ["Main Dashboard", "SQL Interface", "Power BI Integration"])

    if page == "Main Dashboard":
        main_dashboard()
    elif page == "SQL Interface":
        sql_query_interface()
    elif page == "Power BI Integration":
        power_bi_integration()

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        🚗 OLA Ride Analytics Dashboard | Built with Streamlit | Data-Driven Insights for Better Decisions
    </div>
    """, unsafe_allow_html=True)
