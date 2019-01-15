"""YouTube Search API"""

import requests
import requests_cache

from flask import jsonify
from flask_restful import Resource

import keys

YOUTUBE_API_KEY = keys.YOUTUBE_API_KEY


class YouTubeSearchAPI(Resource):
    def get(self, search_term):
        results = []

        for song_type in ['karaoke', 'regular']:
            if song_type == 'karaoke':
                extra_search_terms = ' karaoke'
            else:
                extra_search_terms = ''

            payload = {'part': 'snippet',
                       'key': YOUTUBE_API_KEY,
                       'q': search_term + extra_search_terms,
                       'safeSearch': 'moderate',
                       'type': 'video',
                       'videoCategoryId': 10,
                       'videoEmbeddable': 'true'
                       }
            print(payload)

            requests_cache.install_cache('youtube_search', expire_after=86400)
            response = requests.get('https://www.googleapis.com/youtube/v3/search', params=payload)
            for item in response.json()['items']:
                video_id = item['id']['videoId']
                title = item['snippet']['title']
                thumbnail = item['snippet']['thumbnails']['default']['url']
                results.append({'videoId': video_id,
                                'title': title,
                                'thumbnail': thumbnail,
                                'song_type': song_type})

        return jsonify(results)
