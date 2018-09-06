from sqlalchemy import and_, exists

from db.session import session as db_session
from db.tables import Request
from request.youtube_list import youtube_list


def get_requests(establishment_id):
    """See if video was already requested."""
    session = db_session()
    results = session.query(Request.video_id).\
                            filter(Request.establishment_id == establishment_id,
                                   Request.state == 0)
    session.close()

    video_ids = [_[0]  for _ in results]
    return youtube_list(video_ids)