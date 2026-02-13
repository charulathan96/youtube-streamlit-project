import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd

# Load API Key
load_dotenv(".gitenv")
API_KEY = os.getenv("YOUTUBE_API_KEY")

if not API_KEY:
    raise ValueError("API Key not found. Check .gitenv file.")

youtube = build("youtube", "v3", developerKey=API_KEY)


# ------------------------------------------------
# TASK 2 - Basic Channel Details
# ------------------------------------------------
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


# ------------------------------------------------
# TASK 3 - Channel Extraction (Multiple)
# ------------------------------------------------
def extract_channel_details(channel_ids):
    data = []

    for channel_id in channel_ids:
        try:
            response = youtube.channels().list(
                part="snippet,statistics",
                id=channel_id.strip()
            ).execute()

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
                "Thumbnail URL": snippet.get("thumbnails", {}).get("high", {}).get("url")
            }

            data.append(channel_data)

        except Exception:
            continue

    return pd.DataFrame(data)


# ------------------------------------------------
# TASK 5 - Video Metadata Extraction with Pagination
# ------------------------------------------------
def get_all_videos_metadata(channel_id):
    try:
        # Step 1: Get Upload Playlist ID
        channel_response = youtube.channels().list(
            part="contentDetails",
            id=channel_id
        ).execute()

        if not channel_response["items"]:
            raise ValueError("Invalid Channel ID")

        uploads_playlist_id = channel_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

        videos = []
        next_page_token = None

        # Step 2: Pagination loop
        while True:
            playlist_response = youtube.playlistItems().list(
                part="snippet",
                playlistId=uploads_playlist_id,
                maxResults=50,
                pageToken=next_page_token
            ).execute()

            video_ids = [
                item["snippet"]["resourceId"]["videoId"]
                for item in playlist_response["items"]
            ]

            # Step 3: Get detailed metadata
            video_response = youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id=",".join(video_ids)
            ).execute()

            for video in video_response["items"]:
                snippet = video.get("snippet", {})
                statistics = video.get("statistics", {})
                content_details = video.get("contentDetails", {})

                videos.append({
                    "Video ID": video.get("id"),
                    "Title": snippet.get("title"),
                    "Description": snippet.get("description"),
                    "Published At": snippet.get("publishedAt"),
                    "Duration": content_details.get("duration"),
                    "Views": statistics.get("viewCount", 0),
                    "Likes": statistics.get("likeCount", 0),
                    "Comments": statistics.get("commentCount", 0),
                    "Thumbnail URL": snippet.get("thumbnails", {}).get("high", {}).get("url")
                })

            next_page_token = playlist_response.get("nextPageToken")

            if not next_page_token:
                break

        return pd.DataFrame(videos)

    except HttpError as e:
        raise Exception(f"YouTube API Error: {e}")
    except Exception as e:
        raise Exception(str(e))
