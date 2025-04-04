import requests

def fetch():
    url = "https://api.jolpi.ca/ergast/f1/2025/last/results/"

    res = requests.get(url)
    if not (res.status_code == 200):
        print(f"Request failed with code {res.status_code}")
        return 0, 0
    
    data = res.json()
    # only should have 1 race in []
    race = data['MRData']['RaceTable']['Races'][0]
    results = race['Results']
    
    # Remove debug printing for cleaner output
    # print("DEBUG:")
    # print(race)
    # print("results:")
    # print(results)

    return race, results
