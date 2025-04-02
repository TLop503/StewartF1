import datetime

def generate_race_sql(race):
    """
    Generate SQL to insert a race weekend and race record
    """
    # Extract race info
    race_name = race['raceName']
    circuit_name = race['Circuit']['circuitName']
    circuit_location = race['Circuit']['Location']['country']
    race_date = race['date']
    
    # Round number is used as weekend_id
    weekend_id = race['round']
    
    # Create SQL for race weekend (if not exists)
    race_weekend_sql = f"""
INSERT INTO RaceWeekends (weekend_id, race_name, circuit_name, circuit_location, has_sprint)
SELECT {weekend_id}, '{race_name}', '{circuit_name}', '{circuit_location}', False
WHERE NOT EXISTS (SELECT 1 FROM RaceWeekends WHERE weekend_id = {weekend_id});
"""
    
    # Create SQL for race - now with a check to prevent duplicates
    race_sql = f"""
INSERT INTO Races (weekend_id, race_type, race_date, event_status)
SELECT {weekend_id}, 'GRAND_PRIX', '{race_date}', 'COMPLETED'
WHERE NOT EXISTS (
    SELECT 1 FROM Races 
    WHERE weekend_id = {weekend_id} 
    AND race_type = 'GRAND_PRIX' 
    AND race_date = '{race_date}'
);

-- Get the race_id for driver results
SET @race_id = LAST_INSERT_ID();
-- If no insert happened (race already existed), get the existing race_id
IF @race_id = 0 THEN
    SET @race_id = (SELECT race_id FROM Races WHERE weekend_id = {weekend_id} AND race_type = 'GRAND_PRIX' AND race_date = '{race_date}' LIMIT 1);
END IF;
"""
    
    return race_weekend_sql + race_sql

def generate_driver_results_sql(results, race_id="@race_id"):
    """
    Generate SQL to insert driver results
    """
    driver_results_sql = []
    
    for entry in results:
        driver_code = entry['Driver']['code']
        driver_firstname = entry['Driver']['givenName'].replace("'", "''")
        driver_lastname = entry['Driver']['familyName'].replace("'", "''")
        driver_number = entry['number']
        
        # Constructor is the actual F1 team, not fantasy team
        constructor = entry['Constructor']['name']
        
        # Position data
        starting_pos = entry['grid']
        finishing_pos = entry['position']
        fia_points = entry['points']
        
        # Status can be 'Finished', 'Retired', 'Disqualified', etc.
        status = entry['status']
        dns = "TRUE" if status == "DNS" else "FALSE"
        dnf = "TRUE" if status in ["Retired", "Accident"] else "FALSE"
        
        # Laps can be missing if DNS
        laps = entry.get('laps', '0')
        
        # Insert driver if not exists
        driver_sql = f"""
-- Ensure driver exists
INSERT INTO Drivers (first_name, last_name, car_number, irl_affiliation)
SELECT '{driver_firstname}', '{driver_lastname}', {driver_number}, '{constructor}'
WHERE NOT EXISTS (
    SELECT 1 FROM Drivers 
    WHERE first_name = '{driver_firstname}' AND last_name = '{driver_lastname}'
);

-- Get driver_id for results
SET @driver_id = (SELECT driver_id FROM Drivers WHERE first_name = '{driver_firstname}' AND last_name = '{driver_lastname}' LIMIT 1);
"""
        
        # Insert driver result - now with a check to prevent duplicates
        result_sql = f"""
INSERT INTO DriverResults (race_id, driver_id, starting_position, finishing_position, fia_points, laps_completed, dns, dnf, notes)
SELECT {race_id}, @driver_id, {starting_pos}, {finishing_pos}, {fia_points}, {laps}, {dns}, {dnf}, '{status}'
WHERE NOT EXISTS (
    SELECT 1 FROM DriverResults 
    WHERE race_id = {race_id} 
    AND driver_id = @driver_id
);
"""
        
        driver_results_sql.append(driver_sql + result_sql)
    
    return driver_results_sql

def prepare_sql_for_race(race, results):
    """
    Generate complete SQL for inserting race and all results
    """
    race_sql = generate_race_sql(race)
    driver_results_sql = generate_driver_results_sql(results)
    
    return race_sql, driver_results_sql
