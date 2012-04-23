from zope.publisher.browser import BrowserView
from z3c.saconfig import named_scoped_session
from ftw.footballchallenge.teamstatistics import Teamstatistics
from ftw.footballchallenge.team import Team
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from sqlalchemy import desc
from ftw.footballchallenge import _
from ftw.footballchallenge.league import League
from zope.interface import implements
from zope.publisher.interfaces import IPublishTraverse


class Ranking(BrowserView):
    """Defines a view for the league which displays the ranking."""
    
    template = ViewPageTemplateFile("ranking.pt")

    implements(IPublishTraverse)    
    
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
        return clean_ranking

    
    def __call__(self):
        self.context.Title = _(u"Ranking", default=u"Rangliste").encode('utf-8')
        self.request['disable_plone.leftcolumn'] = True
        self.request['disable_plone.rightcolumn'] = True
        return self.template()

    def publishTraverse(self, request, name):
        self.league_id = name
        return self

    def get_link(self, team_id):
        session = named_scoped_session('footballchallenge')
        team = session.query(Team).filter(Team.id_ == team_id).one()
        portal_url = getToolByName(self.context, 'portal_url')
        portal = portal_url.getPortalObject()
        url = portal.absolute_url()
        link = '<a href="%s/++team++%s/team_overview">%s</a>' % (url, team.id_, team.name)
        return link

    def get_userimg(self, team_id):
        session = named_scoped_session('footballchallenge')
        team = session.query(Team).filter(Team.id_ == team_id).one()
        portal_membership = getToolByName(self.context, 'portal_membership')
        userid = team.user_id
        portrait = portal_membership.getPersonalPortrait(userid)
        return portrait.tag()
