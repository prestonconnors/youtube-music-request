from server.db.session import session as db_session
from server.db.tables import Request


def request_amount(requester_id):
    print(requester_id)
    session = db_session()
    amount = session.query(Request).filter(Request.requester_id == requester_id,
                                           Request.state == 0).count()
    return amount