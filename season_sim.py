import requests
import json
from tqdm import tqdm
from get_data import Sleeper
from optimal_lineup import find_optimal_lineup_from_roster


LEAGUE_ID = "917949555663654912"
TEAM_FORMAT = [['QB'], ['RB'], ['RB'], ['WR'], ['WR'], ['WR'], ['TE'], ['WR','RB','TE'], ['WR','RB','TE'], ['WR','RB','TE'], ['WR','RB','TE', 'QB']]
USERNAME = "ClutchVasu"
sleeper = Sleeper(LEAGUE_ID, "ClutchVasu")

records = {}
for user_id in sleeper.get_all_owner_user_id():
    records[user_id] = {"wins": 0, "losses": 0, "ties": 0, "points_for": 0, "points_against": 0}


for int_week in range(1,15):
    week = str(int_week)

    r_matchups = requests.get('https://api.sleeper.app/v1/league/' + LEAGUE_ID + '/matchups/' + week)
    r_matchups_dict = r_matchups.json()

    matchups = {}

    for matchup_entry in r_matchups_dict:
        matchups[matchup_entry["matchup_id"]] = []
    for matchup_entry in r_matchups_dict:
        roster_id = matchup_entry["roster_id"]
        matchups[matchup_entry["matchup_id"]].append(sleeper.get_owner_user_id_from_roster_id(roster_id))

    for matchup_key in matchups:
        team_1_user_id = matchups[matchup_key][0]
        team_2_user_id = matchups[matchup_key][1]

        team_1_roster = sleeper.get_roster_from_user_id(team_1_user_id)
        team_2_roster = sleeper.get_roster_from_user_id(team_2_user_id)
        team_1_score = find_optimal_lineup_from_roster(team_1_roster, TEAM_FORMAT, LEAGUE_ID, USERNAME, week)
        team_2_score = find_optimal_lineup_from_roster(team_2_roster, TEAM_FORMAT, LEAGUE_ID, USERNAME, week)
        
        records[team_1_user_id]["points_for"] += team_1_score
        records[team_1_user_id]["points_against"] += team_2_score

        records[team_2_user_id]["points_for"] += team_2_score
        records[team_2_user_id]["points_against"] += team_1_score

        if (team_1_score > team_2_score):
            records[team_1_user_id]["wins"] += 1
            records[team_2_user_id]["losses"] += 1
        elif (team_1_score < team_2_score):
            records[team_1_user_id]["losses"] += 1
            records[team_2_user_id]["wins"] += 1
        else:
            records[team_1_user_id]["ties"] += 1
            records[team_2_user_id]["ties"] += 1

sorted_data = sorted(records.items(), key=lambda x: (x[1]['wins'], x[1]['points_for']), reverse=True)
sorted_dict = {item[0]: item[1] for item in sorted_data}

records.clear()
records.update(sorted_dict)

print()
for key in records:
    display_name = sleeper.get_display_name_from_user_id(key)
    print(display_name)
    print('    {}{}'.format(("Wins: ").ljust(15), str(records[key]['wins'])))
    print('    {}{}'.format(("Losses: ").ljust(15), str(records[key]['losses'])))
    print('    {}{}'.format(("Ties: ").ljust(15), str(records[key]['ties'])))
    print('    {}{}'.format(("Points for: ").ljust(15), str(round(records[key]['points_for'], 2))))
    print('    {}{}'.format(("Points Against: ").ljust(15), str(round(records[key]['points_against'], 2))))
    print()