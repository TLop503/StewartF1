def pretty_print(race, results):
    # Results for Place GP (yyyy-mm-dd)
    print(f"Results for {race['raceName']} ({race['date']}):")
    # Winner: Joe Schmo
    print(f"Winner: {results[0]['Driver']['givenName']} {results[0]['Driver']['familyName']}")
    print("+--------+--------+------+-------+")
    print("| Driver | Points | Laps | Delta |")

    for entry in results:
        code = entry['Driver']['code']
        pts = 2 * int(entry['points'])
        pts = str(pts)
        if len(pts) == 1:
            pts = "0" + pts
        laps = entry['laps']
        if len(laps) == 1:
            laps = "0" + laps

        # Parse Position Points
        pos = str( int(entry['grid']) - int(entry['position']))
        if len(pos) == 1:
            pos = "0" + pos

        print(f"| {code}    | {pts}     | {laps}   | {pos}    |")

    print("+--------+--------+------+-------+")


def sql_to_file(out_file, race_sql, driver_results_sql):
    with open(out_file, "w") as f:
        f.write("-- SQL for inserting race\n")
        f.write(race_sql)
        f.write("\n-- SQL for inserting driver results\n")
        f.writelines(driver_results_sql)

    print(f"SQL queries have been written to {out_file} for manual inspection.")