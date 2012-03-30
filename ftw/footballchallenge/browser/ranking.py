from zope.publisher.browser import BrowserView
from z3c.saconfig import named_scoped_session
from ftw.footballchallenge.teamstatistics import Teamstatistics

class Ranking(BrowserView):
    
    def get_ranking(self):
        session = named_scoped_session('footballchallenge')
        ranking = session.query(Teamstatistics).filter(Teamstatistics.team.league_id==self.id_).order_by(Teamstatistics.total_points).all()
        return ranking