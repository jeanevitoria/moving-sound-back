from django.urls import path
from . import views
from .views import YoutubeCrawler

urlpatterns=[
    path('youtube-search/', YoutubeCrawler.as_view(), name='YoutubeCrawler'),
]