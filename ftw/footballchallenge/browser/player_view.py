from zope.publisher.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implements
from zope.publisher.interfaces import IPublishTraverse
from z3c.saconfig import named_scoped_session
from ftw.footballchallenge.player import Player
from ftw.footballchallenge.event import Event
import datetime


class PlayerView(BrowserView):
    """Defines a view for the league which displays the ranking."""
    implements(IPublishTraverse)

    template = ViewPageTemplateFile("player_view.pt")

    def __init__(self, context, request):
        super(PlayerView, self).__init__(context, request)
        self.request.set('disable_border', 1)

    def __call__(self):
        return self.template()

    def publishTraverse(self, request, name):
        self.player_id = name
        return self

    def get_player(self):
        if self.player_id:
            session = named_scoped_session('footballchallenge')
            player = session.query(Player).filter(
                Player.id_ == self.player_id).first()
            return player

    def check_teams_public(self):
        session = named_scoped_session('footballchallenge')
        open_events = session.query(Event).filter(
            Event.deadline > datetime.datetime.now()).all()
        if not open_events:
            return True
        return False
