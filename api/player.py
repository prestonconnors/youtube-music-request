"""Player API"""

from flask_restful import Resource
from random import sample
from sqlalchemy import and_, exists

from db.get_establishment import get_establishment
from db.session import session as db_session
from db.tables import Request
from request.validate_request import validate_request
from request.youtube_playlistitems import youtube_playlistitems
from request.youtube_search import youtube_search

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
                playlist_video_ids = youtube_playlistitems('PLBSQz25Ioz5Wo8KKaOLtpj224vD27_97P')
                played_video_ids = session.query(Request.video_id).\
                                           filter_by(establishment_id=establishment_id, state=2)
                played_video_ids = [_[0] for _ in played_video_ids]
                played_video_ids = sample(played_video_ids, int(len(playlist_video_ids) * .3))
                video_ids = playlist_video_ids + played_video_ids
                

                valid = False
                while not valid:
                    video_id = choice(video_ids)
                    valid, message = validate_request(0, establishment_id, video_id)
                    if not valid:
                        results = youtube_search(video_id,
                                                 establishment['autoplay_safesearch'],
                                                 related_to=True)
                        if results:
                            video_id = choice(results)['videoId']
                            valid, message = validate_request(0, establishment_id, video_id)

                session = db_session()
                session.add(Request(establishment_id=establishment_id,
                                    requester_id=0,
                                    video_id=video_id,
                                    state=0))
                session.commit()

        elif action == 'skip':
            state = session.query(Request.state)\
                           .filter_by(establishment_id=establishment_id, video_id=video_id)\
                           .order_by(Request.requested_time.desc())\
                           .limit(1)\
                           .scalar()

            if state not in [3, 4]:
                value = False
            else:
                value = True

        session.commit()
        session.close()
        return {'establishment_id': establishment_id,
                'action': action,
                'value': value,
                'video_id': video_id,
                'status': 'OK'}
