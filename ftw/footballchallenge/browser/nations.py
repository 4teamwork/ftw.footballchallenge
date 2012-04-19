from Acquisition import aq_inner
from zope.interface import implements
from zope.publisher.browser import BrowserView
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from zope.publisher.interfaces import IPublishTraverse, NotFound
from z3c.saconfig import named_scoped_session
from ftw.footballchallenge.nation import Nation
from ftw.footballchallenge.player import Player


class NationsView(BrowserView):
    """Shows an overview of all national teams or the player listing of a
    specific national team if it's id is given in the url or the detail view
    of a player if a player id is given in the url.
    
    /@@nations     -> overview of all national teams
    /@@nations/1   -> player listing for national team with id 1
    /@@nations/1/2 -> detail view for player with id 2
    """
    implements(IPublishTraverse)

    template_overview = ViewPageTemplateFile("nations.pt")
    template_nation = ViewPageTemplateFile("nation.pt")
    template_player = ViewPageTemplateFile("player.pt")

    def __init__(self, context, request):
        super(NationsView, self).__init__(context, request)
        self.nation_id = None
        self.player_id = None

    def __call__(self):
        self.request.set('disable_border', True)
        if self.player_id is not None:
            return self.template_player()
        if self.nation_id is not None:
            return self.template_nation()
        return self.template_overview()

    def publishTraverse(self, request, name):
        if self.nation_id is None:
            self.nation_id = name
        elif self.player_id is None:
            self.player_id = name
        return self

    def nations(self):
        context = aq_inner(self.context)
        base_url = self.request.get('ACTUAL_URL', context.absolute_url()) 
        session = named_scoped_session('footballchallenge')
        results = []
        for nation in session.query(Nation).order_by(Nation.name).all():
            info = dict(
                title=nation.name,
                url='%s/%s' % (base_url.rstrip('/'), nation.id_),
                coach=nation.coach,
                participations=nation.participations,
                rank=nation.fifa_rank,
            )
            results.append(info)
        return results

    def nation(self):
        session = named_scoped_session('footballchallenge')
        nation = session.query(Nation).filter(
            Nation.id_ == self.nation_id).first()
        if nation is None:
            raise NotFound(self, self.nation_id, self.request)
        return nation

    def players(self):
        context = aq_inner(self.context)
        base_url = self.request.get('ACTUAL_URL', context.absolute_url()) 
        results = []
        for player in self.nation().players:
            info = dict(
                name=player.name,
                url='%s/%s' % (base_url.rstrip('/'), player.id_),
                position=player.position,
                age=player.age,
                club=player.club,
                value=player.value,
            )
            results.append(info)
        return results

    def player(self):
        session = named_scoped_session('footballchallenge')
        player = session.query(Player).filter(
            Player.id_ == self.player_id).first()
        if player is None:
            raise NotFound(self, self.player_id, self.request)
        return player
