from ftw.footballchallenge.testing import DATABASE_LAYER
from ftw.footballchallenge.league import League
import unittest2


class TestLeagueModel(unittest2.TestCase):
    
    layer = DATABASE_LAYER
    
    @property
    def session(self):
        return self.layer.session

        def test_creation(self):
            league1 = League('TheLeague')
            self.session.add(league1)
            self.layer.commit()

            leagues = self.session.query(League).all()
            self.assertEquals(len(leagues), 1)
            myleague = leagues[0]
            self.assertEqual(myleague.name, 'TheLeague')