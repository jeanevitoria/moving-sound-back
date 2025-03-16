from django.urls import path
from . import views

urlpatterns=[
    path('youtube_search/', views.youtube_search, name='youtube_search'),
]