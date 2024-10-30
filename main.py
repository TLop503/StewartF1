import src.fetcher as f
import src.printer as p

def main():
    print("Fetching most recent results...\n")
    race, results = f.fetch()
    if (race == 0 or results == 0):
        print("Error fetching results!")
        return
    
    # TODO: add dataclass for staging once db is live
    p.pretty_print(race, results)



if __name__ == "__main__":
    main()
