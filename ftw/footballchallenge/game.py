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
    score_nation1 = Column(Integer)
    score_nation2 = Column(Integer)
    date = Column(DateTime, nullable=False)
    events_id = Column(Integer, ForeignKey('events.id'), nullable=False)

    event = relationship("Event", backref=backref('games', order_by=id_))

    nation1 = relationship("Nation",
                           primaryjoin="Nation.id_==Game.nation1_id",
                           backref='games.nation1_id')
    nation2 = relationship("Nation",
                           primaryjoin="Nation.id_==Game.nation2_id",
                           backref='games.nation2_id')

    players = relationship('Player', secondary=players_played, backref='games')

    def __init__(self, nation1_id, nation2_id, date, events_id, score_nation1=None, score_nation2=None):
        self.nation1_id = nation1_id
        self.nation2_id = nation2_id
        self.date = date
        self.events_id = events_id
        self.score_nation1 = score_nation1
        self.score_nation2 = score_nation2

    def __repr__(self):
        return '<Game %s vs. %s>' % (self.nation1.name, self.nation2.name)
