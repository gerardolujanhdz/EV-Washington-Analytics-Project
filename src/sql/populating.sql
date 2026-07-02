PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;
/* Script for populating the dataset
*
*/

-- Inserting unique locations from the two "facts" tables, population and registration, 
-- into our locations table 
INSERT OR IGNORE INTO locations(postal_code, county, city, state, legislative_district, census_tract_2020)
  SELECT 
    postal_code,
    county,
    city,
    state,
    legislative_district,
    census_tract_2020
  FROM registration
  WHERE registration.postal_code IS NOT NULL;

INSERT OR IGNORE INTO locations(postal_code, county, city, state,legislative_district, census_tract_2020)
  SELECT 
    postal_code,
    county,
    city,
    state,
    legislative_district,
    census_tract_2020
  FROM population
  WHERE population.postal_code IS NOT NULL;

-- Updating location_id column in population and registration tables from 
-- the locations table 

UPDATE population
SET location_id = (
    SELECT l.location_id
    FROM locations l
    WHERE population.postal_code = l.postal_code
      AND population.county = l.county
      AND population.city = l.city
      AND population.state = l.state
      AND population.legislative_district = l.legislative_district
      AND population.census_tract_2020 = l.census_tract_2020
);

UPDATE registration 
SET location_id = (
    SELECT l.location_id
    FROM locations l
    WHERE registration.postal_code = l.postal_code
      AND registration.county = l.county
      AND registration.city = l.city
      AND registration.state = l.state
      AND registration.legislative_district = l.legislative_district
      AND registration.census_tract_2020 = l.census_tract_2020
);

-- Populating Region column in locations table 
INSERT INTO regions(county,region)
VALUES 
  ('San Juan', 'Northwest'),
  ('Kitsap', 'Peninsulas'),
  ('Clallam', 'Peninsulas'),
  ('Jefferson', 'Peninsulas'),
  ('Grays Harbor', 'Peninsulas'),
  ('Mason', 'Peninsulas'),
  ('Pacific', 'Southwest'),
  ('Thurston', 'Metro Puget Sound'),
  ('Lewis', 'Southwest'),
  ('Wahkiakum', 'Southwest'),
  ('Cowlitz', 'Southwest'),
  ('Clark', 'Southwest'),
  ('Skamania', 'Southwest'),
  ('Pierce', 'Metro Puget Sound'),
  ('King', 'Metro Puget Sound'),
  ('Snohomish', 'Metro Puget Sound'),
  ('Skagit', 'Northwest'),
  ('Whatcom', 'Northwest'),
  ('Okanogan', 'North Central'),
  ('Chelan', 'North Central'),
  ('Douglas', 'North Central'),
  ('Kittitas', 'North Central'),
  ('Yakima', 'Wine Country'),
  ('Klickitat', 'Wine Country'),
  ('Grant', 'North Central'),
  ('Benton', 'Wine Country'),
  ('Ferry','Eastern'),
  ('Stevens','Eastern'),
  ('Pend Oreille','Eastern'),
  ('Lincoln','Eastern'),
  ('Spokane','Eastern'),
  ('Adams','Eastern'),
  ('Franklin','Wine Country'),
  ('Walla Walla','Wine Country'),
  ('Columbia','Wine Country'),
  ('Garfield','Wine Country'),
  ('Asotin','Wine Country'),
  ('Whitman','Eastern'),
  ('Island','Northwest');

-- Updating locations table region based on region table values 
UPDATE locations
  SET region = (
    SELECT regions.region
    FROM regions 
    WHERE locations.county = regions.county
);

-- Dropping now unneeded regions table 
DROP TABLE regions;

-- Dropping postal_code, county, city, state, legislative_district and census columns 
--  from the fact tables population and registration


ALTER TABLE population 
  DROP COLUMN postal_code;
ALTER TABLE population 
  DROP COLUMN county;
ALTER TABLE population 
  DROP COLUMN city;
ALTER TABLE population 
  DROP COLUMN state;
ALTER TABLE population
  DROP COLUMN legislative_district;
ALTER TABLE population 
  DROP COLUMN census_tract_2020;

ALTER TABLE registration 
  DROP COLUMN postal_code;
ALTER TABLE registration 
  DROP COLUMN county;
ALTER TABLE registration 
  DROP COLUMN city;
ALTER TABLE registration 
  DROP COLUMN state;
ALTER TABLE registration
  DROP COLUMN legislative_district;
ALTER TABLE registration 
  DROP COLUMN census_tract_2020;



-- Inserting the raw vehicle coordinate text from the main table ev_washington
-- into our coordinates table 
--
-- Filtering out the null and '' coordinates 
INSERT INTO coordinates(coordinate_text_01)
  SELECT DISTINCT 
   population.coordinate 
  FROM population
  WHERE population.coordinate IS NOT NULL 
    AND population.coordinate != '';

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

