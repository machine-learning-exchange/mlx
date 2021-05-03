-- populate_tables.sql
-- 
-- Populate the smaller tables in the schema created by create_tables.sql
--
-- Run with:
--    psql --dbname=demo --file=scripts/populate_tables.sql
-- Larger tables are populated with dedicated scripts after this script runs.

-- Container table contains a list of container IDs.
-- The INSERT statement here just creates a small initial set of containers.
-- The loader script augments this data with a configurable number of 
-- additional rows for extra dummy containers that don't generate 
-- training data.
delete from Container;
insert into Container(id, failure_type) values 
    ('101', 'none'),
    ('102', 'none'),
    ('103', 'none'),
    ('104', 'co2'),
    ('105', 'co2'),
    ('106', 'co2'),
    ('107', 'power'),
    ('108', 'power'),
    ('109', 'power'),
    ('110', 'power')
;




