""" Monitoring application models.
"""
from sqlalchemy import Column, Integer, DateTime, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class PingModel(Base):
    """ Defines a model for storing pings to the site.
    """
    __tablename__ = 'pings'

    id = Column(Integer, primary_key=True)
    site_url = Column(String(200), nullable=False, default='')
    response_code = Column(Integer, nullable=False, index=True)
    response_time = Column(Integer, nullable=False)
    response_size = Column(Integer, nullable=False)
    success = Column(Boolean, nullable=False)
    date_added = Column(DateTime(timezone=True), nullable=False)
