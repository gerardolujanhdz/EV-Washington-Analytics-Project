-- Creating a table to house all coordinates + coordinate id +
-- postal_code + 


WITH coordinate_postal_codes AS (
  SELECT
      c.id,
      c.latitude,
      c.longitude,
      l.postal_code,
      l.county
  FROM ev_washington ew
  JOIN coordinates c
    ON ew.coordinate_id = c.id
  JOIN locations l
    ON ew.location_id = l.id
  WHERE l.state = 'WA'
)
-- Just checking Counts 
SELECT COUNT(*)
FROM coordinate_postal_codes;
