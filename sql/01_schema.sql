
/* Script for creating all the tables 
*
*/

-- Creating table that will be used to import the .csv file
-- Main table 

CREATE TABLE ev_washington(
  id INTEGER PRIMARY KEY,
  vin TEXT,
  location_id INTEGER,
  county TEXT,
  city TEXT,
  state TEXT,
  postal_code INTEGER,
  model_year INTEGER,
  make TEXT,
  model TEXT,
  ev_type TEXT,
  cafv_eligibility TEXT,
  ev_range INTEGER,
  legislative_district INTEGER,
  dol_vehicle_id INTEGER,
  coordinate TEXT,
  coordinate_id INTEGER,
  electric_utility TEXT,
  census_tract_2020 INTEGER,
  FOREIGN KEY(coordinate_id) REFERENCES coordinates(id),
  FOREIGN KEY(location_id) REFERENCES locations(id)
);

-- Table used to house the 
CREATE TABLE locations(
  id INTEGER PRIMARY KEY,
  postal_code INTEGER,
  county TEXT,
  city TEXT,
  state TEXT,
  UNIQUE(postal_code, county, city, state)
);

CREATE TABLE coordinates(
  id INTEGER PRIMARY KEY,
  coordinate_text_01 TEXT,
  coordinate_text_02 TEXT,
  longitude REAL,
  latitude REAL
);

CREATE VIRTUAL TABLE spatial_index USING rtree(
  id, -- Integer primary key
  minX, -- Latitude X coordinate 
  maxX, -- Latitude X coordinate 
  minY, -- Longitude Y coordinate
  maxY -- Longitude Y coordinate
);
