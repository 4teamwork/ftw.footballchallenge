from sqlalchemy import Column, Integer, String
from ftw.footballchallenge import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from zope.interface import implements
from ftw.footballchallenge.interfaces import ILeague
from Acquisition.interfaces import IAcquirer
from datetime import date
from ftw.footballchallenge.event import Event
from z3c.saconfig import named_scoped_session
from zope.schema.interfaces import IVocabularyFactory
from zope.schema import vocabulary


class League(Base):
    """Modeldefinition for League"""
    __tablename__='leagues'

    #implement the Markerinterface
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

class LeagueVocabularyFactory(object):

    implements(IVocabularyFactory)

    def __call__(self, context):
        """a Proxy function which returns keeper term"""
        session = named_scoped_session("footballchallenge")
        event_id = session.query(Event).filter(Event.LockDate > date.today()).one().id_s
        leagues = session.query(League).filter(League.event_id == event_id).all()
        terms = []
        for league in leagues:
            terms.append(vocabulary.SimpleTerm(league.id_, league.id_, league.name))
        return vocabulary.SimpleVocabulary(terms)
