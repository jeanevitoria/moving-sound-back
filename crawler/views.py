from django.shortcuts import render
from django.http import HttpResponse
import asyncio
from crawl4ai import *
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

async def crawler(videoInfo):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=f"https://www.youtube.com/results?search_query={videoInfo}",
        )
        print(result.markdown)
        return result.markdown

class YoutubeCrawler(APIView):
    def post(self, request):
        data = json.loads(request.body)
        query = data.get("search_data")
        
        markdown = asyncio.run(crawler(query))
        return Response(data=markdown.json(), status=200)
