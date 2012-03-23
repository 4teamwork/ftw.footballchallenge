from sqlalchemy import Column, Integer, String
from ftw.footballchallenge import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Table


player_team = Table('player_team', Base.metadata,
    Column('team_id', Integer, ForeignKey('teams.id')),
    Column('player_id', Integer, ForeignKey('players.id')))



class Team(Base):
    __tablename__='teams'
    
    id_ = Column('id', Integer, primary_key=True)
    name = Column(String(45))
    user_id = Column('user_id', String(40), nullable=False)

    league_id = Column(Integer, ForeignKey('leagues.id'), nullable=True)
    league = relationship("League", backref=backref('leagues', order_by=id_))

    players = relationship('Player', secondary=player_team, backref='teams')

    def __init__(self, name, user_id, league_id=None):
        self.name = name
        self.user_id = user_id
        self.league_id = league_id

    def __repr__(self):
        return '<Team %s>' % self.name