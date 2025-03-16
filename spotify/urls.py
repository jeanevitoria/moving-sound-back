from django.urls import path
from . import views
from .views import AuthView

urlpatterns=[
    path('get-token/', AuthView.as_view(), name='get_token')
]