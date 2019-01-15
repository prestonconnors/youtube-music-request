from sqlalchemy import and_, exists

from db.session import session as db_session
from db.tables import Request
from request.youtube_list import youtube_list


def get_requests(establishment_id):
    """See if video was already requested."""
    session = db_session()
    db_results = session.query(Request).\
                         filter(Request.establishment_id == establishment_id,
                                Request.state == 0)
    session.close()

    youtube_results = youtube_list([_.video_id  for _ in db_results])

    results = []

    for db_result in db_results:
        for youtube_result in youtube_results:
            if db_result.video_id == youtube_result['videoId']:
                db_result.youtube = youtube_result
                results.append(db_result)

    return results