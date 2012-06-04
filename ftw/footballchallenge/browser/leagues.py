from z3c.saconfig import named_scoped_session
from ftw.footballchallenge.event import Event
from ftw.footballchallenge.league import League
from ftw.footballchallenge.browser.ranking import Ranking
from zope.component import provideAdapter, queryMultiAdapter
from ftw.tabbedview.browser.tabbed import TabbedView
from ftw.footballchallenge import _
from zope.publisher.interfaces.browser import IBrowserView
from zope.interface import Interface

def league_tab_factory_generator(leagueid):
   def factory(context, request):
       return Ranking(context, request, leagueid)
   return factory


class LeaguesView(TabbedView):
    """Shows an overview of all national teams or the player listing of a
    specific national team if it's id is given in the url or the detail view
    of a player if a player id is given in the url.
    
    /@@nations     -> overview of all national teams
    /@@nations/1   -> player listing for national team with id 1
    /@@nations/1/2 -> detail view for player with id 2
    """
    def get_tabs(self):
        tabs = []
        session = named_scoped_session("footballchallenge")
        event_id = session.query(Event).all()[-1].id_
        leagues = session.query(League).filter(League.event_id == event_id).all()

        for league in leagues:
            self.register_league_tab(league)
            tabs.append({'id': _('league-%i' % league.id_, default=league.name),
                         'class': ''})

        return tabs

    def register_league_tab(self, league):
        name = 'tabbedview_view-league-%s' % league.id_
        if queryMultiAdapter((self.context, self.request), name=name) is None:
            provideAdapter(league_tab_factory_generator(league.id_),
                provides=IBrowserView,
                adapts=[Interface, Interface],
                name=name)
        return name
