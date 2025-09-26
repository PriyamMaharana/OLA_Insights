# OLA Ride-Sharing Data Analysis

## Project Overview

The rise of ride-sharing platforms has transformed urban mobility, providing convenience and affordability to millions. OLA, a leading ride-hailing service, generates vast amounts of data from ride bookings, driver availability, fare calculations, and customer preferences.

This project analyzes OLA’s ride-sharing data to derive actionable insights using **SQL**, **Power BI**, and **Streamlit**, helping optimize operations, improve customer satisfaction, and support data-driven decision-making.

```bash
insights-ola.streamlit.app
```

---

## Problem Statement

Extracting meaningful insights from large ride-sharing datasets is challenging. This project focuses on:

- Cleaning and processing raw ride data
- Performing Exploratory Data Analysis (EDA)
- Developing an interactive **Power BI dashboard**
- Creating a **Streamlit web application** to visualize key findings

---

## Business Use Cases

- **Peak Demand Analysis**: Identify peak demand hours and optimize driver allocation.
- **Customer Behavior Analysis**: Analyze customer behavior for personalized marketing strategies.
- **Pricing Strategy**: Understand pricing patterns and surge pricing effectiveness.
- **Anomaly Detection**: Detect anomalies or fraudulent activities in ride data.

---

## SQL Queries

1. Retrieve all successful bookings.
2. Find the average ride distance for each vehicle type.
3. Get the total number of cancelled rides by customers.
4. List the top 5 customers who booked the highest number of rides.
5. Get the number of rides cancelled by drivers due to personal and car-related issues.
6. Find the maximum and minimum driver ratings for Prime Sedan bookings.
7. Retrieve all rides where payment was made using UPI.
8. Find the average customer rating per vehicle type.
9. Calculate the total booking value of rides completed successfully.
10. List all incomplete rides along with the reason.

---

## Power BI Dashboard Visualizations

1. **Ride Volume Over Time**
2. **Booking Status Breakdown**
3. **Top 5 Vehicle Types by Ride Distance**
4. **Average Customer Ratings by Vehicle Type**
5. **Cancelled Rides Reasons**
6. **Revenue by Payment Method**
7. **Top 5 Customers by Total Booking Value**
8. **Ride Distance Distribution Per Day**
9. **Driver Ratings Distribution**
10. **Customer vs. Driver Ratings**

---

## Streamlit Application

A user-friendly web application built with Streamlit to:

- Display SQL query results interactively.
- Provide filters for dynamic data exploration.
- Embed Power BI visuals for comprehensive analytics.

---

## Project Deliverables

- Cleaned and optimized SQL queries.
- Interactive Power BI dashboards.
- Fully functional Streamlit application.
- Comprehensive project documentation.

---

## How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/PriyamMaharana/OLA_Insights.git
cd OLA_Insights
```


### 2. Install python dependencies

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-F58025?style=for-the-badge&logo=matplotlib&logoColor=white)
![Seaborn](https://img.shields.io/badge/Seaborn-4C72B0?style=for-the-badge&logo=seaborn&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/SQL-4479A1?style=for-the-badge&logo=postgresql&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=for-the-badge&logo=power-bi&logoColor=black)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)
![Jupyter Notebook](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)


```bash
pip install -r requirements.txt
```


### 3. Setup SQL Database (PostgresSQL + Render)

 - Create a database in your preferred SQL engine (PostgreSQL, MySQL, etc.).
 - Load the dataset from dataset/ola_cleaned.csv into your database.
 - Execute SQL scripts located in sql_queries/ to generate insights.


### 4. Open Power BI Dashboard

 - Open powerbi/OLA_Dashboard.pbix using Power BI Desktop.
 - Connect the dashboard to your dataset or use embedded demo data.
 - Interact with visualizations and filters to explore insights.


### 5. Run Streamlit App

```bash
streamlit run streamlit_apps/main.py
```

---

## Features & Skills

![Data Cleaning](https://img.shields.io/badge/Data%20Cleaning-00BFFF?style=for-the-badge)
![Data Visualization](https://img.shields.io/badge/Data%20Visualization-4CAF50?style=for-the-badge)
![EDA](https://img.shields.io/badge/Exploratory%20Data%20Analysis-FF69B4?style=for-the-badge)
![SQL Queries](https://img.shields.io/badge/SQL%20Queries-FF8C00?style=for-the-badge)
![Interactive Dashboards](https://img.shields.io/badge/Interactive%20Dashboards-8A2BE2?style=for-the-badge)
![Feature Engineering](https://img.shields.io/badge/Feature%20Engineering-00CED1?style=for-the-badge)
![Business Insights](https://img.shields.io/badge/Business%20Insights-FF1493?style=for-the-badge)
