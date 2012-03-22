from ftw.footballchallenge.testing import DATABASE_LAYER
from ftw.footballchallenge.nation import Nation
from ftw.footballchallenge.game import Game
from ftw.footballchallenge.player import Player
import unittest2


class TestGameModel(unittest2.TestCase):
    
    layer = DATABASE_LAYER
    
    @property
    def session(self):
        return self.layer.session

    
    def test_creation(self):
        nation1 = Nation('Nation1')
        self.session.add(nation1)
        nation2 = Nation('Nation2')
        self.session.add(nation2)
        game = Game(nation1, nation2, '3:0')
        self.session.add(game)
        self.layer.commit()
        games = self.session.query(Game).all()
        self.assertEqual(len(games), 1)
        self.assertEqual(games[0], game)
        
    def test_mtom_nations(self):
        games = self.session.query(Game).all()
        nations = self.session.query(Nation).all()
        self.assertEqual(games.nations[0], nations[0])
        self.assertEqual(games.nations[1], nations[1])

    def test_mtom_players(self):
        game = self.session.query(Game).one()
        nations = self.session.query(Nation).all()
        player1 = Player('Freddy', 'midfield', nations[0])
        player2 = Player('Hans', 'defence', nations[0])
        game.players.append(player1)
        game.players.append(player2)
        self.layer.commit()
        game = self.session.query(Game).one()
        players = self.session.query(Player).all()
        self.assertEqual(len(game.players), 2)
        self.assertEqual(players[0].games, game)