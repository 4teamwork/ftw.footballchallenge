from sqlalchemy import Column, Integer, String, DateTime
from ftw.footballchallenge import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Table


players_played = Table('players_played', Base.metadata,
    Column('game_id', Integer, ForeignKey('games.id')),
    Column('player_id', Integer, ForeignKey('players.id')))


class Game(Base):
    __tablename__='games'

    id_ = Column('id', Integer, primary_key=True)

    nation1_id = Column(Integer, ForeignKey('nations.id'), nullable=False)
    nation2_id = Column(Integer, ForeignKey('nations.id'), nullable=False)
    result = Column(String(5))
    date = Column(DateTime, nullable=False)
    events_id = Column(Integer, ForeignKey('events.id'), nullable=False)

    event = relationship("Event", backref=backref('games', order_by=id_))

    nation1 = relationship("Nation",
                           primaryjoin="Nation.id_==Game.nation1_id",
                           backref=backref('games.nation1_id', order_by=id_))
    nation2 = relationship("Nation",
                           primaryjoin="Nation.id_==Game.nation2_id",
                           backref=backref('games.nation2_id', order_by=id_))

    players = relationship('Player', secondary=players_played, backref='games')

    def __init__(self, nation1_id, nation2_id, date, events_id, result=None):
        self.nation1_id = nation1_id
        self.nation2_id = nation2_id
        self.date = date
        self.events_id = events_id

    def __repr__(self):
        return '<Game %s vs. %s>' % (self.nation1.name, self.nation2.name)
