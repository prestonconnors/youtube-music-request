from sqlalchemy.sql.expression import func

from server.db.session import session as db_session
from server.db.tables import Requester


def new_requester_id():
    session = db_session()
    id = session.query(func.max(Requester.id)).scalar()
    if not id:
        id = 0
    id += 1
    session.add(Requester(id=id))
    session.commit()
    session.close()
    return id