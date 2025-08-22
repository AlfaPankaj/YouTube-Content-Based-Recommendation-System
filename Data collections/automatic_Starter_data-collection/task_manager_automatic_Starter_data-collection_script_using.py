import os
import time
import json
import pandas as pd
import sqlite3
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

def get_youtube_client():
    """Builds and returns the YouTube API client."""
    load_dotenv()
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise ValueError("YOUTUBE_API_KEY not found. Make sure it's in a .env file or set as an environment variable.")
    return build("youtube", "v3", developerKey=api_key)

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def search_videos(youtube_client, query, max_results=500, regionCode="IN"):
    """Searches for videos and returns a list of video IDs."""
    results = []
    try:
        request = youtube_client.search().list(q=query, part="id", type="video", maxResults=50, regionCode=regionCode)
        while request and len(results) < max_results:
            resp = request.execute()
            for item in resp.get("items", []):
                if item['id']['kind'] == 'youtube#video':
                    results.append(item["id"]["videoId"])
                if len(results) >= max_results:
                    break
            request = youtube_client.search().list_next(request, resp)
            time.sleep(0.1)
    except HttpError as e:
        print(f"An error occurred during search: {e}")
    return results

def get_video_details(youtube_client, video_ids):
    """Fetches details for a list of video IDs."""
    rows = []
    for batch in chunks(video_ids, 50):
        try:
            resp = youtube_client.videos().list(part="snippet,contentDetails,statistics", id=",".join(batch), maxResults=50).execute()
        except HttpError as e:
            print(f"HttpError: {e}")
            time.sleep(5)
            continue
        for item in resp.get("items", []):
            snip = item.get("snippet", {}); stats = item.get("statistics", {}); content = item.get("contentDetails", {})
            like_count = stats.get("likeCount"); comment_count = stats.get("commentCount")
            rows.append({
                "video_id": item.get("id"), "title": snip.get("title"), "description": snip.get("description"),
                "tags": json.dumps(snip.get("tags", [])), "published_at": snip.get("publishedAt"), "channel_id": snip.get("channelId"),
                "channel_title": snip.get("channelTitle"), "category_id": snip.get("categoryId"), "duration": content.get("duration"),
                "definition": content.get("definition"), "viewCount": int(stats.get("viewCount", 0)),
                "likeCount": int(like_count) if like_count is not None else None,
                "commentCount": int(comment_count) if comment_count is not None else None,
            })
        time.sleep(0.1)
    return rows

def run_data_collection():
    """Main function to run the entire data collection process."""
    youtube_client = get_youtube_client()
    queries = ["technology", "education", "music", "gaming", "sports", "comedy", "news", "cooking", "travel"]
    all_rows = []
    for q in queries:
        print(f"Searching for query: '{q}'...")
        ids = search_videos(youtube_client, q, max_results=500)
        print(f" -> Found {len(ids)} video IDs.")
        if ids:
            rows = get_video_details(youtube_client, ids)
            all_rows.extend(rows)
            print(f" -> Fetched details for {len(rows)} videos.")
            
    if not all_rows:
        print("No video data was collected. Exiting.")
        return
        
    df = pd.DataFrame(all_rows).drop_duplicates(subset=["video_id"])
    out_csv="youtube_sample.csv"
    sqlite_db="youtube_videos.db"
    df.to_csv(out_csv, index=False)
    conn = sqlite3.connect(sqlite_db)
    df.to_sql("videos", conn, if_exists="replace", index=False)
    conn.close()
    print(f"\nSaved {len(df)} unique videos to '{out_csv}' and '{sqlite_db}'.")

# This block makes the script runnable from the command line
if __name__ == "__main__":
    run_data_collection()