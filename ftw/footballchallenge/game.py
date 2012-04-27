from sqlalchemy import Column, Integer, DateTime, Boolean, String
from ftw.footballchallenge import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Table
from zope.interface import implements
from ftw.footballchallenge.interfaces import IGame


players_played = Table('players_played', Base.metadata,
    Column('game_id', Integer, ForeignKey('games.id')),
    Column('player_id', Integer, ForeignKey('players.id')))


class Game(Base):
    """Model delclaration for Game Type"""
    __tablename__='games'

    implements(IGame)

    id_ = Column('id', Integer, primary_key=True)

    nation1_id = Column(Integer, ForeignKey('nations.id'))
    nation2_id = Column(Integer, ForeignKey('nations.id'))
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

    round_ = Column('round', String(20), nullable=False)
    calculated = Column(Boolean)
    nation1_dummy = Column(String(45))
    nation2_dummy = Column(String(45))
    players = relationship('Player', secondary=players_played, backref='games')

    def __init__(self, date, events_id, round_,
                 nation1_dummy=None, nation2_dummy=None, nation1_id=None, nation2_id=None, calculated=False):
        self.nation1_id = nation1_id
        self.nation2_id = nation2_id
        self.date = date
        self.events_id = events_id
        self.nation1_dummy = nation1_dummy
        self.nation2_dummy = nation2_dummy
        self.round_ = round_
        self.calculated = calculated
    def __repr__(self):
        return '<Game %s vs. %s>' % (self.nation1.name, self.nation2.name)
