from django.urls import path
from .views import GetOAuthTokenView, OAuth, OAuthCallback

urlpatterns=[
    path('google/callback/', OAuthCallback.as_view(), name='OAuthCallback'),
    path('get-oauth-token/<str:session_id>/', GetOAuthTokenView.as_view(), name='GetOAuthTokenView'),
    path('<str:session_id>', OAuth.as_view(), name='OAuth'),
]