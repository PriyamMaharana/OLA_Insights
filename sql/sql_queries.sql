-----------------------------
--- SQL Queries Analytics ---
-----------------------------

--Q1: Retrieve all successful bookings
create view successfull_bookings as
select * from rides_ola
WHERE booking_status = 'Success';

select * from successfull_bookings;


--Q2: Find the average ride distance for each vehicle type
create view avg_ride_distance_each_vehicle as
select vehicle_type, trunc(avg(ride_distance)::numeric,1) as avg_ride_km
from rides_ola
group by vehicle_type;

select * from avg_ride_distance_each_vehicle;


--Q3: Get the total number of cancelled rides by customers
create view total_ride_cancelled_by_customer as
select count(*) as ride_cancelled_by_customer
from rides_ola
where booking_status = 'Canceled By Customer';

select * from total_ride_cancelled_by_customer;


--Q4: List the top 5 customers who booked the highest number of rides
create view top_5_customers as
select customer_id, count(booking_id) as total_rides
from rides_ola
group by customer_id order by total_rides
desc limit 5;

select * from top_5_customers;


--Q5: Get the number of rides cancelled by drivers due to personal and car-related issues
create view rides_cancelled_by_driver as
select count(*) as total_ride_cancelled from rides_ola
where canceled_rides_by_driver = 'Personal & Car related issue';

select * from rides_cancelled_by_driver;


--Q6: Find the maximum and minimum driver ratings for Prime Sedan bookings
create view driver_rating_for_prime_sedan as
select max(driver_ratings) as max_rating, min(driver_ratings) as min_rating
from rides_ola
where vehicle_type = 'Prime Sedan';

select * from driver_rating_for_prime_sedan;

--Q7: Retrieve all rides where payment was made using UPI
create view upi_payments as
select * from rides_ola
where payment_method = 'Upi';

select * from upi_payments;


--Q8: Find the average customer rating per vehicle type
create view avg_customer_ratings_per_vehicle as
select vehicle_type, trunc(avg(customer_rating)::numeric, 1) as avg_customer_rating
from rides_ola
group by vehicle_type;

select * from avg_customer_ratings_per_vehicle;


--Q9: Calculate the total booking value of rides completed successfully
create view total_booking_value as
select sum(booking_value) as total_rides_value
from rides_ola
where booking_status = 'Success';

select * from total_booking_value;


--Q10: List all incomplete rides along with the reason
create view incomplete_ride_reason as
select booking_id, incomplete_rides_reason
from rides_ola
where incomplete_rides = 'Yes';

select * from incomplete_ride_reason;
