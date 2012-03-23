from ftw.footballchallenge.testing import DATABASE_LAYER
from ftw.footballchallenge.team import Team
from ftw.footballchallenge.nation import Nation
from ftw.footballchallenge.player import Player
import unittest2


class TestTeamModel(unittest2.TestCase):
    
    layer = DATABASE_LAYER
    
    @property
    def session(self):
        return self.layer.session

    def test_creation(self):
        team1 = Team('TheTeam', 'testi.testmann')
        self.session.add(team1)
        self.layer.commit()
        teams = self.session.query(Team).all()
        self.assertEquals(len(teams), 1)
        myteam = teams[0]
        self.assertEqual(myteam.name, 'TheTeam')
        self.assertEqual(myteam.__repr__(), '<Team TheTeam>')
        
    def test_addplayer(self):
        team1 = Team('TheTeam', 'testi.testmann')
        self.session.add(team1)
        self.layer.commit()
        
        nation1 = Nation('Nation1')
        self.session.add(nation1)
        self.layer.commit()
        mynation = self.session.query(Nation).one()
        player1 = Player('Freddy', 'Midfield', mynation.id_)
        self.session.add(player1)
        self.layer.commit()

        myteam = self.session.query(Team).one()
        player = self.session.query(Player).one()
        myteam.players.append(player)
        self.layer.commit()

        myteam = self.session.query(Team).one()
        player = self.session.query(Player).one()        
        self.assertEqual(len(myteam.players), 1)
        self.assertEqual(myteam.players[0].name, 'Freddy')
        self.assertEqual(len(player.teams), 1)
        self.assertEqual(player.teams[0].name, 'TheTeam')
        
