from ftw.footballchallenge.testing import DATABASE_LAYER
from ftw.footballchallenge.nation import Nation
from ftw.footballchallenge.player import Player
from ftw.footballchallenge.event import Event
import unittest2
from datetime import date, timedelta


class TestPlayerModel(unittest2.TestCase):
    
    layer = DATABASE_LAYER
    
    @property
    def session(self):
        return self.layer.session

    def test_add_without_nation(self):
        with self.assertRaises(TypeError):
            Player('Freddy', 'Midfield')
        

    def test_creation(self):
        event1 = Event('TheEvent', date.today()+ timedelta(days=1))
        self.session.add(event1)
        event1 = self.session.query(Event).one()
        nation1 = Nation('Nation1', event1.id_, 'SWE')
        self.session.add(nation1)
        # self.layer.commit()
        mynation = self.session.query(Nation).one()
        player1 = Player('Freddy', 'Midfield', mynation.id_, event1.id_)
        self.session.add(player1)
        # self.layer.commit()
        #I need to get it again, since the session is closed by commit()
        mynation = self.session.query(Nation).one()
        players = self.session.query(Player).all()
        self.assertEquals(len(players), 1)
        myplayers = players[0]
        self.assertEqual(myplayers.name, 'Freddy')
        self.assertEqual(myplayers.position, 'Midfield')
        self.assertEqual(myplayers.nation.name, mynation.name)
        
