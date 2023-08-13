import streamlit as st
from PIL import Image
import requests
import time

from get_data import Sleeper
from optimal_lineup import *
from trade_evaluator import evaluate_trade

st.set_page_config(
    page_title="RL Internal",
    page_icon="🚀",
)

USERNAME = None
LEAGUE_ID = "917949555663654912"
TEAM_FORMAT = [['QB'], ['RB'], ['RB'], ['WR'], ['WR'], ['WR'], ['TE'], ['WR','RB','TE'], ['WR','RB','TE'], ['WR','RB','TE'], ['WR','RB','TE', 'QB']]

if 'LEAGUE_ID' not in st.session_state:
    st.session_state['LEAGUE_ID'] = LEAGUE_ID

st.title('🚀🔒 Internal Tools')

st.caption("League ID: " + LEAGUE_ID)

username_value = ""
if ('USERNAME' in st.session_state):
    username_value = st.session_state['USERNAME']
USERNAME = str(st.text_input('Team Name:', value=username_value, placeholder='Username', label_visibility="hidden"))

if 'USERNAME' in st.session_state:
    USERNAME = st.session_state['USERNAME']

sleeper = None
user_id = None

if 'SLEEPER' in st.session_state:
    sleeper = st.session_state['SLEEPER']
if 'USER_ID' in st.session_state:
    user_id = st.session_state['USER_ID']

if (USERNAME is not None and len(USERNAME) > 1):
    try:
        st.session_state['USERNAME'] = USERNAME
        if (sleeper is None):
            sleeper = Sleeper(LEAGUE_ID, USERNAME)
        user_id = sleeper.get_my_user_id()
        st.session_state['USER_ID'] = user_id
        st.session_state['SLEEPER'] = sleeper
        st.session_state['TEAM_FORMAT'] = TEAM_FORMAT

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

    except Exception as e:
        st.error("Error")
        print(e)