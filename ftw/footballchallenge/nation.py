from sqlalchemy import Column, Integer, String
from ftw.footballchallenge import Base
from zope.schema import vocabulary
from z3c.saconfig import named_scoped_session
from zope.schema.interfaces import IVocabularyFactory
from zope.interface import implements
from ftw.footballchallenge.interfaces import INation
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref


class Nation(Base):
    "Model definition for Nation"
    __tablename__='nations'

    implements(INation)
    id_ = Column('id', Integer, primary_key=True)
    name = Column(String(45))
    country = Column(String(3))
    coach = Column(String(64))
    participations = Column(Integer)
    fifa_rank = Column(Integer)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)
    event = relationship("Event", backref=backref('nations', order_by=id_))


    def __init__(self, name, event_id):
        self.name = name
        self.event_id = event_id

    def __repr__(self):
        return '<Nation %s>' % self.name


class NationVocabularyFactory(object):
    
    implements(IVocabularyFactory)

    def __call__(self,context):
        session = named_scoped_session('footballchallenge')
        terms=[]
        nations = session.query(Nation).all()
        for nation in nations:
            terms.append(vocabulary.SimpleTerm(nation.id_, nation.id_,
                                               nation.name))
        return vocabulary.SimpleVocabulary(terms)
