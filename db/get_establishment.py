from sqlalchemy import inspect

from db.session import session as db_session
from db.tables import Establishment

def get_establishment(establishment_id=None, name=None):
    """Get establishment info"""

    session = db_session()

    if establishment_id:
        result = session.query(Establishment).filter(Establishment.id == establishment_id).first()
        return(object_as_dict(result))
    if name:
        result = session.query(Establishment).filter(Establishment.name == name).first()
        return(object_as_dict(result))

def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}
