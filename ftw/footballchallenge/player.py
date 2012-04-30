from sqlalchemy import Column, Integer, String, Date, Numeric, BLOB
from ftw.footballchallenge import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from ftw.footballchallenge.playerstatistics import Playerstatistics
from ftw.footballchallenge.goal import Goal
from ftw.footballchallenge.card import Card
from ftw.footballchallenge.save import Save
from ftw.footballchallenge.game import Game
from ftw.footballchallenge.event import Event
from ftw.footballchallenge.config import POINT_MAPPING_STRIKER
from ftw.footballchallenge.config import POINT_MAPPING_MIDFIELD
from ftw.footballchallenge.config import POINT_MAPPING_DEFENDER
from ftw.footballchallenge.config import POINT_MAPPING_KEEPER
from datetime import date
from zope.schema.interfaces import IVocabularyFactory
from zope.schema import vocabulary
from z3c.saconfig import named_scoped_session
from zope.interface import alsoProvides
from zope.interface import implements
from ftw.footballchallenge.interfaces import IPlayer
from zope.interface import classProvides
from zope.schema.interfaces import ISource, IContextSourceBinder

class Player(Base):
    """Modeldefinition for Player"""
    __tablename__='players'

    implements(IPlayer)

    id_ = Column('id', Integer, primary_key=True)
    name = Column(String(128))
    position = Column(String(45))
    original_name = Column(String(128))
    date_of_birth = Column(Date)
    age = Column(Integer)
    foot = Column(String(10))
    value = Column(Integer)
    size = Column(Numeric(3,2))
    club = Column(String(45))
    league = Column(String(64))
    image = Column(BLOB)
    nation_id = Column(Integer, ForeignKey('nations.id'), nullable=False)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)

    nation = relationship("Nation", backref=backref('players', order_by=id_))
    event = relationship("Event", backref=backref('players', order_by=id_))

    def __init__(self, name, position, nation_id, event_id,
                 original_name=None, date_of_birth=None, age=None,
                 foot=None, value=None, size=None, club=None, image=None):
        self.name = name
        self.position = position
        self.event_id = event_id
        self.original_name = original_name
        self.date_of_birth = date_of_birth
        self.age = age
        self.foot = foot
        self.value = value
        self.size = size
        self.club = club
        self.image = image
        self.nation_id = nation_id

    def __repr__(self):
        return '<Player %s>' % self.name

    def pretty_value(self):
        """The value with thousands separators.
        """
        value = '%d' % self.value
        groups = []
        while value and value[-1].isdigit():
            groups.append(value[-3:])
            value = value[:-3]
        return value + "'".join(reversed(groups))

    def get_points(self, session):
        """Gets the Current Total Points for this Player"""
        stats = session.query(Playerstatistics).filter(
            Playerstatistics.player_id==self.id_).order_by(
                Playerstatistics.game_id).first()
        return stats.total_points

    def get_points_for_game(self, game_id, session):
        """Gets the Points gained in one game"""
        stats = session.query(Playerstatistics).filter(
            Playerstatistics.player_id==self.id_ and \
                Playerstatistics.game_id==game_id).one()
        return stats.points

    def get_goals(self, session, game_id=None):
        """Gets all goals or the goals for one game"""
        if game_id:
            goals = session.query(Goal).filter_by(
                player_id=self.id_).filter_by(game_id=game_id).order_by(
                    Goal.game_id).all()
        else:
            goals = session.query(Goal).filter(
                Goal.player_id==self.id_).order_by(Goal.game_id).all()
        return goals

    def get_cards(self, session, game_id=None):
        """Gets all Card or the Cards for one game"""
        if game_id:
            cards = session.query(Card).filter_by(
                player_id=self.id_).filter_by(game_id=game_id).order_by(
                    Card.game_id).all()
        else:
            cards = session.query(Card).filter(
                Card.player_id==self.id_).order_by(
                    Card.game_id).all()
        return cards

    def get_saves(self, session, game_id=None):
        """Gets all Saves or the Saves for one game"""
        if game_id:
            saves = session.query(Save).filter_by(
                player_id=self.id_).filter_by(game_id=game_id).order_by(
                    Save.game_id).all()
        else:
            saves = session.query(Save).filter(
                Save.player_id==self.id_).order_by(
                    Save.game_id).all()
        return saves

    def get_log(self):
        """Returns a Log with all Events that
           influenced the Points of a Player

        """
        #TODO: Check if we can refactor this. The code looks bloody awful
        session = named_scoped_session('footballchallenge')
        log = []
        #get right mapping
        if self.position == "striker":
            mapping = POINT_MAPPING_STRIKER
        elif self.position == "midfield":
            mapping = POINT_MAPPING_MIDFIELD
        elif self.position == "defender":
            mapping = POINT_MAPPING_DEFENDER
        else:
            mapping = POINT_MAPPING_KEEPER
        #get all games where this player played
        games = session.query(Game).filter(Game.players.any(
            id_=self.id_)).order_by(Game.date).all()
        for game in games:
            if game.nation1 == self.nation:
                enemy = game.nation2
            else:
                enemy = game.nation1

            #get his cards for this game
            cards = self.get_cards(session, game.id_)
            if cards:
                log.append([cards[0], mapping[cards[0].color.lower()],
                           cards[0].color.encode('utf-8')+ ' Card'])
            goals = self.get_goals(session, game.id_)
            #get his goals
            if goals:
                for goal in goals:
                    log.append([goal, mapping['goal'],
                               'Goal vs %s' % enemy.name])
            saves = self.get_saves(session, game.id_)
            #the player only can have saves if hes keeper
            if saves:
                for save in saves:
                    log.append([save, mapping['save'],
                               'Save vs %s' % enemy.name])

            #distribute points for victory, draw and loss
            if game.nation1 == self.nation:
                if game.score_nation1 > game.score_nation2:
                    log.append([game, mapping['victory'],
                               'Victory %s vs. %s' % (game.nation1.name,
                                                      game.nation2.name)])
                elif game.score_nation1 == game.score_nation2:
                    log.append([game, mapping['draw'],
                               'Draw %s vs. %s' % (game.nation1.name,
                                                   game.nation2.name)])
                elif game.score_nation1 < game.score_nation2:
                    log.append([game, mapping['loss'],
                               'Loss %s vs. %s' % (game.nation1.name,
                                                   game.nation2.name)])
                if self.position == "defender" or self.position == "keeper":
                    if game.score_nation2 == 0:
                        log.append([game, mapping['no_goals'],
                                   'No Goals recieved'])
                    elif game.score_nation2 >=3:
                        log.append([game, mapping['3_goals'],
                                   '3 Goals recieved'])
            else:
                if game.score_nation1 > game.score_nation2:
                    log.append([game, mapping['loss'],
                               'Loss %s vs. %s' % (game.nation1.name,
                                                   game.nation2.name)])
                elif game.score_nation1 == game.score_nation2:
                    log.append([game, mapping['draw'],
                               'Draw %s vs. %s' % (game.nation1.name,
                                                   game.nation2.name)])
                elif game.score_nation1 < game.score_nation2:
                    log.append([game, mapping['victory'],
                               'Victory %s vs. %s' % (game.nation1.name,
                                                      game.nation2.name)])
                if self.position == "defender" or self.position == "keeper":
                    if game.score_nation1 == 0:
                        log.append([game, mapping['no_goals'],
                                   'No Goals recieved'])
                    elif game.score_nation2 >=3:
                        log.append([game, mapping['3_goals'],
                                   '3 Goals recieved'])
        return log


