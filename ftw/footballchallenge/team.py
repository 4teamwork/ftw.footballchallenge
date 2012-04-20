from sqlalchemy import Column, Integer, String, Table
from ftw.footballchallenge import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from zope.interface import implements
from ftw.footballchallenge.interfaces import ITeam
from zope.schema.interfaces import IVocabularyFactory
from zope.schema import vocabulary
from z3c.saconfig import named_scoped_session

leagues_teams = Table('leagues_teams', Base.metadata,
    Column('team_id', Integer, ForeignKey('teams.id')),
    Column('league_id', Integer, ForeignKey('leagues.id')))

class Team(Base):
    """Modeldefintion for Team"""
    __tablename__='teams'

    implements(ITeam)

    id_ = Column('id', Integer, primary_key=True)
    name = Column(String(45))
    user_id = Column('user_id', String(40), nullable=False)

    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)
    leagues = relationship('League', secondary=leagues_teams, backref='teams')

    players = relationship('Teams_Players', backref='team')
    event = relationship('Event', backref='teams')

    def __init__(self, name, user_id, event_id, league_id=None):
        self.name = name
        self.user_id = user_id
        self.league_id = league_id
        self.event_id = event_id

    def __repr__(self):
        return '<Team %s>' % self.name



class TeamVocabularyFactory(object):

    implements(IVocabularyFactory)

    def __call__(self, context):
        """a Proxy function which returns keeper term"""
        session = named_scoped_session('footballchallenge')
        teams = session.query(Team).filter(Team.event_id == context.event_id).all()
        terms = []
        for team in teams:
            terms.append(vocabulary.SimpleTerm(team.id_, team.id_, team.name))
        return vocabulary.SimpleVocabulary(terms)