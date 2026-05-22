PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;
/* Script for populating the dataset
*
*/

-- Inserting unique postal code locations from the main table ev_washington
-- into our locations table 
INSERT OR IGNORE INTO locations(postal_code, county, city, state)
  SELECT 
    ev.postal_code,
    ev.county,
    ev.city,
    ev.state
  FROM ev_washington ev
  WHERE ev.postal_code IS NOT NULL;

-- Inserting the raw vehicle coordinate text from the main table ev_washington
-- into our coordinates table 
--
-- Filtering out the null and '' coordinates 
INSERT INTO coordinates(coordinate_text_01)
  SELECT DISTINCT 
   ev_washington.coordinate 
  FROM ev_washington 
  WHERE ev_washington.coordinate IS NOT NULL 
    AND ev_washington.coordinate != '';

-- The raw coordinate text has the following form: 
-- "POINT (longitude latitude)" 
-- Inserting into coordinates.coordinate_text_02 the raw coordinate tex 
-- minus the "POINT (" and ")" so that we are left with "longitude latitude"

UPDATE coordinates
	SET coordinate_text_02 =
	    REPLACE(
	        REPLACE(coordinate_text_01, 'POINT (', ''),
	        ')',
	        '');

-- Populating coordinates.longitude from coordinates.coordinate_text_02 
UPDATE coordinates
  SET longitude = 
      CAST(
        SUBSTR(coordinate_text_02, 
               1, 
               INSTR(coordinate_text_02, ' ') - 1)
         AS REAL); 
 
-- Populating coordinates.longitude from coordinates.coordinate_text_02 
UPDATE coordinates
  SET latitude = 
      CAST(
        SUBSTR(coordinate_text_02, 
               INSTR(coordinate_text_02, ' ') + 1) 
              
         AS REAL); 

-- Setting rows with blank coordinates in the original data NULL
UPDATE coordinates 
  SET longitude = NULL,
      latitude = NULL
  WHERE coordinate_text_01 = ''
    OR coordinate_text_01 IS NULL;

-- Populating spatial_index table with the id, longitude, latitude from 
-- the coordinates table
--
-- Note: In our spatial_index table, we want minX = maxX = longitude and 
-- minY = maxY = latitude 

INSERT INTO spatial_index(id, minX, maxX, minY, maxY)
  SELECT 
    c.id,
    c.longitude,
    c.longitude,
    c.latitude,
    c.latitude
  FROM coordinates c
  WHERE longitude IS NOT NULL 
    AND latitude is NOT NULL;

/* Updating ev_washington.coordinate_id = coordinates.id 
 * where ev_washington.vehicle_coordinates = coordinates.raw_coordinate_text
 */
 
UPDATE ev_washington
  SET coordinate_id = (
    SELECT c.id 
    FROM coordinates c 
    WHERE ev_washington.coordinate = c.coordinate_text_01
);

-- Nulling out ev_washington.coordinates_id where 
-- ev_washington.coordinate = ''

UPDATE ev_washington
  SET coordinate = NULL 
  WHERE ev_washington.coordinate = '';

/* Updating ev_washington.location_id = locations.id 
* where the postal_code, city, county, state match 
*/

UPDATE ev_washington
SET location_id = (
    SELECT l.id
    FROM locations l
    WHERE ev_washington.postal_code = l.postal_code
      AND ev_washington.county = l.county
      AND ev_washington.city = l.city
      AND ev_washington.state = l.state
);

-- Dropping ev_washington postal_code, city, county, state columns 
ALTER TABLE ev_washington
  DROP COLUMN postal_code;

ALTER TABLE ev_washington
  DROP COLUMN county;

ALTER TABLE ev_washington
  DROP COLUMN city;

ALTER TABLE ev_washington
  DROP COLUMN state;

-- Dropping coordinate text in ev_washington 
ALTER TABLE ev_washington
  DROP COLUMN coordinate;


COMMIT;
