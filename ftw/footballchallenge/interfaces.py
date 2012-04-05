from zope.interface import Interface


class IEditTeam(Interface):
    """Interface to override macros.pt"""


class IFootballchallengeLayer(Interface):
    """ftw.datepicker browser layer
    """


class ILeague(Interface):
    """Marker interface for League"""

class ITeam(Interface):
    """Marker interface for League"""

class IPlayer(Interface):
    """Marker interface for League"""

class IGame(Interface):
    """Marker interface for League"""

class INation(Interface):
    """Marker interface for League"""

class IEvent(Interface):
    """Marker interface for League"""
