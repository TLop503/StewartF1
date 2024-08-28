import requests

# Prompt for user input
index = int(input("Enter index number (count sprints as well): "))
offset = index * 15

# Define the API endpoint
url = f"https://api.jolpi.ca/ergast/f1/2024/results/?offset={offset}"
print(url + "\n\n\n")

# Make the GET request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    race_data = response.json()
    
    # Navigate to the race results
    races = race_data['MRData']['RaceTable']['Races']
    
    # Print race details
    for race in races:
        print(f"Race Name: {race['raceName']}")
        print(f"Date: {race['date']}")
        print(f"Time: {race['time']}")
        print(f"Circuit: {race['Circuit']['circuitName']}, Location: {race['Circuit']['Location']['locality']}, {race['Circuit']['Location']['country']}")
        
        print("Results:")
        for result in race['Results']:
                driver = result['Driver']
                constructor = result['Constructor']
                print(f"Driver: {driver['givenName']} {driver['familyName']}")
                print(f"Position: {result['positionText']}")
                print(f"Points: {result['points']}")
                print(f"Grid: {result['grid']}")
                print(f"Laps: {result['laps']}")
                print(f"Status: {result['status']}")
                if (result['status'] == "Finished"):
                    print(f"Time: {result['Time']['time']}")
                print(f"Fastest Lap: {result['FastestLap']['Time']['time']} (Lap {result['FastestLap']['lap']})")
                print(f"Average Speed: {result['FastestLap']['AverageSpeed']['speed']} {result['FastestLap']['AverageSpeed']['units']}")
                print()
else:
    print(f"Request failed with status code: {response.status_code}")
