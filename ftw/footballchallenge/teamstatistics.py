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

    game = relationship("Game", backref=backref('teamstatistics',
                        order_by=game_id))
    team = relationship("Team", backref=backref('teamstatistics',
                          order_by=team_id))

    def __init__(self, team_id, game_id, points):
        self.team_id = team_id
        self.game_id = game_id
        self.points = points

    def __repr__(self):
        return '<Statistics for Team %s. Points: %s>' % (self.team.name,
            self.points)


def calculate_team_points(game):
    """recalculates the team points after a game"""
    session = named_scoped_session('footballchallenge')
    teams = session.query(Team).filter_by(event_id = game.events_id).filter_by(valid = True).all()
    session.query(Teamstatistics).filter(Teamstatistics.game_id == game.id_).delete()
    points = {}
    for team in teams:
        for player in game.players:
            for teams_players in player.teams:
                if teams_players.team == team:
                    playerstats = session.query(Playerstatistics).filter_by(
                        player_id = player.id_).filter_by(game_id = game.id_).one()
                    team_player = session.query(Teams_Players).filter_by(
                        team_id = team.id_).filter_by(
                        player_id = player.id_).one()
                    if not points.get(team.id_, None):
                        points[team.id_] = 0
                    if not team_player.is_starter:
                        points[team.id_]+= playerstats.points/2
                    else:
                        points[team.id_]+= playerstats.points
        if not points.get(team.id_):
            stats=Teamstatistics(team.id_, game.id_, 0)
            session.add(stats)
            
    for key, value in points.items():
        old_entry = session.query(Teamstatistics).filter_by(team_id=key).filter_by(game_id=game.id_).all()
        if len(old_entry):
            old_entry[0].points = value
        else:
            stats=Teamstatistics(key, game.id_, value)
            session.add(stats)
    game.calculated = True