from sqlalchemy import Column, Integer, DateTime
from ftw.footballchallenge import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref


class Teamstatistics(Base):
    __tablename__='teamstatistics'

    team_id = Column(Integer, ForeignKey('teams.id'), primary_key=True,
                       nullable=False)
    game_id = Column(Integer, ForeignKey('games.id'), primary_key=True,
                     nullable=False)
    points = Column(Integer, nullable=False)
    total_points = Column(Integer, nullable=False)

    game = relationship("Game", backref=backref('teamstatistics',
                        order_by=game_id))
    team = relationship("Team", backref=backref('teamstatistics',
                          order_by=team_id))

    def __init__(self, team_id, game_id, points, total_points):
        self.team_id = team_id
        self.game_id = game_id
        self.points = points
        self.total_points = total_points


    def __repr__(self):
        return '<Statistics for Team %s. Total Points: %s>' % (self.team.name,
            self.total_points)
