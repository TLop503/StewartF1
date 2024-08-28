import requests
from src.dc import Driver

# index = round from spreadsheet
def fetch_and_build(idx):
    idx = int(idx * 15)

    # endpoint
    url = f"https://api.jolpi.ca/ergast/f1/2024/results/?offset={idx}"

    res = requests.get(url)
    if res.status_code == 200:
        race_data = res.json()
        races = race_data['MRData']['RaceTable']['Races']
        race_results_list = []

        for race in races:
            print (race['raceName'])
            for result in race['Results']:
                driver = result['Driver']
                instance = Driver(
                    name=f"{driver['givenName']} {driver['familyName']}",
                    position=int(result['position']),
                    laps=int(result['laps']),
                    points=int(result['points'])
                )
            
                race_results_list.append(instance)
                if len(race_results_list) >= 20:
                    #sort by family name
                    race_results_list.sort(key=lambda d: d.name.split()[-1])
                    return race_results_list[:20]
        
        # If less than 20 drivers are returned, fill the remaining slots with None or handle as needed
        race_results_list.sort(key=lambda d: d.name.split()[-1])
        return race_results_list[:20]