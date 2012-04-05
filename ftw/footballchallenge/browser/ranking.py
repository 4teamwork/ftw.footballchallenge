from zope.publisher.browser import BrowserView
from z3c.saconfig import named_scoped_session
from ftw.footballchallenge.teamstatistics import Teamstatistics
from ftw.footballchallenge.team import Team
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from sqlalchemy import desc
from ftw.footballchallenge import _

class Ranking(BrowserView):
    """Defines a view for the league which displays the ranking."""
    
    template = ViewPageTemplateFile("ranking.pt")
    
    def get_ranking(self):
        """Gets the teams and Totalpoints in right order"""
        session = named_scoped_session('footballchallenge')
        
        league_id = self.context.id_
        teams = session.query(Team).filter(Team.league_id == league_id).all()
        team_ids = [team.id_ for team in teams]
        
        ranking = session.query(Teamstatistics).filter(Teamstatistics.team_id.in_(team_ids)).order_by(desc(Teamstatistics.total_points)).all()
        teams_in_ranking = []
        clean_ranking = []
        for rank in ranking:
            if not rank.team_id in teams_in_ranking:
                 clean_ranking.append(rank)
                 teams_in_ranking.append(rank.team_id)
        return clean_ranking

    
    def __call__(self):
        self.context.Title = _(u"Ranking", default=u"Rangliste").encode('utf-8')
        self.request['disable_plone.leftcolumn'] = True
        self.request['disable_plone.rightcolumn'] = True
        return self.template()


    def get_link(self, stat):
        portal_url = getToolByName(self.context, 'portal_url')
        portal = portal_url.getPortalObject()
        url = portal.absolute_url()
        link = '<a href="%s/++team++%s/team_overview">%s</a>' % (url, stat.team.id_, stat.team.name)
        return link

    def get_userimg(self, stat):
        portal_membership = getToolByName(self.context, 'portal_membership')
        userid = stat.team.user_id
        portrait = portal_membership.getPersonalPortrait(userid)
        return portrait.tag()
