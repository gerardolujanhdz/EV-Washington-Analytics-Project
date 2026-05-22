-- Basic Exploration Queries

-- Most Common EV Make sorted 
SELECT 
  make,
  COUNT(make) AS total
FROM ev_washington
GROUP BY make
ORDER BY count DESC;

-- Most Common EV model sorted 
SELECT 
  make, 
  model,
  COUNT(*) as count 
FROM ev_washington
GROUP BY 
  make,
  model 
ORDER BY count DESC;

-- Most EVs by county sorted 
SELECT 
  county,
  COUNT(county) as count 
FROM ev_washington
GROUP BY county 
ORDER BY count DESC;

-- Most EVs by city sorted 
SELECT 
  city,
  COUNT(city) as count 
FROM ev_washington
GROUP BY city 
ORDER BY count DESC;

-- EV type breakdown
SELECT 
  ev_type,
  COUNT(ev_type) AS total 
FROM ev_washington
GROUP BY ev_type;


