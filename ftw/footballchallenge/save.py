from sqlalchemy import Column, Integer
from ftw.footballchallenge import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref


class Save(Base):
    __tablename__='saves'

    id_ = Column('id', Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    game_id = Column(Integer, ForeignKey('games.id'), nullable=False)

    player = relationship("Player", backref=backref('saves', order_by=id_))
    game = relationship("Game", backref=backref('saves', order_by=id_))

    def __init__(self, player_id, game_id):
        self.player_id = player_id
        self.game_id = game_id

    def __repr__(self):
        return '<Save %s, %s>' % (self.player, self.game_id)
