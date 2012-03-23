from ftw.footballchallenge.testing import DATABASE_LAYER
from ftw.footballchallenge.league import League
from ftw.footballchallenge.event import Event
import unittest2


class TestLeagueModel(unittest2.TestCase):
    
    layer = DATABASE_LAYER
    
    @property
    def session(self):
        return self.layer.session

    def test_creation(self):
        
        event1 = Event("TheEvent")
        self.session.add(event1)
        self.layer.commit()
        myevent = self.session.query(Event).one()
        # can't take the event directly because it's not assigned to a session.
        # Without session sqlalchemy cant get any information

        league1 = League('TheLeague', myevent.id_)
        self.session.add(league1)
        self.layer.commit()

        leagues = self.session.query(League).all()
        self.assertEquals(len(leagues), 1)
        myleague = leagues[0]
        self.assertEqual(myleague.name, 'TheLeague')
        self.assertEqual(myleague.__repr__(), '<League TheLeague>')