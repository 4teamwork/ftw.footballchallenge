from sqlalchemy import Column, Integer, String
from ftw.footballchallenge import Base
from zope.schema import vocabulary
from z3c.saconfig import named_scoped_session
from zope.interface import alsoProvides
from zope.schema.interfaces import IContextSourceBinder


class Nation(Base):
    "Modeldeifition for Nation"
    __tablename__='nations'

    id_ = Column('id', Integer, primary_key=True)
    name = Column(String(45))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Nation %s>' % self.name


def get_nations_term(context):
    session = named_scoped_session('footballchallenge')
    terms=[]
    nations = session.query(Nation).all()
    for nation in nations:
        terms.append(vocabulary.SimpleTerm(nation.id_, nation.id_,
                                           nation.name))
    return vocabulary.SimpleVocabulary(terms)
alsoProvides(get_nations_term, IContextSourceBinder)
