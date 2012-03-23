from ftw.footballchallenge.nation import Nation
from ftw.footballchallenge.game import Game
from ftw.footballchallenge.player import Player
from ftw.footballchallenge.card import Card
from ftw.footballchallenge.event import Event
from ftw.footballchallenge.testing import DATABASE_LAYER
import unittest2
from datetime import datetime


class TestGoalsModel(unittest2.TestCase):
    
    layer = DATABASE_LAYER
    
    @property
    def session(self):
        return self.layer.session

    
    def test_creation(self):
        event1 = Event('TheEvent')
        self.session.add(event1)
        nation1 = Nation('Nation1')
        self.session.add(nation1)
        nation2 = Nation('Nation2')
        self.session.add(nation2)
        nations = self.session.query(Nation).all()
        event = self.session.query(Event).one()
        game = Game(nations[0].id_, nations[1].id_, datetime.now(), event.id_, '3:0')
        self.session.add(game)
        self.layer.commit()
        nations = self.session.query(Nation).all()
        player1 = Player('Freddy', 'Midfield', nations[0].id_)
        self.session.add(player1)
        self.layer.commit()
        
        game = self.session.query(Game).one()
        player1 = self.session.query(Player).one()
        card1 = Card(player1.id_, game.id_, 'Red')
        self.session.add(card1)
        self.layer.commit()
        cards = self.session.query(Card).all()
        self.assertEqual(len(cards),1)
        self.assertEqual(cards[0].id_, 1)
        self.assertEqual(cards[0].__repr__(),'<Card Freddy, 1, Red>')