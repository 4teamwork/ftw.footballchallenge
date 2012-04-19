from Acquisition import aq_inner
from zope.publisher.browser import BrowserView
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from z3c.saconfig import named_scoped_session
from ftw.footballchallenge.nation import Nation


class NationsView(BrowserView):
    """Shows a listing of all national teams."""

    template = ViewPageTemplateFile("nations.pt")

    def __call__(self):
        self.request.set('disable_border', True)
        return self.template()

    def nations(self):
        context = aq_inner(self.context)
        base_url = '%s/' % context.absolute_url()
        session = named_scoped_session('footballchallenge')
        results = []
        for nation in session.query(Nation).order_by(Nation.name).all():
            info = dict(
                title=nation.name,
                url=base_url + str(nation.id_),
                coach=nation.coach,
                participations=nation.participations,
                rank=nation.fifa_rank,
            )
            results.append(info)
        return results
