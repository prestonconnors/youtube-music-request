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

    '''requests_cache.install_cache('youtube_playlistitems', expire_after=86400)
    response = requests.get('https://www.googleapis.com/youtube/v3/playlistItems', params=payload)
    results = []
    for item in response.json()['items']:
        video_id = item['snippet']['resourceId']['videoId']
        results.append(video_id)'''
    return ["fyNgFKWNJFs","x3bfa3DZ8JM","0jMPXRDYpkQ","ZAfAud_M_mg","pbMwTqkKSps","gl1aHhXnN1k","ApXoWvfEYVU","ajN57m_OSpY","7w4Udbys4O4","U68MJz9DrI4","W16bk86xIY0","rsuKmbYokuk","b63IPrrdPOU","ixkoVwKQaJg","aJOTlE1K90k","OSUxrSe5GbI","6ONRf7h3Mdk","zUOh09GoQgk","kg1BljLu9YY","bo_efYhYU2A","XCQK6LmhYqc","56WBK4ZK_cw","kxloC1MKTpg","m7Bc3pLyij0","LdH7aFjDzjI","kN0iD0pI3o0","mzB1VGEGcSU","BDocp-VpCwY","AX3Bsiq-13k","A9hcJgtnm6Q","Uk1hv6h7O1Y","IPXIgEAGe4U","7_rftpd0u0U","nuckTcoZG4Q","SAWzXkV3hHo","kkLk2XWMBf8","Q4-jOuHO-z4","77RmU8QcM4k","WXBHCQYxwr0","yNXDxUQ4c9U","vB67ddBhO1c","Sc97AUImI04","k73EBmeJ950","KfXvjxbRhZk","6-v1b9waHWY","3dP6pyWe30Y","EQnk-h-LCpQ","uF9YayOgjRg","fKtY_37r1VI","JudqK1hL18w","iI2f8eA8x4Q","-MZ8guTxcFU","B1dmRjyN0CQ","iJUM11goXAU","kudi8OtMu9s","njwXRJDNpbQ","50VNCymT-Cs","t1YHv1wHAxo","qr1-WpWOUk8","CQVNGp0qrLg","ZZhwwtr0n40","HZoX-10-VMs","hW3MN8Jt4g4","u5kP_nfFVt4","MN83XL_a50Q","ZHl4_qJnuAM","yaXAMuhIe7Y","qA7hsFLvepc","a2HF7WRXib8","0A5xm0VLBXE"]

    return results


