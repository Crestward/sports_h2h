import csv
from dateutil import parser
from collections import Counter

data = []

# Function to load the data

def load_data(comp):
    data = []
    with open(f'data/{comp}/{comp}_merged_data.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

# ... (other functions) ...

# Load the data based on the selected competition
comp = 'premier'  # Default to Premier League
data = load_data(comp)

def get_team_names(data):
    team_names = set()
    for match in data:
        team_names.add(match['HomeTeam'])
        team_names.add(match['AwayTeam'])
    return sorted(team_names)

def get_teams_for_h2h(team1_index, team2_index, data):
    team_names = get_team_names(data)
    team1 = team_names[team1_index]
    team2 = team_names[team2_index]
    return team1, team2

# Function to get head-to-head details
def get_h2h_details(team1, team2):
    global data  # Declare the global variable
    team1_wins = team2_wins = draws = 0
    matches = []
    for match in data:
        if match['HomeTeam'] == team1 and match['AwayTeam'] == team2:
            if match['FTR'] == 'H':
                team1_wins += 1
            elif match['FTR'] == 'A':
                team2_wins += 1
            else:
                draws += 1
            matches.append(match)
        elif match['HomeTeam'] == team2 and match['AwayTeam'] == team1:
            if match['FTR'] == 'H':
                team2_wins += 1
            elif match['FTR'] == 'A':
                team1_wins += 1
            else:
                draws += 1
            matches.append(match)
        # Convert relevant fields to integers using safe_int
    matches = [
        {
            k: (safe_int(v) if k in ['FTHG', 'FTAG', 'HTHG', 'HTAG', 'HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR'] else v)
            for k, v in match.items()
        }
        for match in matches
    ]  
    return team1_wins, team2_wins, draws, sorted(matches, key=lambda x: parser.parse(x['Date'], fuzzy=True), reverse=True)

def safe_int(value):
    """
    Convert the given value to an integer, replacing None with 0.
    """
    value = value if value is not None else 0
    try:
        return int(value)
    except:
        return float(value)
    

def calculate_overview_stats(team1, team2, team1_wins, team2_wins, draws, matches):
    def round_stat(value):
        if isinstance(value, float):
            return round(value, 2)
        else:
            return value

    team1_stats = {
        'Games Played': team1_wins + team2_wins + draws,
        'Wins': team1_wins,
        'Draws': draws,
        'Losses': team2_wins,
        'League Position': None,
        'Points Per Game': round_stat((team1_wins * 3 + draws) / (team1_wins + team2_wins + draws)),
        'AVG Goals': round_stat(sum(int(match['FTHG']) for match in matches if match['HomeTeam'] == team1) / (team1_wins + team2_wins + draws)),
        'AVG Goals Scored': round_stat(sum(int(match['FTHG']) for match in matches if match['HomeTeam'] == team1) / (team1_wins + team2_wins + draws)),
        'AVG Goals Conceded': round_stat(sum(int(match['FTAG']) for match in matches if match['HomeTeam'] == team1) / (team1_wins + team2_wins + draws)),
        'Goals Scored': sum(int(match['FTHG']) for match in matches if match['HomeTeam'] == team1),
        'Goals Conceded': sum(int(match['FTAG']) for match in matches if match['HomeTeam'] == team1),
        'Goal Difference': sum(int(match['FTHG']) - int(match['FTAG']) for match in matches if match['HomeTeam'] == team1),
        'Clean Sheet Games': sum(1 for match in matches if match['HomeTeam'] == team1 and match['FTAG'] == '0'),
        'Clean Sheet %': round_stat(sum(1 for match in matches if match['HomeTeam'] == team1 and match['FTAG'] == '0') / (team1_wins + team2_wins + draws) * 100),
        'BTTS Games': sum(1 for match in matches if match['HomeTeam'] == team1 and match['FTHG'] != '0' and match['FTAG'] != '0'),
        'BTTS %': round_stat(sum(1 for match in matches if match['HomeTeam'] == team1 and match['FTHG'] != '0' and match['FTAG'] != '0') / (team1_wins + team2_wins + draws) * 100),
        'Failed To Score': sum(1 for match in matches if match['HomeTeam'] == team1 and match['FTHG'] == '0'),
        'Failed To Score %': round_stat(sum(1 for match in matches if match['HomeTeam'] == team1 and match['FTHG'] == '0') / (team1_wins + team2_wins + draws) * 100),
        'Win %': round_stat(team1_wins / (team1_wins + team2_wins + draws) * 100),
        'Draw %': round_stat(draws / (team1_wins + team2_wins + draws) * 100),
        'Loss %': round_stat(team2_wins / (team1_wins + team2_wins + draws) * 100),
        'Winning at HT': sum(1 for match in matches if match['HomeTeam'] == team1 and match['HTHG'] > match['HTAG']),
        'Winning at HT %': round_stat(sum(1 for match in matches if match['HomeTeam'] == team1 and match['HTHG'] > match['HTAG']) / (team1_wins + team2_wins + draws) * 100),
        'Drawing at HT': sum(1 for match in matches if match['HomeTeam'] == team1 and match['HTHG'] == match['HTAG']),
        'Drawing at HT %': round_stat(sum(1 for match in matches if match['HomeTeam'] == team1 and match['HTHG'] == match['HTAG']) / (team1_wins + team2_wins + draws) * 100),
        'Losing at HT': sum(1 for match in matches if match['HomeTeam'] == team1 and match['HTHG'] < match['HTAG']),
        'Losing at HT %': round_stat(sum(1 for match in matches if match['HomeTeam'] == team1 and match['HTHG'] < match['HTAG']) / (team1_wins + team2_wins + draws) * 100),
        'HT Points Per Game': round_stat(sum(1 if match['HTR'] == 'H' else 0 if match['HTR'] == 'D' else 0 for match in matches if match['HomeTeam'] == team1) / (team1_wins + team2_wins + draws)),
        '0.5+ Goals (Games)': sum(1 for match in matches if match['HomeTeam'] == team1 and (int(match['FTHG']) + int(match['FTAG'])) >= 1),
        '1.5+ Goals (Games)': sum(1 for match in matches if match['HomeTeam'] == team1 and (int(match['FTHG']) + int(match['FTAG'])) >= 2),
        '2.5+ Goals (Games)': sum(1 for match in matches if match['HomeTeam'] == team1 and (int(match['FTHG']) + int(match['FTAG'])) >= 3),
        '3.5+ Goals (Games)': sum(1 for match in matches if match['HomeTeam'] == team1 and (int(match['FTHG']) + int(match['FTAG'])) >= 4),
        '4.5+ Goals (Games)': sum(1 for match in matches if match['HomeTeam'] == team1 and (int(match['FTHG']) + int(match['FTAG'])) >= 5),
        '0.5+ Goals %': round_stat(sum(1 for match in matches if match['HomeTeam'] == team1 and (int(match['FTHG']) + int(match['FTAG'])) >= 1) / (team1_wins + team2_wins + draws) * 100),
        '1.5+ Goals %': round_stat(sum(1 for match in matches if match['HomeTeam'] == team1 and (int(match['FTHG']) + int(match['FTAG'])) >= 2) / (team1_wins + team2_wins + draws) * 100),
        '2.5+ Goals %': round_stat(sum(1 for match in matches if match['HomeTeam'] == team1 and (int(match['FTHG']) + int(match['FTAG'])) >= 3) / (team1_wins + team2_wins + draws) * 100),
        '3.5+ Goals %': round_stat(sum(1 for match in matches if match['HomeTeam'] == team1 and (int(match['FTHG']) + int(match['FTAG'])) >= 4) / (team1_wins + team2_wins + draws) * 100),
        '4.5+ Goals %': round_stat(sum(1 for match in matches if match['HomeTeam'] == team1 and (int(match['FTHG']) + int(match['FTAG'])) >= 5) / (team1_wins + team2_wins + draws) * 100),
        '0.5- Goals (Games)': sum(1 for match in matches if match['HomeTeam'] == team1 and (int(match['FTHG']) + int(match['FTAG'])) < 1),
        '1.5- Goals (Games)': sum(1 for match in matches if match['HomeTeam'] == team1 and (int(match['FTHG']) + int(match['FTAG'])) < 2),
        '2.5- Goals (Games)': sum(1 for match in matches if match['HomeTeam'] == team1 and (int(match['FTHG']) + int(match['FTAG'])) < 3),
        '3.5- Goals (Games)': sum(1 for match in matches if match['HomeTeam'] == team1 and (int(match['FTHG']) + int(match['FTAG'])) < 4),
        '4.5- Goals (Games)': sum(1 for match in matches if match['HomeTeam'] == team1 and (int(match['FTHG']) + int(match['FTAG'])) < 5),
        '0.5- Goals %': round_stat(sum(1 for match in matches if match['HomeTeam'] == team1 and (int(match['FTHG']) + int(match['FTAG'])) < 1) / (team1_wins + team2_wins + draws) * 100),
        '1.5- Goals %': round_stat(sum(1 for match in matches if match['HomeTeam'] == team1 and (int(match['FTHG']) + int(match['FTAG'])) < 2) / (team1_wins + team2_wins + draws) * 100),
        '2.5- Goals %': round_stat(sum(1 for match in matches if match['HomeTeam'] == team1 and (int(match['FTHG']) + int(match['FTAG'])) < 3) / (team1_wins + team2_wins + draws) * 100),
        '3.5- Goals %': round_stat(sum(1 for match in matches if match['HomeTeam'] == team1 and (int(match['FTHG']) + int(match['FTAG'])) < 4) / (team1_wins + team2_wins + draws) * 100),
        '4.5- Goals %': round_stat(sum(1 for match in matches if match['HomeTeam'] == team1 and (int(match['FTHG']) + int(match['FTAG'])) < 5) / (team1_wins + team2_wins + draws) * 100),
    }

    team2_stats = {
        'Games Played': team1_wins + team2_wins + draws,
        'Wins': team2_wins,
        'Draws': draws,
        'Losses': team1_wins,
        'League Position': None,
        'Points Per Game': round_stat((team2_wins * 3 + draws) / (team1_wins + team2_wins + draws)),
        'AVG Goals': round_stat(sum(int(match['FTAG']) for match in matches if match['AwayTeam'] == team2) / (team1_wins + team2_wins + draws)),
        'AVG Goals Scored': round_stat(sum(int(match['FTAG']) for match in matches if match['AwayTeam'] == team2) / (team1_wins + team2_wins + draws)),
        'AVG Goals Conceded': round_stat(sum(int(match['FTHG']) for match in matches if match['AwayTeam'] == team2) / (team1_wins + team2_wins + draws)),
        'Goals Scored': sum(int(match['FTAG']) for match in matches if match['AwayTeam'] == team2),
        'Goals Conceded': sum(int(match['FTHG']) for match in matches if match['AwayTeam'] == team2),
        'Goal Difference': sum(int(match['FTAG']) - int(match['FTHG']) for match in matches if match['AwayTeam'] == team2),
        'Clean Sheet Games': sum(1 for match in matches if match['AwayTeam'] == team2 and match['FTHG'] == '0'),
        'Clean Sheet %': round_stat(sum(1 for match in matches if match['AwayTeam'] == team2 and match['FTHG'] == '0') / (team1_wins + team2_wins + draws) * 100),
        'BTTS Games': sum(1 for match in matches if match['AwayTeam'] == team2 and match['FTHG'] != '0' and match['FTAG'] != '0'),
        'BTTS %': round_stat(sum(1 for match in matches if match['AwayTeam'] == team2 and match['FTHG'] != '0' and match['FTAG'] != '0') / (team1_wins + team2_wins + draws) * 100),
        'Failed To Score': sum(1 for match in matches if match['AwayTeam'] == team2 and match['FTAG'] == '0'),
        'Failed To Score %': round_stat(sum(1 for match in matches if match['AwayTeam'] == team2 and match['FTAG'] == '0') / (team1_wins + team2_wins + draws) * 100),
        'Win %': round_stat(team2_wins / (team1_wins + team2_wins + draws) * 100),
        'Draw %': round_stat(draws / (team1_wins + team2_wins + draws) * 100),
        'Loss %': round_stat(team1_wins / (team1_wins + team2_wins + draws) * 100),
        'Winning at HT': sum(1 for match in matches if match['AwayTeam'] == team2 and match['HTHG'] < match['HTAG']),
        'Winning at HT %': round_stat(sum(1 for match in matches if match['AwayTeam'] == team2 and match['HTHG'] < match['HTAG']) / (team1_wins + team2_wins + draws) * 100),
        'Drawing at HT': sum(1 for match in matches if match['AwayTeam'] == team2 and match['HTHG'] == match['HTAG']),
        'Drawing at HT %': round_stat(sum(1 for match in matches if match['AwayTeam'] == team2 and match['HTHG'] == match['HTAG']) / (team1_wins + team2_wins + draws) * 100),
        'Losing at HT': sum(1 for match in matches if match['AwayTeam'] == team2 and match['HTHG'] > match['HTAG']),
        'Losing at HT %': round_stat(sum(1 for match in matches if match['AwayTeam'] == team2 and match['HTHG'] > match['HTAG']) / (team1_wins + team2_wins + draws) * 100),
        'HT Points Per Game': round_stat(sum(0 if match['HTR'] == 'H' else 1 if match['HTR'] == 'D' else 0 for match in matches if match['AwayTeam'] == team2) / (team1_wins + team2_wins + draws)),
        '0.5+ Goals (Games)': sum(1 for match in matches if match['AwayTeam'] == team2 and (int(match['FTHG']) + int(match['FTAG'])) >= 1),
        '1.5+ Goals (Games)': sum(1 for match in matches if match['AwayTeam'] == team2 and (int(match['FTHG']) + int(match['FTAG'])) >= 2),
        '2.5+ Goals (Games)': sum(1 for match in matches if match['AwayTeam'] == team2 and (int(match['FTHG']) + int(match['FTAG'])) >= 3),
        '3.5+ Goals (Games)': sum(1 for match in matches if match['AwayTeam'] == team2 and (int(match['FTHG']) + int(match['FTAG'])) >= 4),
        '4.5+ Goals (Games)': sum(1 for match in matches if match['AwayTeam'] == team2 and (int(match['FTHG']) + int(match['FTAG'])) >= 5),
        '0.5+ Goals %': round_stat(sum(1 for match in matches if match['AwayTeam'] == team2 and (int(match['FTHG']) + int(match['FTAG'])) >= 1) / (team1_wins + team2_wins + draws) * 100),
        '1.5+ Goals %': round_stat(sum(1 for match in matches if match['AwayTeam'] == team2 and (int(match['FTHG']) + int(match['FTAG'])) >= 2) / (team1_wins + team2_wins + draws) * 100),
        '2.5+ Goals %': round_stat(sum(1 for match in matches if match['AwayTeam'] == team2 and (int(match['FTHG']) + int(match['FTAG'])) >= 3) / (team1_wins + team2_wins + draws) * 100),
        '3.5+ Goals %': round_stat(sum(1 for match in matches if match['AwayTeam'] == team2 and (int(match['FTHG']) + int(match['FTAG'])) >= 4) / (team1_wins + team2_wins + draws) * 100),
        '4.5+ Goals %': round_stat(sum(1 for match in matches if match['AwayTeam'] == team2 and (int(match['FTHG']) + int(match['FTAG'])) >= 5) / (team1_wins + team2_wins + draws) * 100),
        '0.5- Goals (Games)': sum(1 for match in matches if match['AwayTeam'] == team2 and (int(match['FTHG']) + int(match['FTAG'])) < 1),
        '1.5- Goals (Games)': sum(1 for match in matches if match['AwayTeam'] == team2 and (int(match['FTHG']) + int(match['FTAG'])) < 2),
        '2.5- Goals (Games)': sum(1 for match in matches if match['AwayTeam'] == team2 and (int(match['FTHG']) + int(match['FTAG'])) < 3),
        '3.5- Goals (Games)': sum(1 for match in matches if match['AwayTeam'] == team2 and (int(match['FTHG']) + int(match['FTAG'])) < 4),
        '4.5- Goals (Games)': sum(1 for match in matches if match['AwayTeam'] == team2 and (int(match['FTHG']) + int(match['FTAG'])) < 5),
        '0.5- Goals %': round_stat(sum(1 for match in matches if match['AwayTeam'] == team2 and (int(match['FTHG']) + int(match['FTAG'])) < 1) / (team1_wins + team2_wins + draws) * 100),
        '1.5- Goals %': round_stat(sum(1 for match in matches if match['AwayTeam'] == team2 and (int(match['FTHG']) + int(match['FTAG'])) < 2) / (team1_wins + team2_wins + draws) * 100),
        '2.5- Goals %': round_stat(sum(1 for match in matches if match['AwayTeam'] == team2 and (int(match['FTHG']) + int(match['FTAG'])) < 3) / (team1_wins + team2_wins + draws) * 100),
        '3.5- Goals %': round_stat(sum(1 for match in matches if match['AwayTeam'] == team2 and (int(match['FTHG']) + int(match['FTAG'])) < 4) / (team1_wins + team2_wins + draws) * 100),
        '4.5- Goals %': round_stat(sum(1 for match in matches if match['AwayTeam'] == team2 and (int(match['FTHG']) + int(match['FTAG'])) < 5) / (team1_wins + team2_wins + draws) * 100),
    }

    return team1_stats, team2_stats