/* Script for creating all the tables
*
*/


-- Trying to follow a star schema database layout
--
-- Creating tables that will be used to import the two .csv files
-- Redundant columns (in facts + dims tables) will be dropped later

CREATE TABLE IF NOT EXISTS population (
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
    utility_id INTEGER,
    vehicle_id INTEGER,
    FOREIGN KEY (coordinate_id) REFERENCES coordinates (coordinate_id),
    FOREIGN KEY (location_id) REFERENCES locations (location_id),
    FOREIGN KEY (vehicle_id) REFERENCES vehicles (vehicle_id),
    UNIQUE (dol_vehicle_id)
);

CREATE INDEX IF NOT EXISTS idx_population_location_id
ON population (location_id);

CREATE INDEX IF NOT EXISTS idx_population_coordinate_id
ON population (coordinate_id);

CREATE INDEX IF NOT EXISTS idx_population_vehicle_id
ON population (vehicle_id);


CREATE TABLE IF NOT EXISTS vehicles (
    vehicle_id INTEGER PRIMARY KEY,
    vin TEXT,
    make TEXT,
    model TEXT,
    model_year INTEGER,
    ev_type TEXT,
    UNIQUE (vin, make, model, model_year, ev_type)
);

CREATE TABLE IF NOT EXISTS locations (
    location_id INTEGER PRIMARY KEY,
    postal_code INTEGER,
    county TEXT,
    city TEXT,
    state TEXT,
    region TEXT,
    legislative_district INTEGER,
    census_tract_2020 INTEGER,
    UNIQUE (
        postal_code,
        county,
        city,
        state,
        legislative_district,
        census_tract_2020
    )
);

CREATE TABLE IF NOT EXISTS regions (
    region_id INTEGER PRIMARY KEY,
    county TEXT,
    region TEXT
);

CREATE TABLE IF NOT EXISTS coordinates (
    coordinate_id INTEGER PRIMARY KEY,
    coordinate_text_01 TEXT,
    coordinate_text_02 TEXT,
    longitude REAL,
    latitude REAL
);

CREATE TABLE IF NOT EXISTS registration (
    id INTEGER PRIMARY KEY,
    vin TEXT,
    dol_vehicle_id INTEGER,
    model_year INTEGER,
    make TEXT,
    model TEXT,
    ev_type TEXT,
    primary_use TEXT,
    used_status TEXT,
    ev_range INTEGER,
    odometer INTEGER,
    odometer_description TEXT,
    sale_price REAL,
    sale_date TEXT,
    transaction_type TEXT,
    transaction_date TEXT,
    transaction_year INTEGER,
    county TEXT,
    city TEXT,
    state TEXT,
    postal_code INTEGER,
    cafv_eligibility TEXT,
    meets_hb2042_range_requirement TEXT,
    meets_hb2042_sale_date_requirement TEXT,
    meets_hb2042_sale_price_requirement TEXT,
    hb2042_range_requirement_reason TEXT,
    hb2042_purchase_date_requirement_reason TEXT,
    hb2042_sale_price_requirement_reason TEXT,
    ev_fee_paid TEXT,
    transportation_electrification_fee_paid TEXT,
    hybrid_vehicle_electrification_fee_paid TEXT,
    census_tract_2020 INTEGER,
    legislative_district INTEGER,
    electric_utility TEXT,
    location_id INTEGER,
    vehicle_id INTEGER,
    compliance_id INTEGER,
    utility_id INTEGER,
    FOREIGN KEY (location_id) REFERENCES locations (location_id),
    FOREIGN KEY (vehicle_id) REFERENCES vehicles (vehicle_id),
    FOREIGN KEY (compliance_id) REFERENCES hb2042_compliance (compliance_id),
    UNIQUE (vin, dol_vehicle_id, transaction_date, transaction_type)
);

CREATE INDEX IF NOT EXISTS idx_registration_location_id
ON registration (location_id);

CREATE INDEX IF NOT EXISTS idx_registration_vehicle_id
ON registration (vehicle_id);

CREATE INDEX IF NOT EXISTS idx_registration_compliance_id
ON registration (compliance_id);

CREATE TABLE IF NOT EXISTS hb2042_compliance (
    compliance_id INTEGER PRIMARY KEY,
    meets_range_req TEXT,
    range_req_reason TEXT,
    meets_sale_date_req TEXT,
    sale_date_req_reason TEXT,
    meets_sale_price_req TEXT,
    sale_price_req_reason TEXT,
    UNIQUE (
        meets_range_req,
        range_req_reason,
        meets_sale_date_req,
        sale_date_req_reason,
        meets_sale_price_req,
        sale_price_req_reason
    )
);

CREATE TABLE IF NOT EXISTS region_geometric_medians (
    region TEXT PRIMARY KEY,
    latitude TEXT,
    longitude TEXT,
    UNIQUE (region)
);

CREATE TABLE IF NOT EXISTS county_populations (
    county TEXT PRIMARY KEY,
    population INT,
    UNIQUE (county)
);
