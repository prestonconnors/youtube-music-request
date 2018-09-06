from sqlalchemy import and_, exists

from db.session import session as db_session
from db.tables import Request


def banned(establishment_id, video_id):
    """See if video was already requested."""
    session = db_session()
    result = session.query(exists().where(and_(Request.video_id == video_id,
                                               Request.establishment_id == establishment_id,
                                               Request.state == 4))).scalar()
    session.close()

    return result