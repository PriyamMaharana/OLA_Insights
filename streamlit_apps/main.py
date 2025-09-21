import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine, text
import warnings
warnings.filterwarnings('ignore')

# Import queries from the external file
from queries import (
    PEAK_HOURS, RATINGS_BY_VEHICLE, REVENUE_BY_PAYMENT, TOP_CUSTOMERS,
    CANCELLATION_REASONS, DAILY_RIDE_VOLUME, VEHICLE_TYPE_DISTRIBUTION,
    AVG_BOOKING_VALUE_BY_VEHICLE, SURGE_PRICING_ANALYSIS,
    CUSTOMER_RATING_DISTRIBUTION, DRIVER_RATING_DISTRIBUTION,
    TOP_PICKUP_LOCATIONS, AVG_RIDE_DISTANCE_BY_VEHICLE,
    CANCELLATION_BY_VEHICLE, HIGH_VALUE_RIDES
)

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
    /* GENERAL BODY */
    body, .block-container {
        font-family: 'Roboto', sans-serif;
        background-color: 000000;  /* Dark background */
        color: #E0E0E0;  /* Light text */
        margin: 0;
        padding: 2rem 2rem;  /* Added padding for main content */
        box-sizing: border-box;
    }

    /* MAIN HEADER */
    .main-header {
        font-size: 2.8rem;
        color: #FFD369; /* Gold accent */
        text-align: center;
        margin: 2rem 0;
        font-weight: 700;
    }
    
    /* SIDEBAR CONTAINER */
    .sidebar .sidebar-content {
        background-color: #2C2C3A !important;  /* Dark sidebar */
        color: #E0E0E0;
        border-radius: 1rem;
        padding: 1.5rem;
        box-shadow: 0 8px 20px rgba(0,0,0,0.5);
        transition: all 0.3s ease;
    }

    /* SECTION HEADERS */
    .sidebar .sidebar-content h2, 
    .sidebar .sidebar-content h3 {
        color: #FFD369; /* Gold accent */
        font-weight: 600;
        margin-bottom: 0.5rem;
        margin-top: 1rem;
    }

    /* INPUT FIELDS STYLING */
    .sidebar .sidebar-content .stSelectbox, 
    .sidebar .sidebar-content .stMultiselect, 
    .sidebar .sidebar-content .stSlider, 
    .sidebar .sidebar-content .stTextInput, 
    .sidebar .sidebar-content .stDateInput {
        background-color: #1E1E2F !important;
        color: #E0E0E0 !important;
        border: 1px solid #FFD369;
        border-radius: 0.6rem;
        padding: 0.4rem;
        margin-bottom: 1rem;
        width: 100% !important;
        transition: all 0.2s ease;
    }
    .sidebar .sidebar-content .stSelectbox:hover,
    .sidebar .sidebar-content .stMultiselect:hover,
    .sidebar .sidebar-content .stSlider:hover,
    .sidebar .sidebar-content .stTextInput:hover,
    .sidebar .sidebar-content .stDateInput:hover {
        border-color: #FFE085;
    }

    /* EXPANDER CARD EFFECT */
    .sidebar .sidebar-content .streamlit-expanderHeader {
        background-color: #1E1E2F !important;
        color: #FFD369 !important;
        border-radius: 0.6rem;
        padding: 0.5rem 0.8rem;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    .sidebar .sidebar-content .streamlit-expanderContent {
        background-color: #2C2C3A !important;
        border-radius: 0.6rem;
        padding: 0.8rem;
        margin-bottom: 1rem;
    }

    /* HORIZONTAL SEPARATORS */
    .sidebar .sidebar-content hr {
        border-top: 1px solid #FFD369;
        margin: 1rem 0;
    }

    /* KPI CARDS */
    .stMetric > div {
        background-color: #2C2C3A;
        color: #FFD369;
        padding: 1.2rem 2rem;  /* Increased padding */
        border-radius: 1rem;
        text-align: center;
        box-shadow: 0 8px 20px rgba(0,0,0,0.6);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 1.5rem;
    }
    .stMetric > div:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 25px rgba(0,0,0,0.8);
    }

    /* PLOTLY CHARTS */
    .plotly-graph-div {
        background-color: #2C2C3A;
        border-radius: 1rem;
        box-shadow: 0 8px 20px rgba(0,0,0,0.5);
        padding: 1rem;  /* Added padding inside charts */
        margin-bottom: 1.5rem;
    }

    /* DATAFRAME STYLING */
    .stDataFrame table {
        width: 100% !important;
        border-collapse: collapse;
        font-size: 0.9rem;
        color: #E0E0E0;
    }
    .stDataFrame th {
        background-color: #3A3A4D;
        color: #FFD369;
        padding: 0.5rem;
        text-align: center;
    }
    .stDataFrame td {
        background-color: #2C2C3A;
        padding: 0.5rem;
        text-align: center;
    }

    /* FOOTER */
    .footer {
        text-align: center;
        color: #A0A0A0;
        font-size: 0.85rem;
        margin-top: 2rem;
        padding: 1rem;
        border-top: 1px solid #3A3A4D;
        background-color: #1E1E2F;
    }

    /* RESPONSIVE DESIGN */
    @media (max-width: 992px) {
        .main-header {
            font-size: 2.2rem;
        }
        .stMetric > div {
            padding: 1rem 1.5rem;
        }
        .sidebar .sidebar-content {
            padding: 1rem;
        }
        .sidebar .sidebar-content h2, 
        .sidebar .sidebar-content h3 {
            font-size: 1.1rem;
        }
    }

    @media (max-width: 576px) {
        .main-header {
            font-size: 1.8rem;
        }
        .stMetric > div {
            padding: 0.8rem 1rem;
        }
        h2, h3 {
            font-size: 1rem;
        }
        .sidebar .sidebar-content {
            padding: 0.5rem;
        }
        .sidebar .sidebar-content h2, 
        .sidebar .sidebar-content h3 {
            font-size: 1rem;
        }
    }
    </style>
