from ftw.footballchallenge.testing import DATABASE_LAYER
from ftw.footballchallenge.nation import Nation
import unittest2


class TestNationModel(unittest2.TestCase):
    
    layer = DATABASE_LAYER
    
    @property
    def session(self):
        return self.layer.session


    def test_creation(self):
        nation = Nation('MyNation')
        self.session.add(nation)
        self.layer.commit()

        nations = self.session.query(Nation).all()
        self.assertEquals(len(nations), 1)
        mynation = nations[0]
        self.assertEqual(mynation.name, 'MyNation')
