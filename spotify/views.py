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

        credentials = f"{client_id}:{client_secret}"

        encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

        headers = {
            'Authorization': f'Basic {encoded_credentials}'
        }

        data = {
            'grant_type': 'client_credentials'
        }
        response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
            
        return Response(data=response.json(), status=response.status_code)
    
class PlaylistView(APIView):
    
    def get(self, request, playlist_id):
        token = request.headers.get('Authorization')

        if token and token.startswith('Bearer '):
            token = token.split(' ')[1]
        else:
            return Response({"error": "Token de autorização não fornecido ou inválido"}, status=401)
        
        headers = {
            'Authorization': f'Bearer {token}'
        }

        url = f'https://api.spotify.com/v1/playlists/{playlist_id}?fields=tracks.items%28track%28name%2Chref%2Cartists%2Calbum%28%21name%2Chref%29%29%29'
        
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print("Erro na requisição:", response.status_code, response.text)
        return Response(data=response.json(), status=response.status_code)