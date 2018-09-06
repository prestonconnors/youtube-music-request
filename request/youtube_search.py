"""YouTube Search API"""

import requests
import requests_cache

import keys

YOUTUBE_API_KEY = keys.YOUTUBE_API_KEY

def youtube_search(query_term, safesearch, related_to=False):
    """YouTube Search"""
    if not related_to:
        payload = {'part': 'snippet',
                   'key': YOUTUBE_API_KEY,
                   'q': query_term,
                   'safeSearch': safesearch,
                   'type': 'video',
                   'videoCategoryId': 10,
                   'videoEmbeddable': 'true'
                  }

    else:
        payload = {'part': 'snippet',
                   'key': YOUTUBE_API_KEY,
                   'relatedToVideoId': query_term,
                   'safeSearch': safesearch,
                   'type': 'video'
                  }

    requests_cache.install_cache()
    response = requests.get('https://www.googleapis.com/youtube/v3/search', params=payload)
    results = []
    for item in response.json()['items']:
        video_id = item['id']['videoId']
        title = item['snippet']['title']
        thumbnail = item['snippet']['thumbnails']['default']['url']
        results.append({'videoId': video_id,
                        'title': title,
                        'thumbnail': thumbnail})

    return results


