from ftw.footballchallenge.testing import DATABASE_LAYER
from ftw.footballchallenge.team import Team
import unittest2


class TestTeamModel(unittest2.TestCase):
    
    layer = DATABASE_LAYER
    
    @property
    def session(self):
        return self.layer.session
        
    def test_creation_without_league(self):
        with self.assertRaises(TypeError):
            Team('TheTeam')

    def test_creation(self):
        team1 = Team('TheTeam')
        self.session.add(team1)
        self.layer.commit()
        teams = self.session.query(Team).all()
        self.assertEquals(len(teams), 1)
        myteam = teams[0]
        self.assertEqual(myteam.name, 'TheTeam') 