import os
import threading
from datetime import datetime, timedelta
import time
from googleapiclient.discovery import build
import googleapiclient.errors
from django.apps import apps
from dotenv import load_dotenv
from django.core.paginator import Paginator
from django.core import serializers
from django.http import HttpResponse
from django.db.models import Q

load_dotenv()

API_KEYS = list(os.getenv("key").split(","))

def start_fetch_video_thread():
    thread = threading.Thread(target=fetch_video)
    thread.daemon = True  # Daemonize thread
    thread.start()

def fetch_video(api_key_index=0):
    while True:
        try:
            api_key = API_KEYS[api_key_index]
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
            print(e)
            api_key_index = (api_key_index + 1) % len(API_KEYS)
            if api_key_index == 0:
                time.sleep(60)

        time.sleep(10)
        
def view_video(request):
    try:
        page_number = int(request.GET.get('page', 1))
    except ValueError:
        page_number = 1

    Video = apps.get_model('youtubefetchapi', 'Video')
    video_list = Video.objects.all().order_by('-publishedAt')

    paginator = Paginator(video_list, 20)

    page_obj = paginator.get_page(page_number)

    videos_per_page = serializers.serialize('json', page_obj.object_list)
    return HttpResponse(videos_per_page, content_type="text/json-comment-filtered")

def search_video(request):
    q = request.GET.get("q", "")
    query_terms = q.split()

    Video = apps.get_model('youtubefetchapi', 'Video')

    query_objects = Q()
    for term in query_terms:
        if term: 
            query_objects |= Q(title__icontains=term) | Q(description__icontains=term)

    all_videos = Video.objects.filter(query_objects).distinct()

    all_videos_list = serializers.serialize('json', all_videos)
    return HttpResponse(all_videos_list, content_type="text/json-comment-filtered")
