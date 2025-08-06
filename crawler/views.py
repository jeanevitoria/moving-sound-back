import asyncio
import json
import traceback
from rest_framework.views import APIView
from rest_framework.response import Response
from asgiref.sync import async_to_sync
from yt_dlp import YoutubeDL

class YoutubeSearch:
    @staticmethod
    async def search(query):
        try:
            print(f"Searching for: {query}")
            ydl_opts = {
                'quiet': True,
                'extract_flat': True,
                'force_generic_extractor': True,
            }
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"ytsearch1:{query}", download=False)
                if 'entries' in info and len(info['entries']) > 0:
                    url = info['entries'][0]['url']
                    print(f"Found URL: {url}")
                    return url
            print("No entries found")
            return None
        except Exception as e:
            print(f"Error during YouTube search for '{query}':")
            traceback.print_exc()
            return None

class YoutubeCrawler(APIView):
    def post(self, request):
        try:
            print("📥 HEADERS:", request.headers)
            print("📥 BODY:", request.body)

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

            filtered_results = [r for r in results if r is not None]
            print("🎯 Final results:", filtered_results)

            return Response(data=filtered_results, status=200)
        
        except Exception as e:
            print("🔥 Internal server error:")
            traceback.print_exc()
            return Response({"error": "Internal server error"}, status=500)