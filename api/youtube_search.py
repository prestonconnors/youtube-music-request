"""YouTube Search API"""

import requests

from flask import jsonify
from flask_restful import Resource

import server.keys

YOUTUBE_API_KEY = server.keys.YOUTUBE_API_KEY

class YouTubeSearchAPI(Resource):
    """YouTube Search API"""
    def get(self, search_term):
        """GET call to API"""
        payload = {'part': 'snippet',
                   'key': YOUTUBE_API_KEY,
                   'q': search_term,
                   'safeSearch': 'moderate',
                   'type': 'video',
                   'videoCategoryId': 10,
                   'videoEmbeddable': 'true'
                  }
        response = requests.get('https://www.googleapis.com/youtube/v3/search', params=payload)
        results = []
        for item in response.json()['items']:
            video_id = item['id']['videoId']
            title = item['snippet']['title']
            thumbnail = item['snippet']['thumbnails']['default']['url']
            results.append({'videoId': video_id,
                            'title': title,
                            'thumbnail': thumbnail})

        return jsonify(results)



