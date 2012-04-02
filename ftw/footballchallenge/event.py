from sqlalchemy import Column, Integer, String, Date
from ftw.footballchallenge import Base
from zope.schema import vocabulary
from z3c.saconfig import named_scoped_session
from zope.interface import alsoProvides
from zope.schema.interfaces import IContextSourceBinder


class Event(Base):
    """Modeldefinition for Event"""
    __tablename__='events'


    id_ = Column('id', Integer, primary_key=True)
    name = Column(String(45))
    LockDate = Column(Date)

    def __init__(self, name, lockdate):
        self.name = name
        self.LockDate = lockdate

    def __repr__(self):
        return '<Event %s>' % self.name


def get_events_as_term(context):
    """Returns the Events as SimpleVocabulary to use it as Source for fields"""
    session = named_scoped_session('footballchallenge')
    terms=[]
    events = session.query(Event).all()
    for event in events:
        terms.append(vocabulary.SimpleTerm(event.id_, event.id_, event.name))
    return vocabulary.SimpleVocabulary(terms)
alsoProvides(get_events_as_term, IContextSourceBinder)
