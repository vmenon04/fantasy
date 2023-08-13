import streamlit as st
from PIL import Image
import requests
import time
from matplotlib import pyplot as plt
from time import sleep
import numpy as np

from get_data import Sleeper
from optimal_lineup import *
from trade_evaluator import evaluate_trade

st.set_page_config(
    page_title="RL Analytics Grapher",
    page_icon="📈",
)

st.title('🚀🔒 Analytics Grapher')

try:
    LEAGUE_ID = st.session_state["LEAGUE_ID"]
    USERNAME = st.session_state["USERNAME"]
    TEAM_FORMAT = st.session_state["TEAM_FORMAT"]
    sleeper = st.session_state["SLEEPER"]

    st.caption("League ID: " + LEAGUE_ID)


    if st.button('Click to View Your Teams Predicted Score Per Week'):
        vals = []
        progress_bar = st.progress(0, text="Graphing in progress. This may take a while..")
        for int_week in range(1,15):
            progress_bar.progress((int_week-1)/13)

            week = str(int_week)
            vals.append(find_my_optimal_lineup(TEAM_FORMAT, LEAGUE_ID, USERNAME, week, False))

        np.random.shuffle(vals)
        fig, ax = plt.subplots()
        ax.plot(np.arange(1, 15), vals)
        ax.set_xlabel('Week')
        ax.set_ylabel('Optimal Lineup Projected Score')
        ax.set_xticks(np.arange(1,15))

        st.pyplot(fig)

except Exception as e:
    st.error("Error")
    print(e)