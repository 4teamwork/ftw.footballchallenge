from ftw.footballchallenge.testing import DATABASE_LAYER
from ftw.footballchallenge.nation import Nation
from ftw.footballchallenge.player import Player
import unittest2


class TestPlayerModel(unittest2.TestCase):
    
    layer = DATABASE_LAYER
    
    @property
    def session(self):
        return self.layer.session

    def test_add_without_nation(self):
        with self.assertRaises(TypeError):
            Player('Freddy', 'Midfield')
        

    def test_creation(self):
        
        nation1 = Nation('Nation1')
        self.session.add(nation1)
        self.layer.commit()
        nation1 = self.session.query(Nation).one()
        player1 = Player('Freddy', 'Midfield', nation1)
        self.session.add(nation1)
        self.layer.commit()
        players = self.session.query(Player).all()
        self.assertEquals(len(players), 1)
        myplayers = players[0]
        self.assertEqual(myplayers.Name, 'Freddy')
        self.assertEqual(myplayers.Position, 'Midfield')
        self.assertEqual(myplayers.Nations, nation1)
        
