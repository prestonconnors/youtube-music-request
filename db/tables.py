"""Define tables for SQL Alchemy."""

from sqlalchemy import Column, Boolean, Integer, String, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import PasswordType

class Establishment(declarative_base()): # pylint: disable=R0903
    """Establishment table."""
    __tablename__ = 'establishment'

    id = Column(Integer, primary_key=True) # pylint: disable=C0103
    name = Column(String)
    password = Column(PasswordType(schemes=['bcrypt']))
    request_limit = Column(Integer)
    repeat_limit = Column(Integer)
    request_duration_limit = Column(Integer)
    requester_safesearch = Column(String)
    autoplay_safesearch = Column(String)
    confirm = None
    tos_accepted = Column(Boolean)

class Request(declarative_base()): # pylint: disable=R0903
    """Request table."""
    __tablename__ = 'request'

    id = Column(Integer, primary_key=True) # pylint: disable=C0103
    establishment_id = Column(Integer)
    requester_id = Column(Integer)
    video_id = Column(String)
    state = Column(Integer)
    requested_time = Column(String, default=func.now())

class Requester(declarative_base()): # pylint: disable=R0903
    """Requester table."""
    __tablename__ = 'requester'

    id = Column(Integer, primary_key=True) # pylint: disable=C0103
    created_time = Column(String, default=func.now())