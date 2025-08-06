import asyncio
import json
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from asgiref.sync import async_to_sync
from yt_dlp import YoutubeDL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DummyLogger:
    def debug(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): pass

class YoutubeSearch:
    @staticmethod
    async def search(query):
        try:
            logger.info(f"Searching for: {query}")
            ydl_opts = {
                'quiet': True,
                'extract_flat': True,
                'force_generic_extractor': True,
                'logger': DummyLogger(),
                'no_warnings': True,
            }
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"ytsearch1:{query}", download=False)
                if 'entries' in info and len(info['entries']) > 0:
                    url = info['entries'][0]['url']
                    logger.info(f"Found URL: {url}")
                    return url
            logger.warning(f"No entries found for: {query}")
            return None
        except Exception as e:
            logger.exception(f"Error during YouTube search for '{query}'")
            return None

class YoutubeCrawler(APIView):
    def post(self, request):
        try:
            logger.info(f"HEADERS: {dict(request.headers)}")
            logger.info(f"BODY: {request.body}")

            data = json.loads(request.body)
            queries = data.get("search_data", [])

            if not queries:
                return Response({"error": "Missing search_data"}, status=400)

            if isinstance(queries, str):
                queries = [queries]

            async def process_all_queries():
                semaphore = asyncio.Semaphore(2)

                async def process_query(query):
                    async with semaphore:
                        return await YoutubeSearch.search(query)

                tasks = [process_query(query) for query in queries]
                return await asyncio.gather(*tasks)

            results = async_to_sync(process_all_queries)()
            filtered_results = [r for r in results if r is not None]

            logger.info(f"Final results: {filtered_results}")

            return Response(data=filtered_results, status=200)

        except Exception:
            logger.exception("Internal server error")
            return Response({"error": "Internal server error"}, status=500)