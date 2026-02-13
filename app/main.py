import sys
import os
import re
import streamlit as st

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from data_processing.youtube_api import get_channel_details, get_all_videos_metadata

st.set_page_config(page_title="YouTube Channel Analyzer", layout="wide")

st.title("📊 YouTube Channel Analyzer Dashboard")

st.markdown("""
Enter a valid YouTube Channel ID to fetch channel statistics and video metadata.
""")

st.divider()


def is_valid_channel_id(channel_id):
    pattern = r"^UC[a-zA-Z0-9_-]{22}$"
    return re.match(pattern, channel_id)


channel_id = st.text_input(
    "Channel ID",
    placeholder="Example: UC_x5XG1OV2P6uZZ5FSM9Ttw"
)

col1, col2 = st.columns(2)

with col1:
    fetch_channel = st.button("Fetch Channel Data")

with col2:
    fetch_videos = st.button("Fetch All Videos")


# ----------------------------------------
# Channel Data Display
# ----------------------------------------
if fetch_channel:

    if not channel_id or not is_valid_channel_id(channel_id):
        st.error("Invalid Channel ID format.")
    else:
        with st.spinner("Fetching channel data..."):
            response = get_channel_details(channel_id)

        if "error" in response:
            st.error(response["error"])
        else:
            item = response["items"][0]
            snippet = item["snippet"]
            statistics = item["statistics"]

            st.success("Channel data fetched successfully!")

            col1, col2 = st.columns([1, 3])

            with col1:
                st.image(snippet["thumbnails"]["high"]["url"], width=160)

            with col2:
                st.markdown(f"## {snippet['title']}")
                st.markdown(snippet["description"])

            st.divider()

            metric1, metric2, metric3 = st.columns(3)

            subscribers = int(statistics.get("subscriberCount", 0))
            total_videos = int(statistics.get("videoCount", 0))
            total_views = int(statistics.get("viewCount", 0))

            metric1.metric("Subscribers", f"{subscribers:,}")
            metric2.metric("Total Videos", f"{total_videos:,}")
            metric3.metric("Total Views", f"{total_views:,}")

            st.markdown(f"**Channel Created On:** {snippet['publishedAt']}")


# ----------------------------------------
# Video Metadata Display
# ----------------------------------------
if fetch_videos:

    if not channel_id or not is_valid_channel_id(channel_id):
        st.error("Invalid Channel ID format.")
    else:
        with st.spinner("Fetching video metadata... This may take time ⏳"):
            df = get_all_videos_metadata(channel_id)

        st.success("Video metadata fetched successfully!")
        st.dataframe(df)
