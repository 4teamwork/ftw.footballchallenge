from ftw.footballchallenge.testing import DATABASE_LAYER
from ftw.footballchallenge.nation import Nation
from ftw.footballchallenge.event import Event
import unittest2
from datetime import date, timedelta
import transaction

class TestNationModel(unittest2.TestCase):
    
    layer = DATABASE_LAYER
    
    @property
    def session(self):
        return self.layer.session


    def test_creation(self):
        event1 = Event('TheEvent', date.today() + timedelta(days=1))
        self.session.add(event1)
        # self.layer.commit()
        event = self.session.query(Event).one()
        nation = Nation('MyNation', event.id_, 'SWE')
        self.session.add(nation)
        # self.layer.commit()

        nations = self.session.query(Nation).all()
        self.assertEquals(len(nations), 1)
        mynation = nations[0]
        self.assertEqual(mynation.name, 'MyNation')
        self.assertEqual(mynation.__repr__(), '<Nation MyNation>')
