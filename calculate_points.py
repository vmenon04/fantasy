# Half PPR Rocket Lockett League Rules (2023)

'''
Expects a player projection dictionary for a specifc week
'''
def get_projections_from_player(player_projection_dictionary, week):
    projected_points = 0
    if (player_projection_dictionary[str(week)] is not None):
        projected_points = player_projection_dictionary[str(week)]["stats"]["pts_ppr"]
    return projected_points