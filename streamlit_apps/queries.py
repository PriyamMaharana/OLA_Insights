# queries.py

# -----------------------------
# Existing Queries
# -----------------------------
GET_ALL_RIDES = "SELECT * FROM public.rides_ola;"

PEAK_HOURS = """
SELECT hour, COUNT(id) AS ride_count
FROM public.rides_ola
WHERE is_completed = TRUE
GROUP BY hour
ORDER BY hour;
"""

RATINGS_BY_VEHICLE = """
SELECT vehicle_type,
       AVG(driver_ratings) AS avg_driver_rating,
       AVG(customer_rating) AS avg_customer_rating,
       AVG(booking_value) AS avg_booking_value
FROM public.rides_ola
GROUP BY vehicle_type
ORDER BY vehicle_type;
"""

REVENUE_BY_PAYMENT = """
SELECT payment_method,
       SUM(booking_value) AS total_revenue
FROM public.rides_ola
WHERE is_completed = TRUE
GROUP BY payment_method
ORDER BY total_revenue DESC;
"""

TOP_CUSTOMERS = """
SELECT customer_id,
       COUNT(*) AS rides_count,
       SUM(booking_value) AS total_revenue
FROM public.rides_ola
WHERE is_completed = TRUE
GROUP BY customer_id
ORDER BY total_revenue DESC
LIMIT 5;
"""

CANCELLATION_REASONS = """
SELECT customer_reason, driver_reason, COUNT(*) AS cancellation_count
FROM (
    SELECT
        COALESCE(canceled_rides_by_customer) AS customer_reason,
        COALESCE(canceled_rides_by_driver) AS driver_reason
    FROM public.rides_ola
    WHERE is_canceled = TRUE
) AS sub
GROUP BY customer_reason, driver_reason
ORDER BY cancellation_count DESC;
"""

# -----------------------------
# New Queries
# -----------------------------

# 1. Daily Ride Volume (for trend analysis)
DAILY_RIDE_VOLUME = """
SELECT ride_date::date AS date,
       COUNT(*) AS ride_count
FROM public.rides_ola
WHERE is_completed = TRUE
GROUP BY ride_date::date
ORDER BY date;
"""

# 2. Vehicle Type Distribution (total rides per type)
VEHICLE_TYPE_DISTRIBUTION = """
SELECT vehicle_type, COUNT(*) AS total_rides
FROM public.rides_ola
WHERE is_completed = TRUE
GROUP BY vehicle_type
ORDER BY total_rides DESC;
"""

# 3. Average Booking Value per Vehicle Type
AVG_BOOKING_VALUE_BY_VEHICLE = """
SELECT vehicle_type, AVG(booking_value) AS avg_booking_value
FROM public.rides_ola
WHERE is_completed = TRUE
GROUP BY vehicle_type
ORDER BY avg_booking_value DESC;
"""

# 4. Surge Pricing Effectiveness (high vs low booking value rides)
SURGE_PRICING_ANALYSIS = """
SELECT vehicle_type,
       COUNT(*) FILTER (WHERE booking_value > 200) AS high_value_rides,
       COUNT(*) FILTER (WHERE booking_value <= 200) AS normal_value_rides
FROM public.rides_ola
WHERE is_completed = TRUE
GROUP BY vehicle_type
ORDER BY vehicle_type;
"""

# 5. Customer Rating Distribution (for identifying unhappy customers)
CUSTOMER_RATING_DISTRIBUTION = """
SELECT customer_rating, COUNT(*) AS rating_count
FROM public.rides_ola
WHERE is_completed = TRUE
GROUP BY customer_rating
ORDER BY customer_rating;
"""

# 6. Driver Rating Distribution
DRIVER_RATING_DISTRIBUTION = """
SELECT driver_ratings AS driver_rating, COUNT(*) AS rating_count
FROM public.rides_ola
WHERE is_completed = TRUE
GROUP BY driver_ratings
ORDER BY driver_ratings;
"""

# 7. Top Pickup Locations (to identify demand hotspots)
TOP_PICKUP_LOCATIONS = """
SELECT pickup_location, COUNT(*) AS total_rides
FROM public.rides_ola
WHERE is_completed = TRUE
GROUP BY pickup_location
ORDER BY total_rides DESC
LIMIT 10;
"""

# 8. Average Ride Distance by Vehicle Type
AVG_RIDE_DISTANCE_BY_VEHICLE = """
SELECT vehicle_type, AVG(ride_distance) AS avg_distance
FROM public.rides_ola
WHERE is_completed = TRUE
GROUP BY vehicle_type
ORDER BY avg_distance DESC;
"""

# 9. Cancellation Rate by Vehicle Type
CANCELLATION_BY_VEHICLE = """
SELECT vehicle_type,
       COUNT(*) FILTER (WHERE is_canceled = TRUE) AS canceled_rides,
       COUNT(*) AS total_rides,
       ROUND(100.0 * COUNT(*) FILTER (WHERE is_canceled = TRUE)/COUNT(*),2) AS cancellation_rate
FROM public.rides_ola
GROUP BY vehicle_type
ORDER BY cancellation_rate DESC;
"""

# 10. Anomaly Detection (rides with unusually high booking value)
HIGH_VALUE_RIDES = """
SELECT booking_id, customer_id, vehicle_type, booking_value, ride_date
FROM public.rides_ola
WHERE booking_value > 500
ORDER BY booking_value DESC
LIMIT 20;
"""
