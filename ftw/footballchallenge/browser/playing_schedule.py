from zope.publisher.browser import BrowserView
from z3c.saconfig import named_scoped_session
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
import datetime
from ftw.footballchallenge.event import Event
from ftw.footballchallenge.game import Game


class PlayingScheduleView(BrowserView):
    """Defines a view for the league which displays the ranking."""
    
    template = ViewPageTemplateFile("playing_schedule.pt")


    def get_games(self):
        session = named_scoped_session('footballchallenge')
        event_id = session.query(Event).filter(Event.LockDate > datetime.date.today()).one().id_
        games = session.query(Game).filter(Game.events_id == event_id).order_by(Game.date).all()
        games_per_round = {}
        for game in games:
            if game.round_ in games_per_round:
                games_per_round[game.round_].append(game)
            else:
                games_per_round[game.round_] = [game]
        return games_per_round

    def __call__(self):
        return self.template()