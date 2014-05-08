from zope.publisher.browser import BrowserView
from z3c.saconfig import named_scoped_session
from ftw.footballchallenge.teamstatistics import Teamstatistics
from ftw.footballchallenge.team import Team
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from sqlalchemy import desc
from ftw.footballchallenge import _
from ftw.footballchallenge.league import League
from zope.interface import implements
from zope.publisher.interfaces import IPublishTraverse


class Ranking(BrowserView):
    """Defines a view for the league which displays the ranking."""
    
    template = ViewPageTemplateFile("ranking.pt")

    
    def get_ranking(self):
        """Gets the teams and Totalpoints in right order"""
        session = named_scoped_session('footballchallenge')
        
        league = session.query(League).filter(League.id_ == self.league_id).one()
        teams = league.teams
        team_ids = [team.id_ for team in teams]
        ranking = session.query(Teamstatistics).filter(Teamstatistics.team_id.in_(team_ids)).order_by(desc(Teamstatistics.game_id)).all()
        teams_in_ranking = {}
        for rank in ranking:
            teams_in_ranking[rank.team_id] = teams_in_ranking.get(rank.team_id, 0) + rank.points
        clean_ranking = sorted(teams_in_ranking.items(), key=lambda k: k[1], reverse=True)
        correct_ranks = []
        rank = 1
        last_rank = 1
        for index, team in enumerate(clean_ranking):
            if index >= 1:
                if clean_ranking[index-1][1] == team[1]:
                    correct_ranks.append([last_rank, team])
                    rank += 1
                else:
                    correct_ranks.append([rank, team])
                    last_rank = rank
                    rank += 1
            else:
                correct_ranks.append([last_rank, team])
                rank += 1
        return correct_ranks
            
        
        return clean_ranking

    def __init__(self, context, request, league_id):
        super(Ranking, self).__init__(context, request)
        self.league_id = league_id
    
    def __call__(self):
        return self.template()


    def get_link(self, team_id):
        session = named_scoped_session('footballchallenge')
        team = session.query(Team).filter(Team.id_ == team_id).one()
        portal_url = getToolByName(self.context, 'portal_url')
        portal = portal_url.getPortalObject()
        url = portal.absolute_url()
        link = '<a href="%s/team_overview/%s">%s</a>' % (url, team.id_, team.name)
        return link

    def get_userimg(self, team_id):
        session = named_scoped_session('footballchallenge')
        team = session.query(Team).filter(Team.id_ == team_id).one()
        portal_membership = getToolByName(self.context, 'portal_membership')
        userid = team.user_id
        portrait = portal_membership.getPersonalPortrait(userid)
        return portrait.tag()

    def coach(self, team_id):
        session = named_scoped_session('footballchallenge')
        team = session.query(Team).filter(Team.id_ == team_id).one()
        mtool = getToolByName(self.context, 'portal_membership')
        user = mtool.getMemberById(team.user_id)
        return user.getProperty('fullname')
        

    def checkManageEvent(self):
        portal_membership = getToolByName(self.context, 'portal_membership')
        member = portal_membership.getAuthenticatedMember()
        return member.has_permission('ftw.footballchallenge: Manage Event', self.context)