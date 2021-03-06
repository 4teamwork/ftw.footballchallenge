from ftw.footballchallenge.nation import Nation
from ftw.footballchallenge.game import Game
from ftw.footballchallenge.event import Event
from ftw.footballchallenge.player import Player
from ftw.footballchallenge.playerstatistics import Playerstatistics
from datetime import datetime
from ftw.footballchallenge.testing import DATABASE_LAYER
import unittest2
from datetime import date, timedelta

class TestPlayerstatsModel(unittest2.TestCase):
    
    layer = DATABASE_LAYER
    
    @property
    def session(self):
        return self.layer.session

    def test_creation(self):
        event1 = Event('TheEvent', date.today()+timedelta(days=1))
        self.session.add(event1)
        event1 = self.session.query(Event).one()
        nation1 = Nation('Nation1', event1.id_, 'SWE')
        self.session.add(nation1)
        nation2 = Nation('Nation2', event1.id_, 'GBR')
        self.session.add(nation2)
        # self.layer.commit()
        nations = self.session.query(Nation).all()
        event = self.session.query(Event).one()
        game = Game(datetime.now(), event.id_,'group1', nation1_id=nations[0].id_, nation2_id=nations[1].id_)
        game.nation1_score = 3
        game.nation2_score = 0
        self.session.add(game)
        player1 = Player('Freddy', 'Midfield', nations[0].id_, event1.id_)
        self.session.add(player1)
        # self.layer.commit()


        player = self.session.query(Player).one()
        game = self.session.query(Game).one()
        stats1 = Playerstatistics(player.id_, game.id_, 5)
        self.session.add(stats1)
        # self.layer.commit()
        myplayer = self.session.query(Player).one()
        game = self.session.query(Game).one()
        stats = self.session.query(Playerstatistics).one()
        self.assertEqual(stats.__repr__(), '<Statistics for Player Freddy. Points: 5>')
        points = myplayer.get_points_for_game(game.id_, self.session)
        self.assertEqual(points, 5)