from zope.publisher.browser import BrowserView
from z3c.saconfig import named_scoped_session
from ftw.footballchallenge.Teams_Players import Teams_Players
from zope.component.hooks import getSite 
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implements
from zope.publisher.interfaces import IPublishTraverse
from ftw.footballchallenge.playerstatistics import Playerstatistics
from ftw.footballchallenge.event import Event
import datetime
from ftw.footballchallenge import _
from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFCore.utils import getToolByName
from zExceptions import NotFound
from zope.publisher.interfaces import NotFound as PublishNotFound
from ftw.footballchallenge.team import Team


class TeamOverview(BrowserView):
    """Defines a view for the league which displays the ranking."""

    implements(IPublishTraverse)
    
    template = ViewPageTemplateFile("team_overview.pt")

    def __init__(self, context, request):
        super(TeamOverview, self).__init__(context, request)
        self.team_id = None
        self.team_name = ''


    def __call__(self):
        session = named_scoped_session('footballchallenge')
        open_events = session.query(Event).filter(Event.deadline > datetime.datetime.now()).all()
        mtool = getToolByName(self.context, 'portal_membership')
        user = mtool.getAuthenticatedMember()
        userid = user.getId()
        myteam = session.query(Team).filter(Team.user_id == userid).first()

        if not self.team_id:
            if myteam:
                self.team_id = myteam.id_
                self.team_name = myteam.name
                self.coach = user.getProperty('fullname')
            else:
                return self.request.RESPONSE.redirect(self.context.absolute_url() + '/edit_team')
        else:
            # Don't show other teams if event hasn't started yet
            if open_events:
                raise NotFound

            team = session.query(Team).filter(Team.id_ == self.team_id).first()
            if not team:
                raise NotFound
            self.team_name = team.name
            coach = mtool.getMemberById(team.user_id)
            self.coach = coach.getProperty('fullname')

        return self.template()

        
    def publishTraverse(self, request, name):
        if self.team_id is None:
            try:
                self.team_id = int(name)
            except ValueError:
                raise PublishNotFound(self, name, request)
        else:
            raise PublishNotFound(self, name, request)
        return self

    def get_players(self, starters):
        session = named_scoped_session('footballchallenge')
        teams_players = session.query(Teams_Players).filter_by(team_id=self.team_id).filter_by(is_starter=starters).all()
        players = []
        for team_player in teams_players:
            players.append(team_player.player)
        sorted_players = sorted(players, key=lambda player: player.position)
        for index, player in enumerate(sorted_players):
            if player.position == "keeper":
                sorted_players.insert(0, sorted_players.pop(index))
        return sorted_players
        
    def generate_link(self, player):
        portal = getSite()
        base_url = portal.absolute_url()
        url = base_url + '/player_view/' + str(player.id_)
        return '<a href="' + url + '">' + player.name + '</a>'
    
    def get_starters(self):
        return self.get_players(True)

    def get_substitutes(self):
        return self.get_players(False)

    def calculate_nations(self):
        session = named_scoped_session('footballchallenge')
        teams_players = session.query(Teams_Players).filter(Teams_Players.team_id==self.team_id).all()
        nations = []
        all_nations = []
        for team_player in teams_players:
            if team_player.is_starter == True:
                player = team_player.player
                if not player.nation_id in nations:
                    nations.append(player.nation_id)
                    if not player.nation_id in all_nations:
                        all_nations.append(player.nation_id)
            else:
                player = team_player.player
                if not player.nation_id in nations and not player.nation_id in all_nations:
                    all_nations.append(player.nation_id)
        return {'starter_nations': len(nations), 'sub_nations': len(all_nations)}

    def get_player_points(self, player):
        session = named_scoped_session('footballchallenge')
        playerstats = session.query(Playerstatistics).filter(Playerstatistics.player_id == player.id_).all()
        points = 0
        for playerstat in playerstats:
            points += playerstat.points
        return points