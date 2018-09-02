"""YouTube Search API"""

import requests

from isodate import parse_duration

import server.keys

YOUTUBE_API_KEY = server.keys.YOUTUBE_API_KEY


def youtube_list(video_ids):
    """YouTube List API"""
    payload = {'id': ','.join(video_ids),
               'part': 'contentDetails,snippet',
               'key': YOUTUBE_API_KEY,
              }
    response = requests.get('https://www.googleapis.com/youtube/v3/videos', params=payload)

    results = []
    for item in response.json()['items']:
        video_id = item['id']
        title = item['snippet']['title']
        duration = parse_duration(item['contentDetails']['duration']).total_seconds()
        results.append({'videoId': video_id,
                        'title': title,
                        'duration': duration})
    return results


