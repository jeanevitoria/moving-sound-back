from django.urls import path
from . import views
from .views import AuthView, PlaylistView

urlpatterns=[
    path('get-token/', AuthView.as_view(), name='get_token'),
    path('playlist/<str:playlist_id>/', PlaylistView.as_view(), name='playlist')
]