from django.urls import path
from .views import YoutubeSearch

urlpatterns=[
    path('youtube_search/', YoutubeSearch.as_view(), name='YoutubeSearch'),
]