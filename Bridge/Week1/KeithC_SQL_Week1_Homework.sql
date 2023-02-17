-- Q#1
SELECT 
	dest,
    distance
FROM flights
WHERE distance = (SELECT MAX(distance) FROM flights);
-- Answer: HNL is the farthest destination

-- Q#2
SELECT DISTINCT engines FROM planes;

SELECT 
    engines,
    MAX(seats)
FROM planes
GROUP BY engines
ORDER BY engines;

SELECT manufacturer, model, seats, engines
FROM planes
WHERE 
	engines = 1 AND seats = (SELECT MAX(seats) FROM planes WHERE engines = 1) OR
    engines = 2 AND seats = (SELECT MAX(seats) FROM planes WHERE engines = 2) OR
    engines = 3 AND seats = (SELECT MAX(seats) FROM planes WHERE engines = 3) OR
    engines = 4 AND seats = (SELECT MAX(seats) FROM planes WHERE engines = 4)
ORDER BY engines;
-- Answer: Planes can have 1, 2, 3 or 4 engines, with max seating of 16, 400, 379 and 450, respectively.
-- 		Multiple aircraft models are tied for most seats within each engine category.

-- Q#3
SELECT COUNT(*) FROM flights;
-- 

-- Q#4
SELECT carrier, COUNT(flight) 
FROM flights 
GROUP BY carrier
ORDER BY COUNT(flight) DESC;
-- 

-- Q#5
SELECT airlines.name, COUNT(flights.flight) 
FROM airlines 
	LEFT JOIN flights	
	ON airlines.carrier = flights.carrier
GROUP BY airlines.carrier
ORDER BY COUNT(flights.flight) DESC;
-- 

-- Q#6
SELECT airlines.name, COUNT(flights.flight) 
FROM airlines 
	LEFT JOIN flights	
	ON airlines.carrier = flights.carrier
GROUP BY airlines.carrier
ORDER BY COUNT(flights.flight) DESC
LIMIT 5;
-- 

-- Q#7
SELECT airlines.name, COUNT(long_flights.flight) AS flight_count
FROM airlines
	LEFT JOIN (SELECT * FROM flights WHERE distance >= 1000) AS long_flights
	ON airlines.carrier = long_flights.carrier
GROUP BY airlines.carrier
ORDER BY flight_count DESC
LIMIT 5;
-- 

-- Q#8
-- Question: Which plane models have the most flights? And which carriers operate those flights?
SELECT 
    planes.manufacturer,
    planes.model,
    airlines.name,
    COUNT(flights.flight) AS flight_count
FROM flights
	LEFT JOIN airlines
	ON airlines.carrier = flights.carrier
    LEFT JOIN planes
	ON planes.tailnum = flights.tailnum
WHERE planes.model IS NOT NULL
GROUP BY planes.manufacturer, planes.model, airlines.name
ORDER BY flight_count DESC
LIMIT 10;
-- Airbus' A320-232 model has the most flightsat 118, split between JetBlue and United.