
-- Basic Exploration Queries

-- Population Table

-- Most Common EV Make sorted 
SELECT 
  v.make,
  COUNT(make) AS total
FROM population
LEFT JOIN vehicles v ON population.vehicle_id = v.vehicle_id 
GROUP BY make
ORDER BY total DESC;

-- Most Common EV model sorted 
SELECT 
  v.make, 
  v.model,
  COUNT(*) as count 
FROM population
LEFT JOIN vehicles v ON population.vehicle_id = v.vehicle_id
GROUP BY 
  v.make,
  v.model 
ORDER BY count DESC;

-- Most EVs by county sorted 
SELECT 
  l.county,
  COUNT(county) as count 
FROM population
LEFT JOIN locations l on population.location_id = l.location_id
GROUP BY county 
ORDER BY count DESC;

-- Most EVs by city sorted 
SELECT 
  l.city,
  COUNT(city) as count 
FROM population
LEFT JOIN locations l ON population.location_id = l.location_id
GROUP BY city 
ORDER BY count DESC;

-- EV type breakdown
SELECT 
  v.ev_type,
  COUNT(ev_type) AS total 
FROM population
LEFT JOIN vehicles v ON population.vehicle_id = v.vehicle_id
GROUP BY ev_type;

-- Most common makes of EV per County
SELECT 
  l.county,
  v.make,
  COUNT(*) as count
FROM population
  LEFT JOIN locations l ON population.location_id = l.location_id
  LEFT JOIN vehicles v ON population.vehicle_id = v.vehicle_id
GROUP BY
  l.county,
  v.make
ORDER BY count DESC

-- Registration Table Queries 
--

-- Number of registrations by year 
SELECT 
 transaction_year,
 COUNT(transaction_year) as count 
FROM registration
GROUP BY transaction_year
ORDER BY count DESC;

-- Registration Transaction Type and Count 
SELECT 
  transaction_type,
  COUNT(transaction_type) as count 
FROM registration 
GROUP BY transaction_type
ORDER BY count DESC;

-- Registration by County
SELECT 
  l.county,
  COUNT(*) AS count 
FROM registration
LEFT JOIN locations l ON registration.location_id = l.location_id 
GROUP BY county
ORDER BY count DESC;

