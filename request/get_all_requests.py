from sqlalchemy import select
from sqlalchemy.sql.expression import func

from db.session import session as db_session
from db.tables import Request
from request.youtube_list import youtube_list


def get_all_requests(establishment_id):
    """See if video was already requested."""
    session = db_session()
    results = session.query(select([Request.video_id, func.max(Request.state)]).\
                            where(Request.establishment_id == establishment_id).\
                            group_by(Request.video_id)).all()
    session.close()

    video_ids_state = [{_[0]: _[1]}  for _ in results]
    video_data = []
    for chunk in chunks(list(set().union(*(d.keys() for d in video_ids_state))), 50):
        video_data += youtube_list(chunk)

    for video in video_data:
        video_id = video['videoId']
        state = [s[video_id] for s in video_ids_state if video_id in s][0]
        video['state'] = state
    return video_data

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]
