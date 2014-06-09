from sqlalchemy import Column, Integer, Boolean
from ftw.footballchallenge import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Teams_Players(Base):
    """Modeldefinition for TeamsPlayers. This is a 	junction table"""
    __tablename__ = 'teams_players'

    team_id = Column('team_id', Integer, ForeignKey('teams.id'),
                     primary_key=True, nullable=False)
    player_id = Column('player_id', Integer, ForeignKey('players.id'),
                       primary_key=True, nullable=False)
    is_starter = Column('is_starter', Boolean)
    field_pos = Column(Integer)

    player = relationship("Player", backref="teams")

    def __init__(self, team_id, player, is_starter, field_pos=0):
        self.team_id = team_id
        self.is_starter = is_starter
        self.player = player
        self.field_pos = field_pos
