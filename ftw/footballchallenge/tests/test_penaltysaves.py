from ftw.footballchallenge.nation import Nation
from ftw.footballchallenge.game import Game
from ftw.footballchallenge.player import Player
from ftw.footballchallenge.save import Save
from ftw.footballchallenge.event import Event
from ftw.footballchallenge.testing import DATABASE_LAYER
from datetime import datetime
from datetime import date, timedelta
import unittest2

class TestGoalsModel(unittest2.TestCase):
    
    layer = DATABASE_LAYER
    
    @property
    def session(self):
        return self.layer.session

    
    def test_creation(self):
        event1 = Event('TheEvent', date.today()+timedelta(days=1))
        # self.layer.commit()
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
        # self.layer.commit()

        nation = self.session.query(Nation).first()
        player1 = Player('Freddy', 'Goalkeeper', nation.id_, event.id_)
        self.session.add(player1)
        # self.layer.commit()
        
        player1 = self.session.query(Player).one()
        game = self.session.query(Game).one()
        save1 = Save(player1.id_, game.id_)
        self.session.add(save1)
        # self.layer.commit()
        saves = self.session.query(Save).all()
        self.assertEqual(len(saves),1)
        self.assertEqual(saves[0].__repr__(), '<Save <Player Freddy>, 1>')