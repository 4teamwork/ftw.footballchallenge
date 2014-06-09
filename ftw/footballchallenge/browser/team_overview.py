from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ftw.footballchallenge.Teams_Players import Teams_Players
from ftw.footballchallenge.event import Event
from ftw.footballchallenge.playerstatistics import Playerstatistics
from ftw.footballchallenge.team import Team
from z3c.saconfig import named_scoped_session
from zExceptions import Unauthorized, NotFound
from zope.component.hooks import getSite
from zope.interface import implements
from zope.publisher.browser import BrowserView
from zope.publisher.interfaces import IPublishTraverse
import datetime


class TeamOverview(BrowserView):
    """Defines a view for the league which displays the ranking."""
    implements(IPublishTraverse)
    template = ViewPageTemplateFile("team_overview.pt")

    def __init__(self, context, request):
        super(TeamOverview, self).__init__(context, request)
        self.team_id = None
        self.team_name = 'My Team'
        self.coach = ''

    def __call__(self):
        mtool = getToolByName(self.context, 'portal_membership')
        userid = mtool.getAuthenticatedMember().getId()
        session = named_scoped_session('footballchallenge')
        myteam = session.query(Team).filter(Team.user_id == userid).first()

        # If there's no team_id in the url show the team of the currently
        # logged-in user or redirect to the edit form if the user hasn't yet
        # created a team.
        if not self.team_id:
            if myteam:
                self.team_id = int(myteam.id_)
                self.team_name = myteam.name
                self.coach = self.coach_name(myteam.user_id)
                return self.template()
            else:
                return self.request.RESPONSE.redirect(
                    self.context.absolute_url() + '/edit_team')
        # team_id of the currently logged-in user provided
        elif myteam and self.team_id == myteam.id_:
            self.team_name = myteam.name
            self.coach = self.coach_name(myteam.user_id)
            return self.template()

        # Other teams can only be viewed if the event already started.
        open_events = session.query(Event).filter(
            Event.deadline > datetime.datetime.now()).first()
        if open_events:
            raise Unauthorized

        # Check if a team with the given team_id exists.
        team = session.query(Team).filter(Team.id_ == self.team_id).first()
        if not team:
            raise NotFound

        self.team_name = team.name
        self.coach = self.coach_name(team.user_id)
        return self.template()

    def publishTraverse(self, request, name):
        try:
            self.team_id = int(name)
        except ValueError:
            raise NotFound
        return self

    def coach_name(self, userid):
        mtool = getToolByName(self.context, 'portal_membership')
        member = mtool.getMemberById(userid)
        if not member:
            return userid
        return member.getProperty('fullname', userid) or userid

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
        url = base_url + '/player/' + str(player.id_)
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