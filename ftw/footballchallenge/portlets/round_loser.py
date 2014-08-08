from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from zope.interface import implements
from ftw.footballchallenge.game import Game
from ftw.footballchallenge.teamstatistics import Teamstatistics
from sqlalchemy import desc
from z3c.saconfig import named_scoped_session
from operator import itemgetter


class IRoundLoserPortlet(IPortletDataProvider):
    """
    """


class Assignment(base.Assignment):
    implements(IRoundLoserPortlet)

    @property
    def title(self):
        return "Winner/loser of the Round Portlet"


class Renderer(base.Renderer):

    def update(self):
        session = named_scoped_session('footballchallenge')
        last_game = session.query(Game).filter(Game.calculated == True).order_by(desc(Game.date)).first()
        self.ranking = None
        if last_game:
            round_ = last_game.round_
            gameids = session.query(Game.id_).filter_by(calculated = True).filter_by(round_ = round_).all()
            teamstats = session.query(Teamstatistics).filter(Teamstatistics.game_id.in_(gameids)).all()
            teams = {}
            for teamstat in teamstats:
                if not teams.get(teamstat.team_id):
                    teams[teamstat.team_id] = {'team': teamstat.team, 'points':teamstat.points}
                else:
                    teams[teamstat.team_id]['points'] += teamstat.points
        
            self.ranking = sorted(teams.iteritems(), key=lambda (k,v): itemgetter(1)(v))


    def get_loser(self):
        if self.ranking:
            return self.ranking[0][0].team.manager
    
    def get_winner(self):
        if self.ranking:
            return self.ranking[-1][0].team.manager
    
    def render(self):
        if self.ranking:
            return ViewPageTemplateFile('round_loser.pt')
        
class AddForm(base.NullAddForm):

    def create(self):
        return Assignment()
