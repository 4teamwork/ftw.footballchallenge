from zope.traversing.namespace import view
from z3c.saconfig import named_scoped_session
from ftw.footballchallenge.league import League
from Acquisition import ImplicitAcquisitionWrapper


class LeagueTraverse(view):
    
    def traverse(self, name, ignored):
        """docstring"""
        session = named_scoped_session('footballchallenge')
        obj = session.query(League).filter(League.id_==name).one()
        return ImplicitAcquisitionWrapper(obj, self.context)