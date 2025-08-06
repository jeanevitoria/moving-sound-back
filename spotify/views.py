from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
import environ
import requests
import base64

# Inicializa o django-environ
env = environ.Env()

# Carrega as variáveis do .env
environ.Env.read_env()

class AuthView(APIView):
    def post(self, request):
        client_id = env('CLIENT_ID')
        client_secret = env('CLIENT_SECRET')

        credentials = f"{client_id}:{client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

        headers = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = {
            'grant_type': 'client_credentials'
        }
        
        response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
        return Response(data=response.json(), status=response.status_code)
    
class PlaylistView(APIView):
    def get(self, request, playlist_id):
        token = request.headers.get('Authorization')

        if not token or not token.startswith('Bearer '):
            return Response({"error": "Token de autorização não fornecido ou inválido"}, 
                          status=status.HTTP_401_UNAUTHORIZED)
        
        token = token.split(' ')[1]
        headers = {'Authorization': f'Bearer {token}'}

        offset = 0
        # URL modificada para incluir mais campos necessários
        url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks?offset={0}'
        
        formatted_tracks = []
        
        while url:
            response = requests.get(url, headers=headers)
            
            if response.status_code != 200:
                return Response(data=response.json(), status=response.status_code)
            
            data = response.json()
                
            for item in data.get('items', []):
                track = item.get('track')
                if not track:
                    continue
                
                # Formata exatamente como solicitado: "nome artista1, artista2"
                track_name = track.get('name', '')
                artists = ', '.join([artist.get('name', '') for artist in track.get('artists', [])])
                formatted_track = f"{track_name} {artists}"
                formatted_tracks.append(formatted_track)
            
            url = data.get('next')
        
        return Response(data=formatted_tracks, status=status.HTTP_200_OK)