""", unsafe_allow_html=True)




# Database connection function
@st.cache_resource
def init_connection():
    """Initialize database connection"""
    try:
        connection_string = "postgresql://ola_db_8s3u_user:2xwQYvZ46zhTFaQxwZPZNOlUfQSQwYqS@dpg-d37qu495pdvs7384vdi0-a.singapore-postgres.render.com/ola_db_8s3u"
        engine = create_engine(connection_string)
        return engine
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None

# Caching data fetching function
@st.cache_data
def fetch_data(query):
    """
    Fetches data from the database using a given SQL query.
    """
    engine = init_connection()
    if engine is None:
        return pd.DataFrame()
    try:
        with engine.connect() as conn:
            return pd.read_sql(text(query), conn)
    except Exception as e:
        st.error(f"Error executing query: {e}")
        return pd.DataFrame()

# Main dashboard function
def main_dashboard():
    """Main dashboard layout and content"""

    st.markdown('<h1 class="main-header">🚗 OLA Ride Analytics Dashboard</h1>', unsafe_allow_html=True)

    # Sidebar filters
    st.sidebar.header("📊 Dashboard Filters")


    vehicle_types_query = "SELECT DISTINCT vehicle_type FROM public.rides_ola ORDER BY vehicle_type;"
    booking_status_query = "SELECT DISTINCT booking_status FROM public.rides_ola ORDER BY booking_status;"

    vehicle_types_df = fetch_data(vehicle_types_query)
    booking_status_df = fetch_data(booking_status_query)

    all_vehicle_types = vehicle_types_df['vehicle_type'].tolist()
    all_booking_status = booking_status_df['booking_status'].tolist()

    vehicle_types = st.sidebar.multiselect(
        "Select Vehicle Types",
        options=all_vehicle_types,
        default=all_vehicle_types
    )

    booking_status = st.sidebar.multiselect(
        "Select Booking Status",
        options=all_booking_status,
        default=all_booking_status
    )

    where_clause = " WHERE 1=1"
    if vehicle_types:
        vehicles_tuple = tuple(vehicle_types) if len(vehicle_types) > 1 else f"('{vehicle_types[0]}')"
        where_clause += f" AND vehicle_type IN {vehicles_tuple}"
    if booking_status:
        status_tuple = tuple(booking_status) if len(booking_status) > 1 else f"('{booking_status[0]}')"
        where_clause += f" AND booking_status IN {status_tuple}"

    st.markdown("## 📈 Key Performance Indicators")
    kpi_query = f"""
    SELECT
        COUNT(*) AS total_rides,
        SUM(CASE WHEN is_completed = TRUE THEN 1 ELSE 0 END) AS completed_rides,
        AVG(ride_distance) AS avg_ride_distance,
        AVG(driver_ratings) AS avg_rating,
        COUNT(DISTINCT customer_id) AS unique_customers
    FROM public.rides_ola
    {where_clause}
    """
    kpi_df = fetch_data(kpi_query)

    if not kpi_df.empty:
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Total Rides", f"{int(kpi_df.iloc[0]['total_rides']):,}")
        with col2:
            st.metric("Completed Rides", f"{int(kpi_df.iloc[0]['completed_rides']):,}")
        with col3:
            st.metric("Avg Ride Distance", f"{kpi_df.iloc[0]['avg_ride_distance']:.2f} km")
        with col4:
            st.metric("Avg Driver Rating", f"{kpi_df.iloc[0]['avg_rating']:.2f} ⭐")
        with col5:
            st.metric("Unique Customers", f"{int(kpi_df.iloc[0]['unique_customers']):,}")
    else:
        st.warning("No data found for the selected filters.")
        
    st.markdown("---")

    view_option = st.selectbox(
        "Select Dashboard View",
        ["Overall", "Vehicle Type", "Revenue", "Cancellation", "Ratings"]
    )

    if view_option == "Overall":
        show_overall_view(where_clause)
    elif view_option == "Vehicle Type":
        show_vehicle_type_view(where_clause)
    elif view_option == "Revenue":
        show_revenue_view(where_clause)
    elif view_option == "Cancellation":
        show_cancellation_view(where_clause)
    elif view_option == "Ratings":
        show_ratings_view(where_clause)

# In your main Streamlit app file

def show_overall_view(where_clause):
    st.markdown("## 🌟 Overall Performance")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📊 Ride Volume Over Time")

        query = """
            SELECT DATE(date) AS ride_date, COUNT(*) AS ride_count
            FROM public.rides_ola
            WHERE is_completed = TRUE
            GROUP BY ride_date
            ORDER BY ride_date;
        """
        daily_rides_df = fetch_data(query)

        if not daily_rides_df.empty:
            # Optionally add a 7-day rolling average
            daily_rides_df['rolling_avg'] = daily_rides_df['ride_count'].rolling(window=7).mean()

            fig1 = px.line(
                daily_rides_df,
                x='ride_date',
                y=['ride_count', 'rolling_avg'],
                markers=True,
                title="Rides by Day (with 7-Day Moving Average)"
            )

            fig1.update_layout(
                xaxis_title="Date",
                yaxis_title="Number of Rides",
                legend_title="Metrics"
            )

            st.plotly_chart(fig1, use_container_width=True)


    with col2:
        st.markdown("### 📈 Peak Demand Hours")
        # Ensure only one WHERE clause
        base_query = """
            SELECT hour, COUNT(id) AS ride_count
            FROM public.rides_ola
            WHERE is_completed = TRUE
        """
        # Append the dynamic filter
        query = f"{base_query} GROUP BY hour ORDER BY hour;"
        peak_hours_df = fetch_data(query)
        if not peak_hours_df.empty:
            fig2 = px.line(peak_hours_df, x='hour', y='ride_count', title="Rides by Hour of Day")
            st.plotly_chart(fig2, use_container_width=True)

def show_vehicle_type_view(where_clause):
    st.markdown("## 🚙 Vehicle Type Analysis")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📊 Vehicle Type Distribution")
        query = f"{VEHICLE_TYPE_DISTRIBUTION}"
        vehicle_dist_df = fetch_data(query)
        if not vehicle_dist_df.empty:
            fig1 = px.pie(vehicle_dist_df, values='total_rides', names='vehicle_type', title="Total Rides by Vehicle Type")
            st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown("### 📈 Average Ride Distance")
        query = f"{AVG_RIDE_DISTANCE_BY_VEHICLE}"
        avg_distance_df = fetch_data(query)
        if not avg_distance_df.empty:
            fig2 = px.bar(avg_distance_df, x='vehicle_type', y='avg_distance', title="Average Ride Distance by Vehicle Type")
            st.plotly_chart(fig2, use_container_width=True)

def show_revenue_view(where_clause):
    st.markdown("## 💰 Revenue Analysis")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📊 Revenue by Payment Method")
        query = f"{REVENUE_BY_PAYMENT}"
        payment_df = fetch_data(query)
        if not payment_df.empty:
            fig1 = px.pie(payment_df, values='total_revenue', names='payment_method', title="Revenue by Payment Method")
            st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown("### 📈 Top 5 Customers by Revenue")
        query = f"{TOP_CUSTOMERS}"
        top_customers_df = fetch_data(query)
        if not top_customers_df.empty:
            fig2 = px.bar(top_customers_df, x='customer_id', y='total_revenue', title="Top 5 Customers by Revenue")
            st.plotly_chart(fig2, use_container_width=True)

def show_cancellation_view(where_clause):
    st.markdown("## ❌ Cancellation Analysis")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📈 Cancellation Rate by Vehicle Type")
        query = f"{CANCELLATION_BY_VEHICLE}"
        cancellation_df = fetch_data(query)
        if not cancellation_df.empty:
            fig1 = px.bar(cancellation_df, x='vehicle_type', y='cancellation_rate', title="Cancellation Rate by Vehicle Type (%)")
            st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown("### 📊 Top Cancellation Reasons")
        query = f"{CANCELLATION_REASONS}"
        reasons_df = fetch_data(query)
        if not reasons_df.empty:
            fig2 = px.pie(reasons_df, values='cancellation_count', names='customer_reason', title="Top Customer Cancellation Reasons")
            st.plotly_chart(fig2, use_container_width=True)

def show_ratings_view(where_clause):
    st.markdown("## ⭐ Ratings Analysis")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📊 Driver Ratings Distribution")
        query = f"{DRIVER_RATING_DISTRIBUTION}"
        driver_ratings_df = fetch_data(query)
        if not driver_ratings_df.empty:
            fig1 = px.histogram(driver_ratings_df, x='driver_rating', y='rating_count', title="Driver Ratings Distribution")
            st.plotly_chart(fig1, use_container_width=True)
            
    with col2:
        st.markdown("### 📊 Customer Ratings Distribution")
        query = f"{CUSTOMER_RATING_DISTRIBUTION}"
        customer_ratings_df = fetch_data(query)
        if not customer_ratings_df.empty:
            fig2 = px.histogram(customer_ratings_df, x='customer_rating', y='rating_count', title="Customer Ratings Distribution")
            st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### 📊 Average Ratings by Vehicle Type")
    query = f"{RATINGS_BY_VEHICLE}"
    ratings_df = fetch_data(query)
    if not ratings_df.empty:
        fig3 = px.bar(ratings_df, x='vehicle_type', y=['avg_driver_rating', 'avg_customer_rating'], title="Average Ratings by Vehicle Type")
        st.plotly_chart(fig3, use_container_width=True)

# SQL Query Interface
def sql_query_interface():
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
    powerbi_embed_url = "https://app.powerbi.com/reportEmbed?reportId=523bc1bc-5d99-43e0-ab41-5b5043273b49&autoAuth=true&ctid=f8e5ee17-1080-482b-87e2-fa6b0fcf9dfc"
    
    if powerbi_embed_url.startswith("https://app.powerbi.com"):
        st.components.v1.html(
            f'<iframe src="{powerbi_embed_url}" frameborder="0" allowFullScreen="true" style="width:1300px; height:800px;"></iframe>',
            height=800,
        )
    else:
        st.warning("Please publish your Power BI report to the web and paste the embed URL in the code for this tab to function.")

# Main app execution
if __name__ == "__main__":
    # Navigation
    st.sidebar.title("🚗 OLA Analytics")
    page = st.sidebar.radio("Navigate to:", ["Main Dashboard", "SQL Interface", "Power BI Integration"])

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
        🚗 OLA Ride Analytics Dashboard | Built by Priyam Maharana | Data-Driven Insights for Better Decisions
    </div>
    """, unsafe_allow_html=True)