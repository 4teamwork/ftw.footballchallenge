from ftw.footballchallenge.testing import DATABASE_LAYER
from ftw.footballchallenge.nation import Nation
from ftw.footballchallenge.game import Game
from ftw.footballchallenge.player import Player
from ftw.footballchallenge.event import Event
import unittest2
from datetime import datetime
from datetime import date


class TestGameModel(unittest2.TestCase):
    
    layer = DATABASE_LAYER
    
    @property
    def session(self):
        return self.layer.session

    
    def test_creation(self):
        event1 = Event('TheEvent', date.today()+1)
        self.session.add(event1)        
        nation1 = Nation('Nation1')
        self.session.add(nation1)
        nation2 = Nation('Nation2')
        self.session.add(nation2)
        self.layer.commit()
        nations = self.session.query(Nation).all()
        event = self.session.query(Event).one()
        game = Game(nations[0].id_, nations[1].id_, datetime.now(), event.id_, 3, 0)
        self.session.add(game)
        self.layer.commit()
        
        games = self.session.query(Game).all()
        self.assertEqual(len(games), 1)
        self.assertEqual(games[0].__repr__(), '<Game Nation1 vs. Nation2>')
        
    def test_mtom_nations(self):
        event1 = Event('TheEvent')
        self.session.add(event1)        
        nation1 = Nation('Nation1')
        self.session.add(nation1)
        nation2 = Nation('Nation2')
        self.session.add(nation2)
        self.layer.commit()
        nations = self.session.query(Nation).all()
        event = self.session.query(Event).one()
        game = Game(nations[0].id_, nations[1].id_, datetime.now(), event.id_, 3, 0)
        self.session.add(game)
        self.layer.commit()

        games = self.session.query(Game).all()
        nations = self.session.query(Nation).all()
        self.assertEqual(games[0].nation1, nations[0])
        self.assertEqual(games[0].nation2, nations[1])

    def test_mtom_players(self):
        event1 = Event('TheEvent')
        self.session.add(event1)        
        nation1 = Nation('Nation1')
        self.session.add(nation1)
        nation2 = Nation('Nation2')
        self.session.add(nation2)
        self.layer.commit()
        nations = self.session.query(Nation).all()
        event = self.session.query(Event).one()
        game = Game(nations[0].id_, nations[1].id_, datetime.now(), event.id_, 3, 0)
        self.session.add(game)
        self.layer.commit()

        game = self.session.query(Game).one()
        nations = self.session.query(Nation).all()
        player1 = Player('Freddy', 'midfield', nations[0].id_)
        player2 = Player('Hans', 'defence', nations[0].id_)
        game.players.append(player1)
        game.players.append(player2)
        self.layer.commit()
        game = self.session.query(Game).one()
        players = self.session.query(Player).all()
        self.assertEqual(len(game.players), 2)
        self.assertEqual(players[0].games[0], game)