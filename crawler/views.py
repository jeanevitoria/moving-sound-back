import asyncio
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from asgiref.sync import async_to_sync
from yt_dlp import YoutubeDL

class YoutubeSearch:
    @staticmethod
    async def search(query):
        try:
            ydl_opts = {
                'quiet': True,
                'extract_flat': True,
                'force_generic_extractor': True,
            }
            
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"ytsearch1:{query}", download=False)
                if 'entries' in info and len(info['entries']) > 0:
                    url = info['entries'][0]['url']
                    return url
            return []
        except Exception as e:
            return []

class YoutubeCrawler(APIView):
    def post(self, request):
        try:
            print(request.headers)
            data = json.loads(request.body)
            queries = data.get("search_data", [])
            if not queries:
                return Response({"error": "Missing search_data"}, status=400)

            if isinstance(queries, str):
                queries = [queries]

            async def process_all_queries():
                semaphore = asyncio.Semaphore(2)  # Limite de concorrência
                
                async def process_query(query):
                    async with semaphore:
                        return await YoutubeSearch.search(query)
                
                tasks = [process_query(query) for query in queries]
                return await asyncio.gather(*tasks)

            results = async_to_sync(process_all_queries)()
            return Response(data=results, status=200)
            
        except Exception as e:
            return Response({"error": "Internal server error"}, status=500)