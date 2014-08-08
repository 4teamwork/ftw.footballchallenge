from sqlalchemy import Column, Integer, DateTime, Boolean, String
from ftw.footballchallenge import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Table
from zope.interface import implements
from ftw.footballchallenge.interfaces import IGame
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from ftw.footballchallenge import _


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
        return '<Game %s-%s>' % (self.nation1.country, self.nation2.country)

    def has_penalty(self):
        penaltys = []
        for goal in self.goals:
            if goal.is_penalty:
                penaltys.append(goal)
        return bool(penaltys)

    def get_penalty(self):
        total_nation1_score = self.score_nation1
        total_nation2_score = self.score_nation2
        for goal in self.goals:
            if goal.is_penalty:
                if goal.player.nation_id == self.nation1_id:
                    total_nation1_score += 1
                else:
                    total_nation2_score += 1
        return '('+str(total_nation1_score)+':'+str(total_nation2_score)+' n.P.)'


RoundVocabulary = SimpleVocabulary(
    [SimpleTerm(value=u'group1', title=_(u'label_group1', default=u'Group1')),
     SimpleTerm(value=u'group2', title=_(u'label_group2', default=u'Group2')),
     SimpleTerm(value=u'group3', title=_(u'label_group3', default=u'Group3')),
     SimpleTerm(value=u'roundof16', title=_(u'label_roundof16', default=u'Round of Sixteen')),
     SimpleTerm(value=u'quarterfinals', title=_(u'label_quarterfinals', default=u'Quarterfinals')),
     SimpleTerm(value=u'semifinals', title=_(u'label_semifinals', default=u'Semifinals')),
     SimpleTerm(value=u'finals', title=_(u'label_finals', default=u'Finals'))])