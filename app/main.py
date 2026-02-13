import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from data_processing.youtube_api import get_channel_details

st.title("YouTube API Integration 🚀")

channel_id = st.text_input("Enter Channel ID")

if st.button("Fetch Channel Details"):
    if channel_id:
        data = get_channel_details(channel_id)
        st.json(data)
    else:
        st.warning("Please enter a Channel ID")
