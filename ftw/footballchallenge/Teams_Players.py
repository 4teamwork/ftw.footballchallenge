from sqlalchemy import Column, Integer, String, Boolean
from ftw.footballchallenge import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Teams_Players(Base):
    __tablename__='teams_players'
    
    team_id = Column('team_id', Integer, ForeignKey('teams.id'), primary_key=True, nullable=False)
    player_id = Column('player_id', Integer, ForeignKey('players.id'), primary_key=True, nullable=False)
    is_starter = Column('is_starter', Boolean)
    player = relationship("Player", backref="teams")


    def __init__(self, player, is_starter):
        self.is_starter = is_starter
        self.player = player
    
    
