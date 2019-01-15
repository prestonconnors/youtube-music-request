"""Player API"""

from flask_restful import Resource
from random import sample
from sqlalchemy import and_, exists

from db.get_establishment import get_establishment
from db.session import session as db_session
from db.tables import Request
from request.calculate_yei_points import calculate_yei_points
from request.get_requests import get_requests
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
        additional_request_information = {}
        youtube = {}
        establishment = get_establishment(establishment_id)
        establishment.pop('password', None)

        if action == 'playing':
            session.query(Request).filter_by(establishment_id=establishment_id,
                                             state=1).update({'state': 2})
            session.commit()
            session.query(Request).filter_by(establishment_id=establishment_id,
                                             video_id=video_id,
                                             state=0).update({'state': 1})

        elif action == 'next':
            row = session.query(Request)\
                         .filter_by(establishment_id=establishment_id, state=0)\
                         .order_by(Request.requested_time)\
                         .first()

            if row:
                request = {c.name: getattr(row, c.name) for c in row.__table__.columns}
                if row.additional_request_information:
                    additional_request_information = {c.name: getattr(row.additional_request_information, c.name) for c in row.additional_request_information.__table__.columns}
                video_id = request['video_id']

            else:
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

        elif action == 'requests':
            requests =  get_requests(establishment_id)

            if len(requests) > 0:
                request = {c.name: getattr(requests[0], c.name) for c in requests[0].__table__.columns}
                if requests[0].additional_request_information:
                    additional_request_information = {c.name: getattr(requests[0].additional_request_information, c.name) for c in requests[0].additional_request_information.__table__.columns}

                youtube = requests[0].youtube
            else:
                value = False

        elif action == 'yei':
            value = calculate_yei_points()

        session.commit()
        session.close()
        response = self.merge_two_dicts(establishment, additional_request_information)
        response = self.merge_two_dicts(response, youtube)
        response = self.merge_two_dicts(response, {'action': action, 'value': value, 'video_id': video_id, 'status': 'OK'})
        
        return response

    def merge_two_dicts(self, x, y):
        z = x.copy()   # start with x's keys and values
        z.update(y)    # modifies z with y's keys and values & returns None
        return z

