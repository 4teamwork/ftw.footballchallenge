from ftw.footballchallenge.nation import Nation
from ftw.footballchallenge.game import Game
from ftw.footballchallenge.player import Player
from ftw.footballchallenge.goal import Goal
from ftw.footballchallenge.event import Event
from ftw.footballchallenge.card import Card
from ftw.footballchallenge.save import Save
from ftw.footballchallenge.team import Team
from ftw.footballchallenge.testing import DATABASE_LAYER
from datetime import datetime
import unittest2
from datetime import date, timedelta
from ftw.footballchallenge.Teams_Players import Teams_Players

class TestLogModel(unittest2.TestCase):
    
    layer = DATABASE_LAYER
    
    @property
    def session(self):
        return self.layer.session

    
    def test_creation(self):
        event = Event('TheEvent', date.today()+timedelta(days=1))
        self.session.add(event)
        # self.layer.commit()
        event = self.session.query(Event).one()
        nation1 = Nation('Nation1', event.id_, 'SWE')
        self.session.add(nation1)
        nation2 = Nation('Nation2', event.id_, 'GBR')
        self.session.add(nation2)
        nation3 = Nation('Nation3', event.id_, 'FRA')
        self.session.add(nation3)
        team1 = Team('TheTeam', 'testi.testmann')
        self.session.add(team1)
        # self.layer.commit()
        
        nations = self.session.query(Nation).all()
        event = self.session.query(Event).one()
        game = Game(datetime.now(), event.id_,'group1', nation1_id=nations[0].id_, nation2_id=nations[1].id_)
        game.score_nation1 = 3
        game.score_nation2 = 0
        game2 = Game(datetime.now(), event.id_,'group1', nation1_id=nations[0].id_, nation2_id=nations[2].id_)
        game2.score_nation1 = 0
        game2.score_nation2 = 1
        self.session.add(game)
        self.session.add(game2)
        # self.layer.commit()

        team = self.session.query(Team).first()
        nation = self.session.query(Nation).first()
        event = self.session.query(Event).one()
        player1 = Player('Freddy', 'midfield', nation.id_, event.id_)
        self.session.add(player1)
        # self.layer.commit()
        team = self.session.query(Team).first()
        player1 = self.session.query(Player).first()
        team.players.append(Teams_Players(team.id_, player1, is_starter=True))
        
        player1 = self.session.query(Player).one()
        game = self.session.query(Game).all()
        game[0].players.append(player1)
        game[1].players.append(player1)
        goal1 = Goal(player1.id_, game[0].id_, False)
        self.session.add(goal1)
        card1 = Card(player1.id_, game[0].id_, 'Yellow')
        self.session.add(card1)
        # self.layer.commit()
        player1 = self.session.query(Player).one()
        log = player1.get_log()
        goal = self.session.query(Goal).first()
        card = self.session.query(Card).first()
        self.assertEqual(len(log), 4)
        self.assertEqual(log[0][0], card)
        self.assertEqual(log[1][0], goal)
        self.assertEqual(log[2][1], 4)
        self.assertEqual(log[3][1], -2)

        team = self.session.query(Team).one()
