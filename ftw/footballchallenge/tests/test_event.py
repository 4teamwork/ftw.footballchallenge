from ftw.footballchallenge.testing import DATABASE_LAYER
from ftw.footballchallenge.event import Event
import unittest2
from datetime import date, timedelta

class TestEventModel(unittest2.TestCase):
    
    layer = DATABASE_LAYER
    
    @property
    def session(self):
        return self.layer.session

    def test_creation(self):
        event1 = Event('TheEvent', date.today()+timedelta(days=1))
        self.session.add(event1)
        self.layer.commit()

        events = self.session.query(Event).all()
        self.assertEquals(len(events), 1)
        myevent = events[0]
        self.assertEqual(myevent.name, 'TheEvent')
        self.assertEqual(myevent.__repr__(),'<Event TheEvent>')