import csv
import requests
from dateutil import parser
import os

comp = 'premier'
# Download the new data file
url = "https://football-data.co.uk/mmz4281/2324/E0.csv"
response = requests.get(url)
if response.status_code == 200:
    # Save the downloaded file temporarily
    with open(f"data/{comp}/new_data.csv", "wb") as file:
        file.write(response.content)

    # Load the existing merged data
    merged_data = set()
    with open(f"data/{comp}/premier_merged_data.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            match_id = (row["Date"], row["HomeTeam"], row["AwayTeam"])
            merged_data.add(match_id)

    # Load the new data
    new_matches = []
    with open(f"data/{comp}/new_data.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            match_id = (row["Date"], row["HomeTeam"], row["AwayTeam"])
            if match_id not in merged_data:
                new_matches.append(row)
                print(match_id)
                print("Match is new.")
                merged_data.add(match_id)
            else:
                print("Match already exists in merged data.")

    # Append the new matches to the merged data
    if new_matches:
        with open(f"data/{comp}/premier_merged_data.csv", "a", newline="") as file:
            fieldnames = new_matches[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerows(new_matches)
        print(f"{len(new_matches)} new matches appended to merged_data.csv")
    else:
        print("No new matches to append")

    # Delete the temporary new data file
    os.remove(f"data/{comp}/new_data.csv")
else:
    print(f"Failed to download the data file. Error code: {response.status_code}")
