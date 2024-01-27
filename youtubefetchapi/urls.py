from django.urls import path,include 
from . import views

urlpatterns = [
    path('api/view',views.view_video,name='viewapi'),
    path('api/search',views.search_video,name='searchapi'),
]