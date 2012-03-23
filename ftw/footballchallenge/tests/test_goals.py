from ftw.footballchallenge.nation import Nation
from ftw.footballchallenge.game import Game
from ftw.footballchallenge.player import Player
from ftw.footballchallenge.goal import Goal
from ftw.footballchallenge.event import Event
from ftw.footballchallenge.testing import DATABASE_LAYER
from datetime import datetime
import unittest2

class TestGoalsModel(unittest2.TestCase):
    
    layer = DATABASE_LAYER
    
    @property
    def session(self):
        return self.layer.session

    
    def test_creation(self):
        event = Event('TheEvent')
        self.session.add(event)
        nation1 = Nation('Nation1')
        self.session.add(nation1)
        nation2 = Nation('Nation2')
        self.session.add(nation2)
        self.layer.commit()
        
        nations = self.session.query(Nation).all()
        event = self.session.query(Event).one()
        game = Game(nations[0].id_, nations[1].id_, datetime.now(), event.id_, '3:0')
        self.session.add(game)
        self.layer.commit()

        nation = self.session.query(Nation).first()
        player1 = Player('Freddy', 'Midfield', nation.id_)
        self.session.add(player1)
        self.layer.commit()
        
        player1 = self.session.query(Player).one()
        game = self.session.query(Game).one()
        goal1 = Goal(player1.id_, game.id_, False)
        self.session.add(goal1)
        self.layer.commit()
        goals = self.session.query(Goal).all()
        self.assertEqual(len(goals),1)
        self.assertEqual(goals[0].id_, 1)
        self.assertEqual(goals[0].__repr__(),'<Goal Freddy, 1>')