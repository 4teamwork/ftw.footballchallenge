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
        games = session.query(Game).filter(Game.events_id == event_id).order_by(Game.date).group_by(Game.round).all()
        game_dict = {}
        for game in games:
            if game_dict.get(game.stage, None):
                game_dict[game.round].append(game)
            else:
                game_dict[game.round] = [game]
        return game_dict

    def __call__(self):
        return self.template()