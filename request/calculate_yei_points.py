from datetime import datetime
from sqlalchemy import and_, exists


from db.session import session as db_session
from db.tables import AdditionalRequestInformation
from request.youtube_list import youtube_list


def calculate_yei_points(base_points=500, max_points=2500):
    """See if video was already requested."""
    now = datetime.utcnow()
    session = db_session()
    db_result = session.query(AdditionalRequestInformation).\
                         order_by(AdditionalRequestInformation.requested_time.desc()).\
                         first()
    session.close()

    requested_time = datetime.strptime(db_result.requested_time, '%Y-%m-%d %H:%M:%S')
    yei_points = int(round(base_points + ((now - requested_time).total_seconds() * .5)))
    if yei_points > max_points:
        return max_points
    else:
        return yei_points
