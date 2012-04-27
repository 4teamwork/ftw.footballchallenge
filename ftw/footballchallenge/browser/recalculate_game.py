from zope.publisher.browser import BrowserView
from z3c.saconfig import named_scoped_session
from ftw.footballchallenge.game import Game
from ftw.footballchallenge.playerstatistics import calculate_player_points
from ftw.footballchallenge.teamstatistics import calculate_team_points
import transaction

class CalculateGameView(BrowserView):

    def __call__(self):
        session = named_scoped_session('footballchallenge')
        games = session.query(Game).filter(Game.calculated == False).all()
        for game in games:
            calculate_player_points(game)
            calculate_team_points(game)
            game.calculated = True
        transaction.commit()
        return self.request.response.redirect(self.context.absolute_url())
        