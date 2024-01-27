from django.apps import AppConfig
from .views import fetch_video
import sys

class ApirunConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'youtubefetchapi'
    
    def ready(self):
        running_devserver = len(sys.argv) > 1 and sys.argv[1] == 'runserver'
        if running_devserver:
            fetch_video()
