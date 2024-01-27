from django.urls import path,include 
from . import views

urlpatterns = [
    path('api/view',views.view_video,name='viewapi'),
]