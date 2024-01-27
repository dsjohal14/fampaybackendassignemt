from django.apps import AppConfig
from .views import fetch_video
import sys

class ApirunConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'youtubefetchapi'
    
    def ready(self):
        RUNNING_DEVSERVER = len(sys.argv) > 1 and sys.argv[1] == 'runserver'
        if RUNNING_DEVSERVER:
            fetch_video()
