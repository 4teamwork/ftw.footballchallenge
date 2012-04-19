from zope.interface import implements
from zope.publisher.browser import BrowserView
from zope.publisher.interfaces import IPublishTraverse, NotFound
from z3c.saconfig import named_scoped_session
from ftw.footballchallenge.player import Player


class PlayerImageView(BrowserView):
    implements(IPublishTraverse)

    def __init__(self, context, request):
        super(PlayerImageView, self).__init__(context, request)
        self.player_id = None

    def __call__(self):
        session = named_scoped_session('footballchallenge')
        player = session.query(Player).filter(
            Player.id_ == self.player_id).first()
        if player is None:
            raise NotFound(self, self.player_id, self.request)

        self.request.response.setHeader('Content-Type', 'image/jpeg')
        self.request.response.write(player.image)

    def publishTraverse(self, request, name):
        if self.player_id is None:
            self.player_id = name
        return self
