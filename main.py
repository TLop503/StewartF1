import src.fetcher as f
import src.printer as p
import src.parser as parser
import sys
import os

def main():
    # Get the first argument if available
    generate_sql = False
    sql_output_path = "/home/tlop/src/BF1L/queries/latest_race.sql"
    
    # Check if argument is present
    if len(sys.argv) > 1 and sys.argv[1] == "--sql":
        generate_sql = True
        print("SQL generation mode enabled")
        # Check if there's a second argument for output path
        if len(sys.argv) > 2:
            sql_output_path = sys.argv[2]

    print("Fetching most recent results...\n")
    race, results = f.fetch()
    if (race == 0 or results == 0):
        print("Error fetching results!")
        return
    
    # Always print the race results
    p.pretty_print(race, results)
    
    # If SQL generation is enabled, generate and save SQL
    if generate_sql:
        race_sql, driver_results_sql = parser.prepare_sql_for_race(race, results)
        p.sql_to_file(sql_output_path, race_sql, driver_results_sql)
        print(f"SQL has been generated and saved to {sql_output_path}")

if __name__ == "__main__":
    main()
