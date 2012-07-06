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
        event = self.session.query(Event).one()
        nation1 = Nation('Nation1', event.id_, 'SWE')
        self.session.add(nation1)
        nation2 = Nation('Nation2', event.id_, 'GBR')
        self.session.add(nation2)
        # self.layer.commit()
        nations = self.session.query(Nation).all()
        event = self.session.query(Event).one()
        game = Game(datetime.now(), event.id_,'group1', nation1_id=nations[0].id_, nation2_id=nations[1].id_)
        game.score_nation1 = 3
        game.score_nation2 = 0
        self.session.add(game)
        # self.layer.commit()
        team1 = Team('testi.testmann', event.id_, 'TheTeam')
        self.session.add(team1)
        # self.layer.commit()


        team = self.session.query(Team).one()
        game = self.session.query(Game).one()
        stats1 = Teamstatistics(team.id_, game.id_, 5)
        self.session.add(stats1)
        # self.layer.commit()
        team = self.session.query(Team).one()
        game = self.session.query(Game).one()
        stats = self.session.query(Teamstatistics).one()
        self.assertEqual(stats.__repr__(), '<Statistics for Team TheTeam. Points: 5>')
