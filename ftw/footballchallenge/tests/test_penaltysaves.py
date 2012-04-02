from ftw.footballchallenge.nation import Nation
from ftw.footballchallenge.game import Game
from ftw.footballchallenge.player import Player
from ftw.footballchallenge.save import Save
from ftw.footballchallenge.event import Event
from ftw.footballchallenge.testing import DATABASE_LAYER
from datetime import datetime
from datetime import date
import unittest2

class TestGoalsModel(unittest2.TestCase):
    
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

        nation = self.session.query(Nation).first()
        player1 = Player('Freddy', 'Goalkeeper', nation.id_)
        self.session.add(player1)
        self.layer.commit()
        
        player1 = self.session.query(Player).one()
        game = self.session.query(Game).one()
        save1 = Save(player1.id_, game.id_)
        self.session.add(save1)
        self.layer.commit()
        saves = self.session.query(Save).all()
        self.assertEqual(len(saves),1)
        self.assertEqual(saves[0].__repr__(), '<Save <Player Freddy>, 1>')