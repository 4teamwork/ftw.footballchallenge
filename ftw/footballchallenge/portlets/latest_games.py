from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from zope.interface import implements
from ftw.footballchallenge.game import Game
from sqlalchemy import desc
from z3c.saconfig import named_scoped_session


class ILatestGamesPortlet(IPortletDataProvider):
    """
    """


class Assignment(base.Assignment):
    implements(ILatestGamesPortlet)

    @property
    def title(self):
        return "Latest Games Portlet"


class Renderer(base.Renderer):

    def update(self):
        session = named_scoped_session('footballchallenge')
        games = session.query(Game).order_by(desc(Game.date)).all()[:3]
        self.games = games
    
    render = ViewPageTemplateFile('latest_games.pt')

    def get_link(self, game):
        portal_url = self.context.absolute_url()
        return '<a href="'+portal_url+'/game_view/'+str(game.id_)+'">'+game.nation1.name +' vs. '+game.nation2.name+'</a>'

class AddForm(base.NullAddForm):

    def create(self):
        return Assignment()
