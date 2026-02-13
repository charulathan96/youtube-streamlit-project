import sys
import os
import re
import streamlit as st

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from data_processing.youtube_api import get_channel_details


# ----------------------------------------
# Page Configuration
# ----------------------------------------
st.set_page_config(
    page_title="YouTube Channel Analyzer",
    page_icon="📊",
    layout="wide"
)

# ----------------------------------------
# Header Section
# ----------------------------------------
st.title("📊 YouTube Channel Analyzer Dashboard")

st.markdown("""
Welcome to the **YouTube Channel Analytics App**.  
Enter a valid YouTube Channel ID to fetch channel statistics and insights.
""")

st.divider()


# ----------------------------------------
# Channel ID Validation Function
# ----------------------------------------
def is_valid_channel_id(channel_id):
    """
    Validates YouTube Channel ID.
    Channel IDs:
    - Start with 'UC'
    - Total length = 24 characters
    """
    pattern = r"^UC[a-zA-Z0-9_-]{22}$"
    return re.match(pattern, channel_id)


# ----------------------------------------
# Input Section
# ----------------------------------------
st.subheader("🔎 Enter YouTube Channel ID")

channel_id = st.text_input(
    "Channel ID",
    placeholder="Example: UC_x5XG1OV2P6uZZ5FSM9Ttw"
)

submit = st.button("Fetch Channel Data")


# ----------------------------------------
# Fetch & Display Section
# ----------------------------------------
if submit:

    if not channel_id:
        st.error("⚠ Please enter a Channel ID.")

    elif not is_valid_channel_id(channel_id):
        st.error("⚠ Invalid Channel ID format. Please check and try again.")

    else:
        with st.spinner("Fetching channel data... ⏳"):

            response = get_channel_details(channel_id)

        if "error" in response:
            st.error(response["error"])

        else:
            item = response["items"][0]
            snippet = item["snippet"]
            statistics = item["statistics"]

            st.success("✅ Channel data fetched successfully!")

            # ----------------------------------------
            # Channel Card Layout
            # ----------------------------------------
            col1, col2 = st.columns([1, 3])

            with col1:
                st.image(
                    snippet["thumbnails"]["high"]["url"],
                    width=160
                )

            with col2:
                st.markdown(f"## {snippet['title']}")
                st.markdown(snippet["description"])

            st.divider()

            # ----------------------------------------
            # Metrics Section
            # ----------------------------------------
            metric1, metric2, metric3 = st.columns(3)

            subscribers = int(statistics.get("subscriberCount", 0))
            total_videos = int(statistics.get("videoCount", 0))
            total_views = int(statistics.get("viewCount", 0))

            metric1.metric("Subscribers", f"{subscribers:,}")
            metric2.metric("Total Videos", f"{total_videos:,}")
            metric3.metric("Total Views", f"{total_views:,}")

            st.divider()

            st.markdown(
                f"**📅 Channel Created On:** {snippet['publishedAt']}"
            )
