from sqlalchemy import Column, Integer, String
from ftw.footballchallenge import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from zope.interface import implements
from ftw.footballchallenge.interfaces import ILeague

class League(Base):
    __tablename__='leagues'

    implements(ILeague)
    
    id_ = Column('id', Integer, primary_key=True)
    name = Column(String(45))

    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)

    event = relationship("Event", backref=backref('leagues', order_by=id_))

    def __init__(self, name, event_id):
        self.name = name
        self.event_id = event_id

    def __repr__(self):
        return '<League %s>' % self.name
