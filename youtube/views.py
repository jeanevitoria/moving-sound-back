import json
from django.shortcuts import render
from googleapiclient.discovery import build
from rest_framework.views import APIView
import environ
from django.shortcuts import render
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.shortcuts import render, HttpResponse
from rest_framework.response import Response

# Inicializa o django-environ
env = environ.Env()

# Carrega as variáveis do .env
environ.Env.read_env()

api_key = env('KEY')

class YoutubeSearch(APIView):
    def post(self, request):
        youtube = build('youtube', 'v3', developerKey=api_key)

        data = json.loads(request.body)
        query = data.get("search_data")
        
        try:
            req = youtube.search().list(q=query, part='snippet', type='video', maxResults=1, order="viewCount" )
            res = req.execute()
            print(res)

            return Response(data=res, status=200)
        except HttpError as e:
            print(f'Ocorreu um erro: {e}')
            return render(request, 'your_template.html', e)