import src.build_class
import src.parse_to_csv

def main():
    index = int(input("Enter index number (count sprints as well): "))
    
    # Fetch and build the list of Driver instances
    drivers = src.build_class.fetch_and_build(index)
    
    # Parse the list to CSV formatted string
    csv_data = src.parse_to_csv.parse_to_csv(drivers)
    
    # Print or save the CSV data
    print(csv_data)

if __name__ == "__main__":
    main()
