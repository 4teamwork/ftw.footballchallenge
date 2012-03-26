from sqlalchemy import Column, Integer, DateTime
from ftw.footballchallenge import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref


class Teamstatistics(Base):
    __tablename__='teamstatistics'

    player_id = Column(Integer, ForeignKey('players.id'), primary_key=True,
                       nullable=False)
    game_id = Column(Integer, ForeignKey('games.id'), primary_key=True,
                     nullable=False)
    points = Column(Integer, nullable=False)
    total_points = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)

    game = relationship("Game", backref=backref('teamstatistics',
                        order_by=game_id))
    player = relationship("Player", backref=backref('teamstatistics',
                          order_by=player_id))

    def __init__(self, player_id, game_id, points, total_points):
        self.player_id = player_id
        self.game_id = game_id
        self.points = points
        self.total_points = total_points

    def __repr__(self):
        return '<Statistics for Team %s. Total Points: %s>' % (self.player,
            self.game)
