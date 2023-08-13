import streamlit as st
from PIL import Image
import requests
import time

from get_data import Sleeper
from optimal_lineup import find_my_optimal_lineup
from trade_evaluator import evaluate_trade

st.set_page_config(
    page_title="RL Trade Calculator",
    page_icon="🧮",
)

st.title('🚀🔒 Trade Calculator')
try:
    LEAGUE_ID = st.session_state["LEAGUE_ID"]
    USERNAME = st.session_state["USERNAME"]
    TEAM_FORMAT = st.session_state["TEAM_FORMAT"]
    sleeper = st.session_state["SLEEPER"]
    user_id = st.session_state['USER_ID']

    st.caption("League ID: " + LEAGUE_ID)


    c1, c2 = st.columns(2)
    pic_url = sleeper.get_profile_pic_url_from_user_id(user_id)
    if (pic_url is not None):
        with c1:
            image = Image.open(requests.get(pic_url, stream=True).raw).resize((200,200))
            st.image(image)
        with c2:
            team_name = sleeper.get_team_name_from_user_id(user_id)
            st.subheader(team_name)
    else:
        team_name = sleeper.get_team_name_from_user_id(user_id)
        st.subheader(team_name)
    
    my_player_ids = sleeper.get_my_roster_player_ids()
    my_player_names = [sleeper.get_player_name_from_id(player_id) for player_id in my_player_ids]
    giving = st.multiselect('Players to Give', my_player_names)
    

    all_league_user_ids = sleeper.get_all_owner_user_id()
    all_players_ids = sleeper.get_all_player_id_in_league()
    all_player_names = [sleeper.get_player_name_from_id(player_id) for player_id in all_players_ids]
    getting = st.multiselect('Players to Give', all_player_names)

    if st.button('Analyze Trade'):
        if (len(giving) == 0 or len(getting) == 0):
            st.error("Error")
        else:
            with st.spinner("This may take a while.."):
                t0 = time.time()
                trade_score = evaluate_trade(giving, getting, TEAM_FORMAT, LEAGUE_ID, USERNAME, printable=False)
                t1 = time.time()
            st.success("Trade Score: " + str(round(trade_score,2)) + "\n\n\n Trade Analysis Completed in: " + str(round(t1-t0, 2)) + "s")

except Exception as e:
    st.error("Error")
    print(e)