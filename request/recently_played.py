from sqlalchemy import and_, exists

from server.db.session import session as db_session
from server.db.tables import Request


def recently_played(establishment_id, video_id, repeat_limit):
    """See if video was already requested."""
    session = db_session()
    results = session.query(Request.video_id).\
                      filter(Request.establishment_id == establishment_id, Request.state == 2).\
                      order_by(Request.requested_time.desc()).\
                      limit(repeat_limit)
    session.close()
    video_ids = [_[0] for _ in results]
    if video_id in video_ids:
        return True
    else:
        return False
