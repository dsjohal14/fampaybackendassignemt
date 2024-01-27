from django.apps import AppConfig
from .views import start_fetch_video_thread
import sys

class ApirunConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'youtubefetchapi'
    
    def ready(self):
        RUNNING_DEVSERVER = len(sys.argv) > 1 and sys.argv[1] == 'runserver'
        if RUNNING_DEVSERVER:
            start_fetch_video_thread()
