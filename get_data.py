import requests
import json
from calculate_points import get_projections_from_player

class Sleeper:
    def __init__(self, league_id, username):
        self.LEAGUE_ID = league_id = "917949555663654912"
        self.USERNAME = username

        user = requests.get("https://api.sleeper.app/v1/user/" + self.USERNAME)
        self.my_user_dict = user.json()
        self.my_user_id = self.my_user_dict['user_id']

        self.r_rosters = requests.get('https://api.sleeper.app/v1/league/' + league_id + '/rosters')
        self.r_users = requests.get('https://api.sleeper.app/v1/league/' + league_id + '/users')

        self.r_rosters_dict = self.r_rosters.json()
        self.r_users_dict = self.r_users.json()

        self.players_json_file = open('./players/all_players.json')
        self.players_dict = json.load(self.players_json_file)
        
        user_roster_index = -1
        self.my_roster_id = None
        for roster in self.r_rosters_dict:
            if (self.my_user_id == roster["owner_id"]) or (roster["co_owners"] is not None and self.my_user_id in roster["co_owners"]):
                self.my_roster_id = roster["roster_id"]
                user_roster_index = roster["roster_id"] - 1
            
        self.my_roster_dict = self.r_rosters_dict[user_roster_index]
        self.players = self.my_roster_dict["players"]
    
    def get_all_player_id_in_league(self):
        all_players = []
        user_ids = self.get_all_owner_user_id()
        for user_id in user_ids:
            roster = self.get_roster_from_user_id(user_id)
            all_players += roster
        return all_players

    def get_user_id_from_display_name(self, display_name):
        for user in self.r_users_dict:
            if (display_name.lower() == user["display_name"].lower()):
                return user["user_id"]
        return None

    def get_profile_pic_url_from_user_id(self, user_id):
        user_id = str(user_id)
        for user in self.r_users_dict:
            if (user_id == user["user_id"]):
                if (user["metadata"].__contains__('avatar')):
                    return user["metadata"]["avatar"]
        return None
    
    def get_team_name_from_user_id(self, user_id):
        user_id = str(user_id)
        for user in self.r_users_dict:
            if (user_id == user["user_id"]):
                if (user["metadata"].__contains__('team_name')):
                    return user["metadata"]["team_name"]
        display_name = self.get_owner_display_name_from_roster_id(self.my_roster_id)
        if (display_name is not None):
            return ("Team " + display_name)
        return None

    def get_roster_from_user_id(self, user_id):
        for roster in self.r_rosters_dict:
            if (user_id == roster["owner_id"]) or (roster["co_owners"] is not None and user_id in roster["co_owners"]):
                return roster["players"]
        return None

    def get_all_owner_user_id(self):
        owner_user_ids = []
        for roster in self.r_rosters_dict:
            owner_user_ids.append(roster["owner_id"])
        return owner_user_ids

    def get_owner_user_id_from_roster_id(self, roster_id):
        # ignores co-owners
        roster_id = str(roster_id)
        for roster in self.r_rosters_dict:
            if (roster_id == str(roster["roster_id"])):
                return roster["owner_id"]
        return None
    
    def get_display_name_from_user_id(self, user_id):
        user_id = str(user_id)
        for user in self.r_users_dict:
            if (user_id == user["user_id"]):
                return user["display_name"]
        return None

    def get_owner_display_name_from_roster_id(self, roster_id):
        roster_id = str(roster_id)
        user_id = self.get_owner_user_id_from_roster_id(roster_id)
        return self.get_display_name_from_user_id(user_id)
    
    def get_player_name_from_id(self, player_id):
        return self.players_dict[player_id]["full_name"]
    
    def get_player_id_from_name(self, name):
        name = name.lower()
        for player_entry in self.players_dict:
            if (self.players_dict[player_entry].__contains__('full_name') and self.players_dict[player_entry]['full_name'].lower() == name):
                return self.players_dict[player_entry]['player_id']
        return "0"
    
    def get_my_user_id(self):
        return self.my_user_id

    def get_my_roster_player_ids(self):
        return self.players

    def get_my_roster_player_projs_dict(self, week):
        my_roster_projs_dict = {}
        for player in self.players:
            if (player != "0"):
                r_player_projs = requests.get('https://api.sleeper.com/projections/nfl/player/' + player + '?season_type=regular&season=2023&grouping=week')
                r_player_projs_dict = r_player_projs.json()
                projected_points = get_projections_from_player(r_player_projs_dict, week=week)
                projs_element_dict = {}
                projs_element_dict['position'] = self.players_dict[player]['position']
                projs_element_dict['projection'] = projected_points
                my_roster_projs_dict[player] = projs_element_dict
        return my_roster_projs_dict
    
    def get_player_projs_dict_from_roster(self, roster, week):
        roster_projs_dict = {}
        for player in roster:
            if (player != "0"):
                r_player_projs = requests.get('https://api.sleeper.com/projections/nfl/player/' + player + '?season_type=regular&season=2023&grouping=week')
                r_player_projs_dict = r_player_projs.json()
                projected_points = get_projections_from_player(r_player_projs_dict, week=week)
                projs_element_dict = {}
                projs_element_dict['position'] = self.players_dict[player]['position']
                projs_element_dict['projection'] = projected_points
                roster_projs_dict[player] = projs_element_dict
        return roster_projs_dict


