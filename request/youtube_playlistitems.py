"""YouTube Search API"""

import requests
import requests_cache

import keys

YOUTUBE_API_KEY = keys.YOUTUBE_API_KEY

def youtube_playlistitems(playlist_id):
    """YouTube Playlist Items"""
    payload = {'part': 'snippet',
               'maxResults': 50,
               'playlistId': playlist_id,
               'key': YOUTUBE_API_KEY
              }

    requests_cache.install_cache('youtube_playlistitems', expire_after=86400)
    response = requests.get('https://www.googleapis.com/youtube/v3/playlistItems', params=payload)
    results = []
    for item in response.json()['items']:
        video_id = item['snippet']['resourceId']['videoId']
        results.append(video_id)

    return results


