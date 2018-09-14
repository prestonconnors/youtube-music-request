"""YouTube Search API"""

import requests
import requests_cache

from isodate import parse_duration

import keys

YOUTUBE_API_KEY = keys.YOUTUBE_API_KEY


def youtube_list(video_ids):
    """YouTube List API"""
    payload = {'id': ','.join(video_ids),
               'part': 'contentDetails,snippet',
               'key': YOUTUBE_API_KEY,
              }
    requests_cache.install_cache('youtube_list')
    response = requests.get('https://www.googleapis.com/youtube/v3/videos', params=payload)

    results = []
    for item in response.json()['items']:
        video_id = item['id']
        title = item['snippet']['title']
        duration = parse_duration(item['contentDetails']['duration']).total_seconds()
        thumbnail = item['snippet']['thumbnails']['default']['url']
        definition = item['contentDetails']['definition']
        results.append({'videoId': video_id,
                        'title': title,
                        'duration': duration,
                        'thumbnail': thumbnail,
                        'definition': definition})
    return results


