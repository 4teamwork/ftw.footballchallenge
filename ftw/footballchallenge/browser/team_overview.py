from zope.publisher.browser import BrowserView
from z3c.saconfig import named_scoped_session
from ftw.footballchallenge.Teams_Players import Teams_Players
from zope.app.component.hooks import getSite 
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile


class TeamOverview(BrowserView):
    """Defines a view for the league which displays the ranking."""

    
    template = ViewPageTemplateFile("team_overview.pt")

    def __call__(self):
        self.request['disable_plone.leftcolumn'] = True
        self.request['disable_plone.rightcolumn'] = True
        self.context.Title = self.context.name
        return self.template()
    
    def get_players(self, starters):
        session = named_scoped_session('footballchallenge')
        teams_players = session.query(Teams_Players).filter_by(team_id=self.context.id_).filter_by(is_starter=starters).all()
        players = []
        for team_player in teams_players:
            players.append(team_player.player)
        return players
        
    def generate_link(self, player):
        portal = getSite()
        base_url = portal.absolute_url()
        url = base_url + '/++player++'+str(player.id_)+'/player_view'
        return '<a href="'+url+'">'+player.name+'</a>'
    
    def get_starters(self):
        return self.get_players(True)

    def get_substitutes(self):
        return self.get_players(False)