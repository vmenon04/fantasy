from get_data import Sleeper

def find_my_optimal_lineup(team_format, league_id, username, week, printable=True):

    sleeper = Sleeper(league_id, username)

    player_projs_dict = sleeper.get_my_roster_player_projs_dict(week)

    remaining_players = sleeper.get_my_roster_player_ids()

    total_team_projection = 0

    if (printable):
        print()
        print("Optimal Lineup")
        print("--------------")

    for accepted_positions in team_format:
        best_player = None
        best_player_projection = 0

        for player in remaining_players:
            if (player_projs_dict[player]['position'] in accepted_positions):
                if (player_projs_dict[player]['projection'] > best_player_projection):
                    best_player = player
                    best_player_projection = player_projs_dict[best_player]['projection']

        if (best_player is not None):
            remaining_players.remove(best_player)
            
            best_player_name = sleeper.get_player_name_from_id(best_player)
            best_player_projection = player_projs_dict[best_player]['projection']
            
            total_team_projection += best_player_projection

            if (printable):
                print('{}{}'.format(str(best_player_name).ljust(40), best_player_projection))

        else:
            if (printable):
                print('{}{}'.format(str("*** No Player Available ***").ljust(40), 0))
        
    if (printable):
        print()
        print('{}{}'.format(str("Total Team Projection").ljust(40), round(total_team_projection, 2)))

    return total_team_projection

def find_optimal_lineup_from_roster(roster, team_format, league_id, username, week, printable=False):

    sleeper = Sleeper(league_id, username)

    player_projs_dict = sleeper.get_player_projs_dict_from_roster(roster, week)

    remaining_players = roster[:]

    total_team_projection = 0

    if (printable):
        print()
        print("Optimal Lineup")
        print("--------------")

    for accepted_positions in team_format:
        best_player = None
        best_player_projection = 0

        for player in remaining_players:
            if (player_projs_dict[player]['position'] in accepted_positions):
                if (player_projs_dict[player]['projection'] > best_player_projection):
                    best_player = player
                    best_player_projection = player_projs_dict[best_player]['projection']

        if (best_player is not None):
            remaining_players.remove(best_player)
            
            best_player_name = sleeper.get_player_name_from_id(best_player)
            best_player_projection = player_projs_dict[best_player]['projection']
            
            total_team_projection += best_player_projection

            if (printable):
                print('{}{}'.format(str(best_player_name).ljust(40), best_player_projection))
        
        else:
            if (printable):
                print('{}{}'.format(str("*** No Player Available ***").ljust(40), 0))

    if (printable):
        print()
        print('{}{}'.format(str("Total Team Projection").ljust(40), round(total_team_projection, 2)))

    return total_team_projection