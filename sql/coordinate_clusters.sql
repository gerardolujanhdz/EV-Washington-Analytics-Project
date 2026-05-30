-- Creating a table to house all coordinates + coordinate id


WITH coordinate_joined AS (
  SELECT
      c.coordinate_id,
      c.latitude,
      c.longitude,
      l.region
  FROM population p 
  JOIN coordinates c
    ON p.coordinate_id = c.coordinate_id
  JOIN locations l
    ON population.location_id = l.location_id
  WHERE l.state = 'WA'
)
-- Just checking Counts 
SELECT COUNT(*)
FROM coordinate_joined;
