from django.shortcuts import render
from googleapiclient.discovery import build
import environ
from django.shortcuts import render
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.shortcuts import render, HttpResponse

# Inicializa o django-environ
env = environ.Env()

# Carrega as variáveis do .env
environ.Env.read_env()

api_key = env('KEY')

def youtube_search(request):
    print(f"Usando a chave de API: {api_key}") 
    youtube = build('youtube', 'v3', developerKey=api_key)

    try:
        req = youtube.search().list(q='Justin Bieber', part='snippet', type='video')
        res = req.execute()

        print(res) 
    except HttpError as e:
        print(f'Ocorreu um erro: {e}')
        return render(request, 'your_template.html', {'error': 'Erro ao buscar vídeos.'})

    finally:
        youtube.close()