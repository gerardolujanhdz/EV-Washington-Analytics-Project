
-- Creating indexes for foreign keys to speed up joins 
--

-- Population table indexes
CREATE INDEX idx_population_location_id 
  ON population(location_id);

CREATE INDEX idx_population_coordinate_id 
  ON population(coordinate_id);

CREATE INDEX idx_population_vehicle_id 
  ON population(vehicle_id);

-- Registration table indexes
CREATE INDEX idx_registration_location_id 
  ON registration(location_id);

CREATE INDEX idx_registration_vehicle_id 
  ON registration(vehicle_id);

CREATE INDEX idx_registration_compliance_id 
  ON registration(compliance_id);


