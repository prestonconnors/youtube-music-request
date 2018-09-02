"""Player API"""

from flask_restful import Resource
from sqlalchemy import and_, exists

from server.db.get_establishment import get_establishment
from server.db.session import session as db_session
from server.db.tables import Request
from server.request.validate_request import validate_request
from server.request.youtube_search import youtube_search

from random import choice

class PlayerAPI(Resource):
    """Player API"""
    def get(self, establishment_id, action, video_id=None):
        """GET call to API"""
        session = db_session()
        value = True

        if action == 'playing':
            session.query(Request).filter_by(establishment_id=establishment_id,
                                             state=1).update({'state': 2})
            session.commit()
            session.query(Request).filter_by(establishment_id=establishment_id,
                                             video_id=video_id,
                                             state=0).update({'state': 1})

        elif action == 'next':
            video_id = session.query(Request.video_id)\
                              .filter_by(establishment_id=establishment_id, state=0)\
                              .order_by(Request.requested_time)\
                              .limit(1)\
                              .scalar()

            if not video_id:
                establishment = get_establishment(establishment_id)
                video_ids = session.query(Request.video_id).\
                                    filter_by(establishment_id=establishment_id, state=2)

                valid = False
                while not valid:
                    video_id = choice([_[0] for _ in video_ids])
                    valid, message = validate_request(0, establishment_id, video_id)
                    if not valid:
                        video_id = choice(youtube_search(video_id,
                                                         establishment['safesearch'],
                                                         related_to=True))['videoId']
                        valid, message = validate_request(0, establishment_id, video_id)
                    print(valid, message)


                session = db_session()
                session.add(Request(establishment_id=establishment_id,
                                    requester_id=0,
                                    video_id=video_id,
                                    state=0))
                session.commit()

        elif action == 'skip':
            value = session.query(exists()\
                           .where(and_(Request.establishment_id == establishment_id,
                                       Request.video_id == video_id,
                                       Request.state.in_([3, 4]))))\
                           .scalar()


        session.commit()
        session.close()
        return {'establishment_id': establishment_id,
                'action': action,
                'value': value,
                'video_id': video_id,
                'status': 'OK'}
