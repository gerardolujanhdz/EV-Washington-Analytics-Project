
-- Creating indexes for foreign keys to speed up joins 
--

CREATE INDEX idx_ev_location_id 
  ON ev_washington(location_id);

CREATE INDEX idx_ev_coordinate_id 
  ON ev_washington(coordinate_id);




