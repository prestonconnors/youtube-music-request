"""Define tables for SQL Alchemy."""

from sqlalchemy import Column, Boolean, Integer, ForeignKey, String, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy_utils import PasswordType

Base = declarative_base()

class Establishment(Base): # pylint: disable=R0903
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
    mode = Column(String)
    confirm = None
    tos_accepted = Column(Boolean)

class Request(Base): # pylint: disable=R0903
    """Request table."""
    __tablename__ = 'request'

    id = Column(Integer, primary_key=True) # pylint: disable=C0103
    establishment_id = Column(Integer)
    requester_id = Column(Integer)
    video_id = Column(String)
    state = Column(Integer)
    requested_time = Column(String, default=func.now())
    additional_request_information = relationship('AdditionalRequestInformation', uselist=False, back_populates="request")

class Requester(Base): # pylint: disable=R0903
    """Requester table."""
    __tablename__ = 'requester'

    id = Column(Integer, primary_key=True) # pylint: disable=C0103
    created_time = Column(String, default=func.now())

class AdditionalRequestInformation(Base): # pylint: disable=R0903
    """Additional Request Information table."""
    __tablename__ = 'additional_request_information'

    id = Column(Integer, primary_key=True) # pylint: disable=C0103
    request_id = Column(Integer, ForeignKey('request.id'))
    requested_by = Column(String, default=None)
    dedicated_to = Column(String, default=None)
    performer = Column(String, default=None)
    requested_time = Column(String, default=func.now())
    request = relationship('Request', back_populates='additional_request_information')