/* Updating population.coordinate_id = coordinates.id 
 * where population.vehicle_coordinates = coordinates.coordinate_text_01
 */
 
UPDATE population 
  SET coordinate_id = (
    SELECT c.coordinate_id 
    FROM coordinates c 
    WHERE population.coordinate = c.coordinate_text_01
);

-- Nulling out population.coordinates_id where 
-- population.coordinate = ''

UPDATE population 
  SET coordinate_id = NULL 
  WHERE population.coordinate = '';

-- Dropping coordinate text in ev_washington 
ALTER TABLE population DROP COLUMN coordinate;

-- Dropping coordinate_text_01 and coordinate_text_02 from coordinates table 
ALTER TABLE coordinates DROP COLUMN coordinate_text_01;

ALTER TABLE coordinates DROP COLUMN coordinate_text_02;

-- Populating vehicles table from the population and registration tables 

INSERT OR IGNORE INTO vehicles(vin, make, model, model_year, ev_type)
  SElECT
    vin, 
    make,
    model,
    model_year,
    ev_type 
  FROM registration 
  WHERE registration.vin IS NOT NULL;

INSERT OR IGNORE INTO vehicles(vin, make, model, model_year, ev_type)
  SElECT
    vin, 
    make,
    model,
    model_year,
    ev_type 
  FROM population 
  WHERE population.vin IS NOT NULL;

-- Updating vehicle_id column in population and registration tables from 
-- the vehicles table 

UPDATE population
SET vehicle_id = (
    SELECT v.vehicle_id
    FROM vehicles v
    WHERE population.vin = v.vin
      AND population.make = v.make
      AND population.model = v.model
      AND population.model_year = v.model_year
      AND population.ev_type = v.ev_type
);

UPDATE registration
SET vehicle_id = (
    SELECT v.vehicle_id
    FROM vehicles v
    WHERE registration.vin = v.vin
      AND registration.make = v.make
      AND registration.model = v.model
      AND registration.model_year = v.model_year
      AND registration.ev_type = v.ev_type
);


-- Dropping vin, make, model, model_year, ev_type columns from facts tables 
ALTER TABLE registration DROP COLUMN vin;
ALTER TABLE registration DROP COLUMN make;
ALTER TABLE registration DROP COLUMN model;
ALTER TABLE registration DROP COLUMN model_year;
ALTER TABLE registration DROP COLUMN ev_type;

ALTER TABLE population DROP COLUMN vin;
ALTER TABLE population DROP COLUMN make;
ALTER TABLE population DROP COLUMN model;
ALTER TABLE population DROP COLUMN model_year;
ALTER TABLE population DROP COLUMN ev_type;

-- Populating hb2042_compliance table from registration table

INSERT OR IGNORE INTO hb2042_compliance(
  meets_range_req, 
  range_req_reason, 
  meets_sale_date_req, 
  sale_date_req_reason,
  meets_sale_price_req,
  sale_price_req_reason)

  SELECT 
    meets_hb2042_range_requirement,
    hb2042_range_requirement_reason,
    meets_hb2042_sale_date_requirement,
    hb2042_purchase_date_requirement_reason,
    meets_hb2042_sale_price_requirement,
    hb2042_sale_price_requirement_reason
  FROM registration;


-- Updating compliance_id column in registration tables from 
-- the hb2042_compliance table 

UPDATE registration
SET compliance_id = (
    SELECT c.compliance_id
    FROM hb2042_compliance c
    WHERE 
      registration.meets_hb2042_range_requirement = c.meets_range_req AND
      registration.hb2042_range_requirement_reason = c.range_req_reason AND
      registration.meets_hb2042_sale_date_requirement = c.meets_sale_date_req AND 
      registration.hb2042_purchase_date_requirement_reason = c.sale_date_req_reason AND 
      registration.meets_hb2042_sale_price_requirement = c.meets_sale_price_req AND 
      registration.hb2042_sale_price_requirement_reason = c.sale_price_req_reason
);

-- Dropping meets_range_req, range_req_reason, meets_sale_date_req,
-- sale_date_req_reason, meets_sale_price_req, sale_price_req_reason from registration
ALTER TABLE registration
  DROP COLUMN meets_hb2042_range_requirement;
ALTER TABLE registration 
  DROP COLUMN hb2042_range_requirement_reason;
ALTER TABLE registration
  DROP COLUMN meets_hb2042_sale_date_requirement;
ALTER TABLE registration 
  DROP COLUMN hb2042_purchase_date_requirement_reason;
ALTER TABLE registration
  DROP COLUMN meets_hb2042_sale_price_requirement;
ALTER TABLE registration
  DROP COLUMN hb2042_sale_price_requirement_reason;

COMMIT;
