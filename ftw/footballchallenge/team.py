from sqlalchemy import Column, Integer, String, Boolean
from ftw.footballchallenge import Base
from ftw.footballchallenge.game import Game
from ftw.footballchallenge.goal import Goal
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Table
from ftw.footballchallenge.teamstatistics import Teamstatistics


class Team(Base):
    __tablename__='teams'

    id_ = Column('id', Integer, primary_key=True)
    name = Column(String(45))
    user_id = Column('user_id', String(40), nullable=False)

    league_id = Column(Integer, ForeignKey('leagues.id'), nullable=True)
    league = relationship("League", backref=backref('leagues', order_by=id_))

    players = relationship('Teams_Players', backref='team')

    def __init__(self, name, user_id, league_id=None):
        self.name = name
        self.user_id = user_id
        self.league_id = league_id

    def __repr__(self):
        return '<Team %s>' % self.name

    def get_points(self, session):
        stats = session.query(Teamstatistics).filter(
            Teamstatistics.team_id==self.id_).order_by(
                Teamstatistics.game_id).first()
        return stats.total_points

    def get_points_for_game(self, game_id, session):
        stats = session.query(Teamstatistics).filter(
            Teamstatistics.team_id==self.id_ and
                Teamstatistics.game_id==game_id).one()
        return stats.points
