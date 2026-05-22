/* Creating postal code  'buckets' for later visualizations
* using the ev_washington (main) table and the locations table
*/

WITH postal_code_buckets AS (
  SELECT 
    l.postal_code AS postal_code,
    COUNT(*) AS ev_count
  FROM ev_washington ew
  JOIN locations l
    ON ew.location_id = l.id
  GROUP BY l.postal_code
)

SELECT *
  FROM postal_code_buckets
  ORDER BY ev_count DESC;
