import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from data_processing.youtube_api import get_channel_details, extract_channel_details

st.title("YouTube API Dashboard 🚀")

tab1, tab2 = st.tabs(["Basic Fetch", "Channel Extraction Module"])

# ------------------ TAB 1 ------------------
with tab1:
    st.header("Basic Channel Details (Task 2)")

    channel_id = st.text_input("Enter Channel ID")

    if st.button("Fetch Channel Details"):
        if channel_id:
            data = get_channel_details(channel_id)
            st.json(data)
        else:
            st.warning("Please enter a Channel ID")


# ------------------ TAB 2 ------------------
with tab2:
    st.header("Comprehensive Channel Data Extraction (Task 3)")

    channel_input = st.text_area(
        "Enter Channel IDs (comma separated)"
    )

    if st.button("Extract Channel Data"):
        try:
            channel_ids = [cid.strip() for cid in channel_input.split(",")]
            df = extract_channel_details(channel_ids)

            st.success("Channel data extracted successfully!")
            st.dataframe(df)

        except Exception as e:
            st.error(str(e))
