from sqlalchemy import Column, Integer, Boolean
from ftw.footballchallenge import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref


class Goal(Base):
    """Modeldefinition for goal"""
    __tablename__='goals'

    id_ = Column('id', Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    game_id = Column(Integer, ForeignKey('games.id'), nullable=False)
    is_penalty = Column(Boolean, nullable=False)

    game = relationship("Game", backref=backref('goals', order_by=id_))
    player = relationship("Player", backref=backref('goals', order_by=id_))

    def __init__(self, player_id, game_id, is_penalty=False):
        self.player_id = player_id
        self.game_id = game_id
        self.is_penalty = is_penalty

    def __repr__(self):
        return '<Goal %s, %s>' % (self.player.name, self.game_id)
