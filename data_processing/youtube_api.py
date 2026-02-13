import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd

# Load environment variables
load_dotenv(".gitenv")

API_KEY = os.getenv("YOUTUBE_API_KEY")

if not API_KEY:
    raise ValueError("YouTube API Key not found. Check your .gitenv file.")

# Build YouTube service
youtube = build("youtube", "v3", developerKey=API_KEY)


# ----------------------------
# TASK 2 - Basic Fetch
# ----------------------------
def get_channel_details(channel_id):
    try:
        request = youtube.channels().list(
            part="snippet,statistics",
            id=channel_id
        )
        response = request.execute()

        if not response["items"]:
            return {"error": "Invalid Channel ID"}

        return response

    except HttpError as e:
        return {"error": f"HTTP Error: {e}"}
    except Exception as e:
        return {"error": str(e)}


# ----------------------------
# TASK 3 - Comprehensive Extraction
# ----------------------------
def extract_channel_details(channel_ids):
    """
    Extract detailed channel information for multiple channel IDs
    and return as pandas DataFrame
    """

    data = []

    for channel_id in channel_ids:
        try:
            request = youtube.channels().list(
                part="snippet,statistics",
                id=channel_id.strip()
            )
            response = request.execute()

            if not response["items"]:
                continue

            item = response["items"][0]

            snippet = item.get("snippet", {})
            statistics = item.get("statistics", {})

            channel_data = {
                "Channel ID": channel_id,
                "Channel Name": snippet.get("title"),
                "Description": snippet.get("description"),
                "Subscribers": statistics.get("subscriberCount"),
                "Total Videos": statistics.get("videoCount"),
                "Total Views": statistics.get("viewCount"),
                "Created At": snippet.get("publishedAt"),
                "Thumbnail URL": snippet.get("thumbnails", {}).get("default", {}).get("url")
            }

            data.append(channel_data)

        except HttpError as e:
            print(f"HTTP Error for {channel_id}: {e}")
        except Exception as e:
            print(f"Error for {channel_id}: {e}")

    df = pd.DataFrame(data)
    return df
