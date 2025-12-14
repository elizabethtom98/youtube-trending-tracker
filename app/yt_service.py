import os
import datetime as dt
import requests
from dotenv import load_dotenv
from typing import Dict, Any, List

load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
BASE_URL = "https://www.googleapis.com/youtube/v3/videos"


def normalize_items(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Flatten/clean trending items → list of dicts
    """
    items = data.get("items", [])
    captured_at = data.get("_captured_at")
    region = data.get("_region")

    rows = []
    for entry in items:
        snippet = entry.get("snippet", {})
        stats = entry.get("statistics", {})

        rows.append({
            "videoId": entry.get("id"),
            "title": snippet.get("title"),
            "channelId": snippet.get("channelId"),
            "channelTitle": snippet.get("channelTitle"),
            "categoryId": snippet.get("categoryId"),
            "publishedAt": snippet.get("publishedAt"),
            "views": int(stats.get("viewCount", 0)),
            "likes": int(stats.get("likeCount", 0)),
            "comments": int(stats.get("commentCount", 0)),
            "regionCode": region,
            "capturedAt": captured_at,
        })

    return rows


def fetch_trending(region: str = "AU", max_results: int = 20) -> Dict[str, Any]:
    """
    Fetch trending videos from YouTube API.
    """
    if not YOUTUBE_API_KEY:
        raise ValueError("Missing YOUTUBE_API_KEY in .env")

    params = {
        "part": "snippet,statistics,contentDetails",
        "chart": "mostPopular",
        "regionCode": region,
        "maxResults": min(max_results, 50),
        "key": YOUTUBE_API_KEY,
    }

    response = requests.get(BASE_URL, params=params, timeout=20)
    response.raise_for_status()

    data = response.json()
    data["_captured_at"] = dt.datetime.utcnow().isoformat()
    data["_region"] = region

    return data
