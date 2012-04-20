from zope.publisher.browser import BrowserView
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter
from zExceptions import Forbidden
from ftw.footballchallenge.game import Game
from ftw.footballchallenge.player import Player
from ftw.footballchallenge.card import Card
from ftw.footballchallenge.save import Save
from ftw.footballchallenge.goal import Goal

from z3c.saconfig import named_scoped_session
from zope.interface import implements
from zope.publisher.interfaces import IPublishTraverse


class EnterResults(BrowserView):
    """A Form for enter Match Results."""
    
    implements(IPublishTraverse)
    
    template = ViewPageTemplateFile("enter_results.pt")
    
    def update(self):
        import pdb; pdb.set_trace( )
        if 'submited' in self.request.form:
            authenticator = getMultiAdapter((self.context, self.request), name=u"authenticator")
            if not authenticator.verify():
                raise Forbidden()
        super(EnterResults, self).update()
    
    def __call__(self):
        if self.request.form.get('form.submited'):
            playing_players = self.request.form.get('played', {})
            yellow = self.request.form.get('yellow', {})
            second_yellow = self.request.form.get('2ndyellow', {})
            red = self.request.form.get('red', {})
            goals = self.request.form.get('goals', {})
            saves = self.request.form.get('saves', {})
            self.write_to_db(playing_players, yellow, second_yellow, red, goals, saves)
            self.request.set('disable_border', True)
            authenticator = getMultiAdapter((self.context, self.request), name=u"authenticator")
            if not authenticator.verify():
                raise Forbidden()

        else:
            session = named_scoped_session('footballchallenge')
            game = session.query(Game).filter(Game.id_ == self.game_id).one()
            for player in game.players:
                self.request.form[str(player.id_)+'_played'] = "checked"
            for card in game.cards:
                self.request.form[str(card.player_id)+'_'+card.color] = "checked"
            for goal in game.goals:
                self.request.form[str(goal.player_id)+'_goals'] = 1 + self.request.form.get(str(goal.player_id)+'_goals', 0)
            for save in game.saves:
                self.request.form[str(save.player_id)+'_goals'] = 1 + self.request.form.get(str(save.player_id)+'_saves', 0)
        return self.template()
    
    def publishTraverse(self, request, name):
        self.game_id = name
        return self
    
    def get_home_team(self):
        session = named_scoped_session('footballchallenge')
        game = session.query(Game).filter(Game.id_ == self.game_id).one()
        home = game.nation1
        players = home.players
        return players

    def get_visitor_team(self):
        session = named_scoped_session('footballchallenge')
        game = session.query(Game).filter(Game.id_ == self.game_id).one()
        visitor = game.nation2
        players = visitor.players
        return players

    def write_to_db(self, playing_players, yellow, second_yellow, red, goals, saves):
        session = named_scoped_session('footballchallenge')
        game = session.query(Game).filter(Game.id_ == self.game_id).one()
        if playing_players:
            players = playing_players.keys()
            for player_id in players:
                player = session.query(Player).filter(Player.id_ == player_id).one()
                game.players.append(player)
        if yellow:
            players = yellow.keys()
            self.write_cards(players, "yellow", game, session)
        if second_yellow:
            players = second_yellow.keys()
            self.write_cards(players, "second_yellow", game, session)
        if red:
            players = red.keys()
            self.write_cards(players, "red", game, session)
        for key, value in goals.items():
            if not value == '':
                try:
                    value_int = int(value)
                except ValueError:
                    continue
                for count in range(0, value_int):
                    goal = Goal(key, game.id_, False)
                    session.add(goal)
        for key, value in saves.items():
            if not value == '':
                try:
                    value_int = int(value)
                except ValueError:
                    continue
                for count in range(0, value_int):
                    save = Save(key, game.id_)
                    session.add(save)


    def write_cards(self, player_ids, color, game, session):
        for player_id in player_ids:
            card = Card(player_id, game.id_, "yellow")
            session.add(card)
            
        