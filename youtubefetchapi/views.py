import os
import threading
from datetime import datetime, timedelta
from apiclient.discovery import build
import googleapiclient.errors
from django.apps import apps
from dotenv import load_dotenv

load_dotenv()

API_KEYS = list(os.getenv("key").split(","))

def fetch_video(api_key=API_KEYS[0]):
    threading.Timer(10.0, fetch_video).start()
    try:
        start_date = datetime.utcnow() - timedelta(days=1)
        published_after = start_date.strftime('%Y-%m-%dT%H:%M:%SZ')

        youtube = build('youtube', 'v3', developerKey=api_key)
        req = youtube.search().list(
            q='punjabi songs', 
            part='snippet', 
            type='video', 
            order='date', 
            publishedAfter=published_after
        )
        context = req.execute()

        Video = apps.get_model('youtubefetchapi', 'Video')

        for video_obj in context["items"]:
            video_id = video_obj["id"]["videoId"]
            title = video_obj["snippet"]["title"]
            description = video_obj["snippet"]["description"]
            thumbnail_url = video_obj["snippet"]["thumbnails"]["default"]["url"]
            published_at = datetime.strptime(video_obj["snippet"]["publishedAt"], '%Y-%m-%dT%H:%M:%SZ')

            Video.objects.get_or_create(
                video_id=video_id,
                defaults={
                    'title': title,
                    'description': description,
                    'thumbnail_url': thumbnail_url,
                    'publishedAt': published_at
                }
            )

    except googleapiclient.errors.HttpError as e:
        new_key = rotate_api_key(api_key)
        if new_key:
            fetch_video(api_key=new_key)

def rotate_api_key(current_key):
    try:
        api_keys = API_KEYS[:]
        api_keys.remove(current_key)
        return api_keys[0] if api_keys else None
    except ValueError:
        return None