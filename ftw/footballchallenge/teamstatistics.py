from sqlalchemy import Column, Integer
from ftw.footballchallenge import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from ftw.footballchallenge.team import Team
from ftw.footballchallenge.playerstatistics import Playerstatistics
from ftw.footballchallenge.Teams_Players import Teams_Players
import transaction
from z3c.saconfig import named_scoped_session


class Teamstatistics(Base):
    """Modeldefinition for Teamstatistics"""
    __tablename__='teamstatistics'

    team_id = Column(Integer, ForeignKey('teams.id'), primary_key=True,
                       nullable=False)
    game_id = Column(Integer, ForeignKey('games.id'), primary_key=True,
                     nullable=False)
    points = Column(Integer, nullable=False)
    total_points = Column(Integer, nullable=False)

    game = relationship("Game", backref=backref('teamstatistics',
                        order_by=game_id))
    team = relationship("Team", backref=backref('teamstatistics',
                          order_by=team_id))

    def __init__(self, team_id, game_id, points, total_points):
        self.team_id = team_id
        self.game_id = game_id
        self.points = points
        self.total_points = total_points

    def __repr__(self):
        return '<Statistics for Team %s. Total Points: %s>' % (self.team.name,
            self.total_points)


def calculate_team_points(game):
    """recalculates the team points after a game"""
    session = named_scoped_session('footballchallenge')
    teams = session.query(Team).filter(Team.event_id == game.event_id).all()
    points = {}
    for team in teams:
        for player in game.players:
            if player.teams.team == team:
                playerstats = session.query(Playerstatistics).filter(
                    Playerstatistics.player_id == player.id_ and \
                        Playerstatistics.game_id == game.id_)
                team_player = session.query(Teams_Players).filter(
                    Teams_Players.team_id == team.id_ and \
                    Teams_Players.player_id == player.id_)
                if not team_player.is_starter:
                    points[team.id_]+= playerstats.points/2
                else:
                    points[team.id_]+= playerstats.points/2

    for key, value in points.items():
        old_stats = session.query(Teamstatistics.team_id==key).all()[-1]
        if not old_stats:
            stats=Teamstatistics(key, game.id_, value, value)
        else:
            stats=Teamstatistics(key, game.id_, value,
                                 old_stats.total_points+value)

        session.add(stats)
    transaction.commit()
