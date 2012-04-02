from zope.publisher.browser import BrowserView
from z3c.saconfig import named_scoped_session
from ftw.footballchallenge.teamstatistics import Teamstatistics
from ftw.footballchallenge.team import Team

class Ranking(BrowserView):
    """Defines a view for the league which displays the ranking."""

    def get_ranking(self):
        """Gets the teams and Totalpoints in right order"""
        session = named_scoped_session('footballchallenge')
        teams = session.query(Team).filter(Team.league_id==self.context.id_).all()
        ranking = session.query(Teamstatistics).filter(\
        Teamstatistics.team in self.context.teams).order_by(\
        Teamstatistics.total_points).all()
        return ranking
