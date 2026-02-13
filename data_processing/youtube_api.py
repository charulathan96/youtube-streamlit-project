import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

# Load environment variables from .gitenv
load_dotenv(".gitenv")

API_KEY = os.getenv("YOUTUBE_API_KEY")

def get_youtube_service():
    """
    Create and return YouTube API service object.
    """
    if not API_KEY:
        raise ValueError("API Key not found. Check your .gitenv file.")

    return build("youtube", "v3", developerKey=API_KEY)


def get_channel_details(channel_id):
    """
    Fetch channel details using Channel ID.
    """
    try:
        youtube = get_youtube_service()

        request = youtube.channels().list(
            part="snippet,statistics",
            id=channel_id
        )

        response = request.execute()
        return response

    except HttpError as e:
        if e.resp.status == 403:
            return {"error": "Quota exceeded or API access denied."}
        elif e.resp.status == 404:
            return {"error": "Channel not found."}
        else:
            return {"error": f"HTTP Error: {e}"}

    except Exception as e:
        return {"error": f"Unexpected Error: {e}"}
