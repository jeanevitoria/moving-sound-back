from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
import environ
import requests
import base64
import re

# Inicializa o django-environ
env = environ.Env()

# Carrega as variáveis do .env
environ.Env.read_env()

# Requisição do token à API do Spotify
class AuthView(APIView):
    def post(self, request):
        client_id = env('CLIENT_ID')
        client_secret = env('CLIENT_SECRET')
        print(client_id, client_secret)
        credentials = f"{client_id}:{client_secret}"

        encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

        headers = {
            'Authorization': f'Basic {encoded_credentials}'
        }

        data = {
            'grant_type': 'client_credentials'
        }
        response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
        print(response)
            
        return Response(data=response.json(), status=response.status_code)
    
class PlaylistView(APIView):
    
    def post(self, request):
        token = request.headers.get('Authorization')
        
        if token and token.startswith('Bearer '):
            token = token.split(' ')[1]
        else:
            return Response({"error": "Token de autorização não fornecido ou inválido"}, status=401)
        
        playlist_link = self.request.POST.get("playlist_link")
        playlist_id = re.split(r'[/?]', playlist_link)[-1]
        
        headers = {
            'Authorization': f'Bearer {token}'
        }
        
        url = f'https://api.spotify.com/v1/playlists/{playlist_id}?fields=tracks.items%28track%28name%2Chref%2Cartists%2Calbum%28%21name%2Chref%29%29%29'
        
        response = request.get(url, headers=headers)
        print(response)
        return Response(data=response.json(), status=response.status_code)