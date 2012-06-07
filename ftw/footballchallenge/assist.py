from sqlalchemy import Column, Integer, Boolean
from ftw.footballchallenge import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref


class Assist(Base):
    """Modeldefinition for assists"""
    __tablename__='assists'

    id_ = Column('id', Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    game_id = Column(Integer, ForeignKey('games.id'), nullable=False)

    game = relationship("Game", backref=backref('assists', order_by=id_))
    player = relationship("Player", backref=backref('assists', order_by=id_))

    def __init__(self, player_id, game_id):
        self.player_id = player_id
        self.game_id = game_id

    def __repr__(self):
        return '<Assist %s, %s>' % (self.player.name, self.game_id)
