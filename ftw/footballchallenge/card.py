from sqlalchemy import Column, Integer, String
from ftw.footballchallenge import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref


class Card(Base):
    __tablename__='cards'

    id_ = Column('id', Integer, primary_key=True)
    color = Column(String(20), nullable=False)

    player_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    game_id = Column(Integer, ForeignKey('games.id'), nullable=False)

    player = relationship("Player", backref=backref('cards', order_by=id_))
    game = relationship("Game", backref=backref('cards', order_by=id_))

    def __init__(self, player_id, game_id, color):
        self.player_id = player_id
        self.game_id = game_id
        self.color = color

    def __repr__(self):
        return '<Card %s, %s, %s>' % (self.player.name, self.game_id,
                                      self.color)
