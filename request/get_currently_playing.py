from sqlalchemy import and_, exists

from db.session import session as db_session
from db.tables import Request
from request.youtube_list import youtube_list


def get_currently_playing(establishment_id):
    """See if video was already requested."""
    session = db_session()
    result = session.query(Request.video_id).\
                            filter(Request.establishment_id == establishment_id,
                                   Request.state == 1).first()
    session.close()

    if result:
        return youtube_list([result[0]])[0]
    else:
        return None