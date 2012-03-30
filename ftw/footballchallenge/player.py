from sqlalchemy import Column, Integer, String, Date, Numeric, BLOB
from ftw.footballchallenge import Base
from sqlalchemy import ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from ftw.footballchallenge.playerstatistics import Playerstatistics
from ftw.footballchallenge.goal import Goal
from ftw.footballchallenge.card import Card
from ftw.footballchallenge.save import Save
from ftw.footballchallenge.game import Game
from ftw.footballchallenge.event import Event
from ftw.footballchallenge.config import POINT_MAPPING_STRIKER, POINT_MAPPING_MIDFIELD, POINT_MAPPING_DEFENDER, POINT_MAPPING_KEEPER
from datetime import date
from zope.schema import vocabulary
from z3c.saconfig import named_scoped_session
from zope.interface import alsoProvides
from zope.schema.interfaces import IContextSourceBinder


class Player(Base):
    __tablename__='players'


    id_ = Column('id', Integer, primary_key=True)
    name = Column(String(128))
    position = Column(String(45))
    original_name = Column(String(128))
    date_of_birth = Column(Date)
    age = Column(Integer)
    foot = Column(String(10))
    value = Column(Integer)
    size = Column(Numeric(2,2))
    club = Column(String(45))
    image = Column(BLOB)
    nation_id = Column(Integer, ForeignKey('nations.id'), nullable=False)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)

    nation = relationship("Nation", backref=backref('players', order_by=id_))
    event = relationship("Event", backref=backref('players', order_by=id_))
    
    def __init__(self, name, position, nation_id, event_id, original_name=None, date_of_birth=None, age=None, foot=None, value=None, size=None, club=None, image=None):
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
            goals = session.query(Goal).filter(Goal.player_id==self.id_ and Goal.game_id==game_id).order_by(Goal.game_id).all()
        else:
            goals = session.query(Goal).filter(Goal.player_id==self.id_).order_by(Goal.game_id).all()
        return goals
    
    def get_cards(self, session, game_id=None):
        """Gets all Card or the Cards for one game"""
        if game_id:
            cards = session.query(Card).filter(Card.player_id==self.id_ and Card.game_id==game_id).order_by(Card.game_id).all()        
        else:
            cards = session.query(Card).filter(Card.player_id==self.id_).order_by(Card.game_id).all()
        return cards
    
    def get_saves(self, session, game_id=None):
        """Gets all Saves or the Saves for one game"""
        if game_id:
            saves = session.query(Save).filter(Save.player_id==self.id_ and Save.game_id==game_id).order_by(Save.game_id).all()        
        else:
            saves = session.query(Save).filter(Save.player_id==self.id_).order_by(Save.game_id).all()
        return saves

    def get_log(self, session):
        """Returns a Log with all Events that influenced the Points of a Player"""

        #TODO: Refactor this Function. I don't like the dublicated code in it
        log = []
        if self.position == "striker":
            mapping = POINT_MAPPING_STRIKER
        elif self.position == "midfield":
            mapping = POINT_MAPPING_MIDFIELD
        elif self.position == "defender":
            mapping = POINT_MAPPING_DEFENDER
        else:
            mapping = POINT_MAPPING_KEEPER
        games = session.query(Game).filter(Game.players.any(id_=self.id_)).order_by(Game.id_).all()
        for game in games:
            if game.nation1 == self.nation:
                enemy = game.nation2
            else:
                enemy = game.nation1
            cards = session.query(Card).filter(Card.game_id==game.id_ and Card.player==self).all()
            if cards:
                log.append([cards[0], mapping[cards[0].color.encode('utf-8').lower()], cards[0].color.encode('utf-8')+ ' Card'])
            goals = session.query(Goal).filter(Goal.game_id==game.id_ and Goal.player==self).all()
            if goals:
                for goal in goals:
                    log.append([goal, mapping['goal'],'Goal vs %s' % enemy.name])
            saves = session.query(Save).filter(Save.game_id==game.id_ and Save.player==self).all()
            if saves:
                for save in saves:
                    log.append([save, mapping['save'], 'Save vs %s' % enemy.name])
            if game.nation1 == self.nation:
                if game.score_nation1 > game.score_nation2:
                    log.append([game, mapping['victory'], 'Victory %s vs. %s' % (game.nation1.name, game.nation2.name)])
                elif game.score_nation1 == game.score_nation2:
                    log.append([game, mapping['draw'], 'Draw %s vs. %s' % (game.nation1.name, game.nation2.name)])
                elif game.score_nation1 < game.score_nation2:
                    log.append([game, mapping['loss'], 'Loss %s vs. %s' % (game.nation1.name, game.nation2.name)])
                if self.position == "defender" or self.position == "keeper":
                    if game.score_nation2 == 0:
                        log.append([game, mapping['no_goals'], 'No Goals recieved'])
                    elif game.score_nation2 >3:
                        log.append([game, mapping['3_goals'], '3 Goals recieved'])
            else:
               if game.score_nation1 > game.score_nation2:
                   log.append([game, mapping['loss'], 'Loss %s vs. %s' % (game.nation1.name, game.nation2.name)])
               elif game.score_nation1 == game.score_nation2:
                   log.append([game, mapping['draw'], 'Draw %s vs. %s' % (game.nation1.name, game.nation2.name)])
               elif game.score_nation1 < game.score_nation2:
                   log.append([game, mapping['victory'], 'Victory %s vs. %s' % (game.nation1.name, game.nation2.name)])
               if self.position == "defender" or self.position == "keeper":
                   if game.score_nation1 == 0:
                       log.append([game, mapping['no_goals'], 'No Goals recieved'])
                   elif game.score_nation2 >1:
                       log.append([game, mapping['3_goals'], '3 Goals recieved'])
        return log

def get_player_term(context, position=None, nation=None):
    
    terms=[]
    session = named_scoped_session('footballchallenge')
    event_id = session.query(Event).filter(Event.LockDate > date.today()).one().id_
    if not position and not nation:
        players = session.query(Player).filter(Player.event_id == event_id).all()
    elif position and not nation:
        players = session.query(Player).filter(Player.position==position and Player.event_id == event_id).all()        
    for player in players:
        terms.append(vocabulary.SimpleTerm(player.id_, player.id_, player.name))
    return vocabulary.SimpleVocabulary(terms)
    
def get_keeper_term(context):
    return get_player_term(context, position="keeper")

def get_defender_term(context):
    return get_player_term(context, position="defender")

def get_midfield_term(context):
    return get_player_term(context, position="midfield")

def get_striker_term(context):
    return get_player_term(context, position="striker")

alsoProvides(get_keeper_term, IContextSourceBinder)
alsoProvides(get_defender_term, IContextSourceBinder)
alsoProvides(get_midfield_term, IContextSourceBinder)
alsoProvides(get_striker_term, IContextSourceBinder)
alsoProvides(get_player_term, IContextSourceBinder)
