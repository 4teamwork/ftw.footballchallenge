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

    def __init__(self, context, request):
        super(NationsView, self).__init__(context, request)
        self.nation_id = None
        self.player_id = None

    def __call__(self):
        self.request.set('disable_border', True)
        return self.template_overview()

    def publishTraverse(self, request, name):
        if self.nation_id is None:
            self.nation_id = name
        elif self.player_id is None:
            self.player_id = name
        return self

    def nations(self):
        context = aq_inner(self.context)
        base_url = context.absolute_url()
        session = named_scoped_session('footballchallenge')
        results = []
        for nation in session.query(Nation).order_by(Nation.name).all():
            info = dict(
                title=nation.name,
                url='%s/%s' % (base_url.rstrip('/')+'/nation', nation.id_),
                coach=nation.coach,
                participations=nation.participations,
                rank=nation.fifa_rank,
            )
            results.append(info)
        return results


