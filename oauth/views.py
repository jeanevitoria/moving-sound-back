from django.shortcuts import redirect
import urllib.parse
import environ
import requests
from django.http import JsonResponse
import uuid
from django.core.cache import cache
from rest_framework.views import APIView
from django.http import HttpResponse
import json
from rest_framework.response import Response

env = environ.Env()
environ.Env.read_env()

CLIENT_ID = env('CLIENT_ID_OAUTH')
CLIENT_SECRET = env('CLIENT_SECRET_OAUTH')

def login(request, session_id):
    params = {
        'client_id': CLIENT_ID,
        'redirect_uri': 'http://localhost:8000/oauth/google/callback/',
        'response_type': 'code',
        'scope': 'https://www.googleapis.com/auth/youtube',
        'access_type': 'offline',
        'prompt': 'consent',
        'state': session_id,
    }
    url = 'https://accounts.google.com/o/oauth2/v2/auth?' + urllib.parse.urlencode(params)

    opener_origin = request.GET.get('opener_origin')
    if opener_origin:
        opener_origin = urllib.parse.unquote(opener_origin)
    else:
        opener_origin = "http://localhost:5173"

        html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Autenticação Google</title>
                </head>
                <body>
                    <p>Redirecionando para o Google...</p>
                    <script>
                        const openerOrigin = '{opener_origin}';
                        sessionStorage.setItem('oauth_opener_origin', openerOrigin);
                        console.log("Origin salvo no sessionStorage:", sessionStorage.getItem('oauth_opener_origin'));

                        setTimeout(() => {{
                            window.location.href = {json.dumps(url)};
                        }}, 100);
                    </script>
                </body>
                </html>
            """
        return HttpResponse(html_content)



def createPlaylist(res):
    redirect

class OAuthCallback(APIView):
    def get(self, request): 
        code = request.GET.get('code')
        flow_id = request.GET.get('state')

        if not code or not flow_id:
            return HttpResponse("Erro: Código de autorização ou 'state' (flow_id) ausente na callback.", status=400)

        data = {
            'code': code,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'redirect_uri': 'http://localhost:8000/oauth/google/callback/',
            'grant_type': 'authorization_code',
        }

        response = requests.post('https://oauth2.googleapis.com/token', data=data)
        token_data = response.json()
        
        cache_key = f"oauth_token:{flow_id}" 
        cache.set(cache_key, token_data, timeout=60) 
                
        frontend_relay_url = f"http://localhost:5173/oauth/relay?session_id={flow_id}"
        
        html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Aguarde...</title>
            </head>
            <body>
                <p>Finalizando autenticação...</p>
                <script>
                    // Redireciona o pop-up para a página relay no frontend
                    window.location.href = "{frontend_relay_url}";
                </script>
            </body>
            </html>
        """
        
        return HttpResponse(html_content)

class OAuth(APIView):
    def get(self, request, session_id):
        return login(request, session_id=session_id)
    
class GetOAuthTokenView(APIView):
    def get(self, request, session_id):
        print('acessou')
        token_data = cache.get(f"oauth_token:{session_id}")
        print(f'token_data: {token_data}')
            
        if not token_data:
            return Response({'error': 'Token não encontrado ou expirado'}, status=404)
        cache.delete(f"oauth_token:{session_id}")
        return Response(token_data)
