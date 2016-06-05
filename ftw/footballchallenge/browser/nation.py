from zope.interface import implements
from zope.publisher.browser import BrowserView
from zope.publisher.interfaces import IPublishTraverse, NotFound
from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.saconfig import named_scoped_session
from ftw.footballchallenge.nation import Nation


class NationView(BrowserView):

    implements(IPublishTraverse)

    template = ViewPageTemplateFile("nation.pt")


    def __init__(self, context, request):
        super(NationView, self).__init__(context, request)
        self.nation_id = None

    def __call__(self):
        return self.template()

    def publishTraverse(self, request, name):
        self.nation_id = name
        return self

    def nation(self):
        session = named_scoped_session('footballchallenge')
        nation = session.query(Nation).filter(
            Nation.id_ == self.nation_id).first()
        if nation is None:
            raise NotFound(self, self.nation_id, self.request)
        return nation

    def players(self):
        context = aq_inner(self.context)
        base_url = context.absolute_url()
        results = []
        for player in self.nation().players:
            info = dict(
                name=player.name,
                url='%s/%s' % (base_url.rstrip('/')+'/player_view', player.id_),
                position=context.translate(player.position, domain='ftw.footballchallenge'),
                age=player.age,
                club=player.club,
                league=player.league,
                value=player.pretty_value(),
                value_int=player.value,
            )
            results.append(info)
        return results
