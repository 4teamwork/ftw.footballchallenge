from ftw.footballchallenge.nation import Nation
from ftw.footballchallenge.game import Game
from ftw.footballchallenge.event import Event
from ftw.footballchallenge.teamstatistics import Teamstatistics
from datetime import date, datetime, timedelta
from ftw.footballchallenge.testing import DATABASE_LAYER
from ftw.footballchallenge.team import Team
import unittest2

class TestTeamstatsModel(unittest2.TestCase):
    
    layer = DATABASE_LAYER
    
    @property
    def session(self):
        return self.layer.session

    def test_creation(self):
        event1 = Event('TheEvent', date.today()+timedelta(days=1))
        self.session.add(event1)        
        nation1 = Nation('Nation1')
        self.session.add(nation1)
        nation2 = Nation('Nation2')
        self.session.add(nation2)
        self.layer.commit()
        nations = self.session.query(Nation).all()
        event = self.session.query(Event).one()
        game = Game(nations[0].id_, nations[1].id_, datetime.now(), event.id_, 3, 0)
        self.session.add(game)
        self.layer.commit()
        team1 = Team('TheTeam', 'testi.testmann')
        self.session.add(team1)
        self.layer.commit()


        team = self.session.query(Team).one()
        game = self.session.query(Game).one()
        stats1 = Teamstatistics(team.id_, game.id_, 5, 500)
        self.session.add(stats1)
        self.layer.commit()
        team = self.session.query(Team).one()
        game = self.session.query(Game).one()
        stats = self.session.query(Teamstatistics).one()
        self.assertEqual(stats.__repr__(), '<Statistics for Team TheTeam. Total Points: 500>')
        self.assertEqual(team.get_points(self.session), 500)
        self.assertEqual(team.get_points_for_game(game.id_, self.session), 5)
