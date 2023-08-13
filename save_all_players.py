import requests
import json

r = requests.get('https://api.sleeper.app/v1/players/nfl')

response_dict = r.json()

with open('./players/all_players.json', 'w', encoding='utf-8') as file:
    json.dump(response_dict, file, ensure_ascii=False, indent=4)