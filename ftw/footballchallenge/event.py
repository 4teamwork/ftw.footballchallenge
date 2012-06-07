from sqlalchemy import Column, Integer, String, DateTime
from ftw.footballchallenge import Base
from zope.schema import vocabulary
from z3c.saconfig import named_scoped_session
from zope.interface import alsoProvides
from zope.schema.interfaces import IContextSourceBinder
from zope.interface import implements
from ftw.footballchallenge.interfaces import IEvent
from zope.schema.interfaces import IVocabularyFactory


class Event(Base):
    """Modeldefinition for Event"""
    __tablename__='events'
    
    implements(IEvent)

    id_ = Column('id', Integer, primary_key=True)
    name = Column(String(45))
    deadline = Column(DateTime)

    def __init__(self, name, deadline):
        self.name = name
        self.deadline = deadline

    def __repr__(self):
        return '<Event %s>' % self.name


class EventVocabularyFactory(object):
    
    implements(IVocabularyFactory)

    def __call__(self, context):
        """Returns the Events as SimpleVocabulary to use it as Source for fields"""
        session = named_scoped_session('footballchallenge')
        terms=[]
        events = session.query(Event).all()
        for event in events:
            terms.append(vocabulary.SimpleTerm(event.id_, event.id_, event.name))
        return vocabulary.SimpleVocabulary(terms)
