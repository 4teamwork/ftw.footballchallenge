from ftw.footballchallenge.nation import Nation
from ftw.footballchallenge.game import Game
from ftw.footballchallenge.player import Player
from ftw.footballchallenge.goal import Goal
from ftw.footballchallenge.event import Event
from ftw.footballchallenge.testing import DATABASE_LAYER
from datetime import datetime
import unittest2
from datetime import date, timedelta
import transaction


class TestGoalsModel(unittest2.TestCase):
    
    layer = DATABASE_LAYER
    
    @property
    def session(self):
        return self.layer.session

    
    def test_creation(self):
        event1 = Event('TheEvent', date.today()+timedelta(days=1))
        self.session.add(event1)        
        # self.layer.commit()
        event1 = self.session.query(Event).one()
        nation1 = Nation('Nation1', event1.id_, 'SWE')
        self.session.add(nation1)
        nation2 = Nation('Nation2', event1.id_, 'GBR')
        self.session.add(nation2)
        
        nations = self.session.query(Nation).all()
        event = self.session.query(Event).one()
        game = Game(datetime.now(), event.id_,'group1', nation1_id=nations[0].id_, nation2_id=nations[1].id_)
        game.nation1_score = 3
        game.nation2_score = 0
        self.session.add(game)
        # self.layer.commit()

        event = self.session.query(Event).one()
        nation = self.session.query(Nation).first()
        player1 = Player('Freddy', 'Midfield', nation.id_, event.id_)
        self.session.add(player1)
        # self.layer.commit()
        
        player1 = self.session.query(Player).one()
        game = self.session.query(Game).one()
        game.players.append(player1)
        goal1 = Goal(player1.id_, game.id_, False)
        self.session.add(goal1)
        # self.layer.commit()
        player1 = self.session.query(Player).one()
        goals = self.session.query(Goal).all()
        self.assertEqual(len(goals),1)
        self.assertEqual(goals[0].id_, 1)
        self.assertEqual(goals[0].__repr__(),'<Goal Freddy, 1>')
        self.assertEqual(len(player1.get_goals(self.session)),1)