def get_player_term(context, position=None, nation=None):
    """Returns the players as SimpleVocabulary"""
    terms=[]
    session = named_scoped_session('footballchallenge')
    event_id = session.query(Event).filter(
        Event.LockDate > date.today()).one().id_
    if not position and not nation:
        players = session.query(Player).filter(
            Player.event_id == event_id).order_by(Player.name).all()
    elif position and not nation:
        players = session.query(Player).filter(
            Player.position==position and \
                Player.event_id == event_id).order_by(Player.name).all()
    for player in players:
        terms.append(vocabulary.SimpleTerm(player.id_, player.id_,
                                           player.name+' [%s]' % player.nation.country))
    return vocabulary.SimpleVocabulary(terms)


class PlayerVocabularyFactory(object):
    
    implements(IVocabularyFactory)

    def __call__(self, context):
        """a Proxy function which returns keeper term"""
        return get_player_term(context)
    
    
class KeeperVocabularyFactory(object):

    implements(IVocabularyFactory)
#    implements(ISource)
#    classProvides(IContextSourceBinder)

    def __call__(self, context):
        """a Proxy function which returns keeper term"""
        return get_player_term(context, position="keeper")

class DefenderVocabularyFactory(object):

        implements(IVocabularyFactory)
    #    implements(ISource)
    #    classProvides(IContextSourceBinder)

        def __call__(self, context):
            """a Proxy function which returns keeper term"""
            return get_player_term(context, position="defender")

class MidfieldVocabularyFactory(object):

        implements(IVocabularyFactory)
    #    implements(ISource)
    #    classProvides(IContextSourceBinder)

        def __call__(self, context):
            """a Proxy function which returns keeper term"""
            return get_player_term(context, position="midfield")



class StrikerVocabularyFactory(object):

        implements(IVocabularyFactory)
    #    implements(ISource)
    #    classProvides(IContextSourceBinder)

        def __call__(self, context):
            """a Proxy function which returns keeper term"""
            return get_player_term(context, position="striker")

