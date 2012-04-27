from zope.publisher.browser import BrowserView
from z3c.saconfig import named_scoped_session
from ftw.footballchallenge.Teams_Players import Teams_Players
from zope.app.component.hooks import getSite 
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from zope.interface import implements
from zope.publisher.interfaces import IPublishTraverse


class TeamOverview(BrowserView):
    """Defines a view for the league which displays the ranking."""

    implements(IPublishTraverse)
    
    template = ViewPageTemplateFile("team_overview.pt")

    def __call__(self):
        return self.template()

    def publishTraverse(self, request, name):
        self.team_id = name
        return self

    def get_players(self, starters):
        session = named_scoped_session('footballchallenge')
        teams_players = session.query(Teams_Players).filter_by(team_id=self.team_id).filter_by(is_starter=starters).all()
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

    def calculate_nations(self):
        session = named_scoped_session('footballchallenge')
        teams_players = session.query(Teams_Players).filter(Teams_Players.team_id==self.team_id).all()
        nations = []
        sub_nations = []
        for team_player in teams_players:
            if team_player.is_starter == True:
                player = team_player.player
                if not player.nation_id in nations and not player.nation_id in sub_nations:
                    nations.append(player.nation_id)
            else:
                player = team_player.player
                if not player.nation_id in nations and not player.nation_id in sub_nations:
                    sub_nations.append(player.nation_id)
        return {'starter_nations': len(nations), 'sub_nations': len(sub_nations)+len(nations)}
