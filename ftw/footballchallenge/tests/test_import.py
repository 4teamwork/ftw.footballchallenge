import unittest2
from ftw.footballchallenge.event import Event
from ftw.footballchallenge.testing import DATABASE_LAYER
from ftw.footballchallenge.nation import Nation
from ftw.footballchallenge.playerimport import import_team
from ftw.footballchallenge.player import Player

class TestImport(unittest2.TestCase):
    
    
    layer = DATABASE_LAYER
    
    @property
    def session(self):
        return self.layer.session
    
    
    def test_import(self):
        import_team(['http://www.transfermarkt.ch/de/russland/startseite/nationalmannschaft_3448.html'], self.session)
        query = self.session.query(Player).all()
        for player in query:
            print player.original_name
        self.assertEqual(len(query), 23)
        