from db.get_establishment import get_establishment
from request.banned import banned
from request.request_amount import request_amount
from request.already_requested import already_requested
from request.recently_played import recently_played
from request.youtube_list import youtube_list
from request.youtube_search import youtube_search

def validate_request(requester_id, establishment_id, video_id):
    """Validate if a request can be submitted."""
    establishment = get_establishment(establishment_id)
    list_results = youtube_list([video_id])

    if not list_results:
        return (False, u'{video_id} contains no YouTube data!'.format(video_id=video_id))
    else:
        list_results = list_results[0]

    if requester_id == 0:
        safesearch = establishment['autoplay_safesearch']
    else:
        safesearch = establishment['requester_safesearch']

    search_results = youtube_search(list_results['title'], safesearch)

    if request_amount(requester_id) >= establishment['request_limit'] and requester_id != 0:
        return (False, u'Wait until one of your requests play before submitting another request!')

    elif already_requested(establishment_id, video_id):
        return (False, u'{title} is currently requested!'.format(title=list_results['title']))

    elif recently_played(establishment_id, video_id, establishment['repeat_limit']):
        return (False, u'{title} has played too recently!'.format(title=list_results['title']))

    elif banned(establishment_id, video_id):
        return (False, u'{title} has been banned!'.format(title=list_results['title']))

    elif list_results['duration'] > establishment['request_duration_limit']:
        return (False, u'{title}\'s duration is too long!'.format(title=list_results['title']))

    elif list_results['definition'] != 'hd' and requester_id == 0:
        return (False, u'{title} is not in HD!'.format(title=list_results['title']))

    elif video_id not in [_['videoId'] for _ in search_results]:
        return (False, u'{title} contains mature content!'.format(title=list_results['title']))

    else:
        return (True, u'{title} has been requested!'.format(title=list_results['title']))
