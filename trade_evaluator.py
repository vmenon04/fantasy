from get_data import Sleeper
from optimal_lineup import find_my_optimal_lineup, find_optimal_lineup_from_roster
from tqdm import tqdm


def evaluate_trade(giving_names, getting_names, team_format, league_id, username, printable=True):

    sleeper = Sleeper(league_id, username)

    giving = []
    getting = []

    for name in giving_names:
        giving.append(sleeper.get_player_id_from_name(name))
    for name in getting_names:
        getting.append(sleeper.get_player_id_from_name(name))

    current_roster = sleeper.get_my_roster_player_ids()

    new_roster = current_roster[:]
    for player in giving:
        new_roster.remove(player)
    for player in getting:
        new_roster.append(player)

    no_trade_score = 0
    yes_trade_score = 0
    for week in tqdm(range(1,15)):
        no_trade_score += find_optimal_lineup_from_roster(current_roster, team_format, league_id, username, str(week))
        yes_trade_score += find_optimal_lineup_from_roster(new_roster, team_format, league_id, username, str(week))
    
    trade_score = yes_trade_score - no_trade_score
    if (printable):
        print("\nGiving:")
        for name_id in giving:
            print("     - " + sleeper.get_player_name_from_id(name_id))
        print("\nGetting:")
        for name_id in getting:
            print("     - " + sleeper.get_player_name_from_id(name_id))
        print("\nTrade Score: " + str(round(trade_score, 3)) + "\n")
    return trade_score