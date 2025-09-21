# OLA Ride-Sharing Data Analysis Project

## Project Overview
The rise of ride-sharing platforms has transformed urban mobility, providing convenience and affordability to millions. OLA, a leading ride-hailing service, generates vast amounts of data from ride bookings, driver availability, fare calculations, and customer preferences.  

This project analyzes OLA’s ride-sharing data to derive actionable insights using **SQL, Power BI, and Streamlit**, helping optimize operations, improve customer satisfaction, and support data-driven decision-making.

---

## Problem Statement
Extracting meaningful insights from large ride-sharing datasets is challenging. This project focuses on:  
- Cleaning and processing raw ride data  
- Performing Exploratory Data Analysis (EDA)  
- Developing an interactive **Power BI dashboard**  
- Creating a **Streamlit web application** to visualize key findings  

---

## Business Use Cases
- Identify peak demand hours and optimize driver allocation  
- Analyze customer behavior for personalized marketing  
- Understand pricing patterns and surge pricing effectiveness  
- Detect anomalies or fraudulent activities  

---

## Project Approach
### 1. Data Understanding & Exploration
- Examine dataset structure and key variables (ride status, payment, ratings)  
- Perform initial EDA to uncover trends  

### 2. Data Cleaning & Preprocessing
- Handle missing and inconsistent values  
- Convert data types and standardize formats  
- Create derived features for deeper insights  

### 3. SQL Query Development
- Extract insights using queries (trends, cancellations, ratings)  
- Optimize queries for performance and accuracy  
- Validate results against dataset  

### 4. Power BI Dashboard Creation
- Interactive visualizations for ride trends, revenue, and cancellations  
- Filters and slicers for dynamic data exploration  
- KPIs and metrics for actionable insights  

### 5. Streamlit Application Development
- User-friendly UI to display SQL query results  
- Interactive filters and search options  
- Embedded Power BI visuals for a complete analytics experience  

### 6. Documentation & Deployment
- Document queries, dashboards, and insights  
- Deploy Streamlit app for accessible data exploration  
- Present findings with business-oriented storytelling  

---

## SQL Queries Examples
- Retrieve all successful bookings  
- Average ride distance per vehicle type  
- Total number of canceled rides by customers  
- Top 5 customers with the highest number of rides  
- Rides canceled by drivers due to personal/car issues  
- Maximum and minimum driver ratings for Prime Sedan bookings  
- Rides paid using UPI  
- Average customer rating per vehicle type  
- Total booking value of completed rides  
- Incomplete rides with cancellation reasons  

---

## Power BI Dashboard Visualizations
**Overall**
- Ride Volume Over Time  
- Booking Status Breakdown  

**Vehicle Type**
- Top 5 Vehicle Types by Ride Distance  

**Revenue**
- Revenue by Payment Method  
- Top 5 Customers by Total Booking Value  
- Ride Distance Distribution Per Day  

**Cancellation**
- Cancelled Rides Reasons (Customer & Driver)  

**Ratings**
- Driver Ratings Distribution  
- Customer Ratings Distribution  

---

## Project Results
- Interactive dashboards and applications showcasing key insights  
- Streamlined access to booking trends, ratings, and revenue analysis  
- Actionable insights to improve ride experience and service efficiency  

---

## Technical Stack
- **Languages & Libraries:** Python, Pandas, NumPy, Matplotlib, Seaborn  
- **Database:** SQL  
- **BI & Visualization:** Power BI  
- **Web App:** Streamlit  
- **Data Processing:** Data Cleaning, Feature Engineering, EDA  

---

## Folder Structure
- ola-ride-sharing-analysis/
- │
- ├── data/
- │ └── ola_dataset.csv
- │
- ├── sql_queries/
- │ ├── successful_bookings.sql
- │ ├── avg_ride_distance.sql
- │ ├── cancelled_rides.sql
- │ └── ...
- │
- ├── powerbi/
- │ └── OLA_Dashboard.pbix
- │
- ├── app.py
- ├── requirements.txt
- ├── README.md
- └── LICENSE
