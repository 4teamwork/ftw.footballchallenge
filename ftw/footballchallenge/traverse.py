from zope.traversing.namespace import view
from z3c.saconfig import named_scoped_session
from ftw.footballchallenge.league import League
from ftw.footballchallenge.game import Game
from ftw.footballchallenge.team import Team
from ftw.footballchallenge.player import Player
from ftw.footballchallenge.event import Event
from Acquisition import ImplicitAcquisitionWrapper


class LeagueTraverse(view):
    """A Traverseadapter for League"""

    def traverse(self, name, ignored):
        """get the right object"""
        session = named_scoped_session('footballchallenge')
        obj = session.query(League).filter(League.id_==name).one()
        return ImplicitAcquisitionWrapper(obj, self.context)


class PlayerTraverse(view):
    """A Traverseadapter for Player"""

    def traverse(self, name, ignored):
        """get the right object"""
        session = named_scoped_session('footballchallenge')
        obj = session.query(Player).filter(Player.id_==name).one()
        return ImplicitAcquisitionWrapper(obj, self.context)

class TeamTraverse(view):
    """A Traverseadapter for League"""

    def traverse(self, name, ignored):
        """get the right object"""
        session = named_scoped_session('footballchallenge')
        obj = session.query(Team).filter(Team.id_==name).one()
        return ImplicitAcquisitionWrapper(obj, self.context)

class GameTraverse(view):
    """A Traverseadapter for League"""

    def traverse(self, name, ignored):
        """get the right object"""
        session = named_scoped_session('footballchallenge')
        obj = session.query(Game).filter(Game.id_==name).one()
        return ImplicitAcquisitionWrapper(obj, self.context)

class EventTraverse(view):
    """A Traverseadapter for League"""

    def traverse(self, name, ignored):
        """get the right object"""
        session = named_scoped_session('footballchallenge')
        obj = session.query(Event).filter(Event.id_==name).one()
        return ImplicitAcquisitionWrapper(obj, self.context)
