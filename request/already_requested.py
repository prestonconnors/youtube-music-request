from sqlalchemy import and_, exists

from server.db.session import session as db_session
from server.db.tables import Request


def already_requested(establishment_id, video_id):
    """See if video was already requested."""
    session = db_session()
    result = session.query(exists().where(and_(Request.video_id == video_id,
                                               Request.establishment_id == establishment_id,
                                               Request.state.in_([0, 1])))).scalar()
    session.close()

    return result