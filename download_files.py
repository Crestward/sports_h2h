import requests
import os

# Starting year
# year = 2324
comp = 'league2'

year1 = 23
year2 = 24

hold1 = 100
hold2 = 100

i = 30

print('Started')
# Loop through years from 2324 to 9394
while i  >= 0:
    # Construct URL
    if year1 < 0:
        year1 = hold1
        hold1 -= 1
    
    if year2 < 0:
        year2 = hold2
        hold2 -= 1

    if year1 >= 0 and year1 < 10:
        year1 = "0" + str(year1)

    if year2 >= 0 and year2 < 10:
        year2 = "0" + str(year2)

    year = str(year1) + str(year2)
    url = f"https://football-data.co.uk/mmz4281/{year}/E3.csv"
    
    # Download CSV file
    response = requests.get(url)
    if response.status_code == 200:
        # Save CSV file
        with open(f"data/{comp}/{comp}_league_{year}.csv", "wb") as f:
            f.write(response.content)
            
        print(f"Downloaded and saved {comp}_league_{year}.csv")
        
        # # Rename file
        # os.rename(f"{comp}_league_{year}.csv", f"{comp}_league_{year}.csv")
        # print(f"Renamed file to {comp}_league_{year}.csv")
        
        # Decrement year for the next iteration
        year1 = int(year1)
        year2 = int(year2)
        
        year1 -= 1
        year2 -= 1

        if int(year1) < 0:
            hold1 -= 1
        
        if int(year2) < 0:
            hold2 -= 1
        i -= 1
    else:
        print(f"Failed to download data for year {year}")

        if year1 < 0:
            hold1 -= 1
        
        if year2 < 0:
            hold2 -= 1
        
    # Update year for the next iteration
        year1 -= 1
        year2 -= 1
        i -= 1



# import csv
# from dateutil import parser
# from collections import Counter

# def load_data(file_path):
#     data = []
#     with open(file_path, 'r') as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             row = {k: safe_int(v) if k in ['FTHG', 'FTAG', 'HTHG', 'HTAG', 'HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR'] else v for k, v in row.items()}
#             data.append(row)
#     return data

# def get_team_names(data):
#     team_names = set()
#     for match in data:
#         team_names.add(match['HomeTeam'])
#         team_names.add(match['AwayTeam'])
#     return sorted(team_names)

# def get_h2h_details(data, team1, team2):
#     team1_wins = team2_wins = draws = 0
#     matches = []
#     for match in data:
#         if match['HomeTeam'] == team1 and match['AwayTeam'] == team2:
#             if match['FTR'] == 'H':
#                 team1_wins += 1
#             elif match['FTR'] == 'A':
#                 team2_wins += 1
#             else:
#                 draws += 1
#             matches.append(match)
#         elif match['HomeTeam'] == team2 and match['AwayTeam'] == team1:
#             if match['FTR'] == 'H':
#                 team2_wins += 1
#             elif match['FTR'] == 'A':
#                 team1_wins += 1
#             else:
#                 draws += 1
#             matches.append(match)
#     matches = sorted(matches, key=lambda x: parser.parse(x['Date'], fuzzy=True), reverse=True)
#     return team1_wins, team2_wins, draws, matches

# def safe_int(value):
#     try:
#         return int(value)
#     except ValueError:
#         return 0

# def calculate_overview_stats(team1, team2, team1_wins, team2_wins, draws, matches):
#     # ... (existing code for calculating statistics)

# def main():
#     file_path = input("Enter the file path (default: 'merged_data.csv'): ") or 'merged_data.csv'
#     data = load_data(file_path)
#     team_names = get_team_names(data)
#     print("Available teams:")
#     for team in team_names:
#         print(team)

#     team1 = input(f"Enter team 1 ({team_names[0]}): ") or team_names[0]
#     team2 = input(f"Enter team 2 ({team_names[1]}): ") or team_names[1]

#     team1_wins, team2_wins, draws, matches = get_h2h_details(data, team1, team2)

#     team1_stats = calculate_overview_stats(team1, team2, team1_wins, team2_wins, draws, matches)
#     team2_stats = calculate_overview_stats(team2, team1, team2_wins, team1_wins, draws, matches)

#     # Print the calculated statistics
#     print(f"Statistics for {team1}:")
#     for stat, value in team1_stats.items():
#         print(f"{stat}: {value}")

#     print(f"\nStatistics for {team2}:")
#     for stat, value in team2_stats.items():
#         print(f"{stat}: {value}")

# if __name__ == "__main__":
#     main()