from ftw.footballchallenge.testing import DATABASE_LAYER
from ftw.footballchallenge.nation import Nation
from ftw.footballchallenge.player import Player
from ftw.footballchallenge.team import Team
from ftw.footballchallenge.league import League

import unittest2


class TestManytoMany(unittest2.TestCase):
    
    layer = DATABASE_LAYER
    
    @property
    def session(self):
        return self.layer.session
    
    def test_many_to_many(self):
        league1 = League('TheLeague')
        self.session.add(league1)
        nation = Nation('MyNation')
        self.session.add(nation)
        team1 = Team('TheTeam', league1)
        self.session.add(team1)
        player1 = Player('Freddy', 'midfield', nation)
        team1.players.append(player1)
        self.layer.commit()
        teams = self.session.query(Team).one()
        players = self.session.query(Player).one()
        self.assertEqual(len(teams.players), 1)
        self.assertEqual(teams.players.one(), players)
        self.assertEqual(len(players.teams),1)
        self.assertEqual(players.teams.one(), teams)