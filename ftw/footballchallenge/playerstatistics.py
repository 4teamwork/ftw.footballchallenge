from sqlalchemy import Column, Integer
from ftw.footballchallenge import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
import transaction
from ftw.footballchallenge.config import POINT_MAPPING_STRIKER
from ftw.footballchallenge.config import POINT_MAPPING_MIDFIELD
from ftw.footballchallenge.config import POINT_MAPPING_DEFENDER
from ftw.footballchallenge.config import POINT_MAPPING_KEEPER
from z3c.saconfig import named_scoped_session


class Playerstatistics(Base):
    """Modeldefinition for playerstatistics"""
    __tablename__='playerstatistics'

    player_id = Column(Integer, ForeignKey('players.id'), primary_key=True,
                       nullable=False)
    game_id = Column(Integer, ForeignKey('games.id'), primary_key=True,
                     nullable=False)
    points = Column(Integer, nullable=False)
    total_points = Column(Integer, nullable=False)

    game = relationship("Game", backref=backref('playerstatistics',
                        order_by=game_id))
    player = relationship("Player", backref=backref('playerstatistics',
                          order_by=player_id))

    def __init__(self, player_id, game_id, points, total_points):
        self.player_id = player_id
        self.game_id = game_id
        self.points = points
        self.total_points = total_points

    def __repr__(self):
        return '<Statistics for Player %s. Total Points: %s>' % (
            self.player.name, self.total_points)


def calculate_player_points(game):
    """This function calculates the playerpoints
       and rewrites it to a playerstatistics instance

    """
    for player in game.players:
        points = 0
        #get right mapping
        if player.position == "striker":
            mapping = POINT_MAPPING_STRIKER
        elif player.position == "midfield":
            mapping = POINT_MAPPING_MIDFIELD
        elif player.position == "defender":
            mapping = POINT_MAPPING_DEFENDER
        else:
            mapping = POINT_MAPPING_KEEPER

        #calculate points for game result
        if player.nation_id == game.nation1_id:
            if game.score_nation1 > game.score_nation2:
                points += mapping['victory']
            elif game.score_nation1 == game.score_nation2:
                points += mapping['draw']
            else:
                points += mapping['loss']
        else:
            if game.score_nation1 < game.score_nation2:
                points += mapping['victory']
            elif game.score_nation1 == game.score_nation2:
                points += mapping['draw']
            else:
                points += mapping['loss']

        session = named_scoped_session('footballchallenge')
        #get points for playerspecific events like cards or goals
        goals = player.get_goals(session, game.id_)
        points += mapping['goal']*len(goals)
        card = player.get_cards(session, game.id_)
        if card:
            points += mapping[card[0].color]
        if player.position == "keeper" or player.position == "defender":
            if player.nation_id == game.nation1_id:
                if game.score_nation2 == 0:
                    points += mapping['no_goals']
                elif game.score_nation2 <= 3:
                    points += mapping['3_goals']
            else:
                if game.score_nation1 == 0:
                    points += mapping['no_goals']
                elif game.score_nation1 <= 3:
                    points += mapping['3_goals']
        if player.position == "keeper":
            saves = player.get_saves(session, game.id_)
            points += mapping['save']*len(saves)

        #get last entry. We need it to calculate the total
        old_entry = session.query(Playerstatistics).filter(
            Playerstatistics.player_id == player.id_).all()
        if not old_entry:
            stats = Playerstatistics(player.id_, game.id_, points, points)
        else:
            stats = Playerstatistics(player.id_, game.id_, points,
                                     old_entry[-1].total_points+points)
        session.add(stats)
    transaction.commit()
