from zope.publisher.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter
from zExceptions import Forbidden
from ftw.footballchallenge.game import Game
from ftw.footballchallenge.player import Player
from ftw.footballchallenge.card import Card
from ftw.footballchallenge.save import Save
from ftw.footballchallenge.goal import Goal
from ftw.footballchallenge.playerstatistics import calculate_player_points
from ftw.footballchallenge.teamstatistics import calculate_team_points
from z3c.saconfig import named_scoped_session
from sqlalchemy.orm.exc import NoResultFound
from zope.interface import implements
from zope.publisher.interfaces import IPublishTraverse, NotFound
from ftw.footballchallenge.assist import Assist

class EnterResults(BrowserView):
    """A Form for enter Match Results."""
    
    implements(IPublishTraverse)
    
    template = ViewPageTemplateFile("enter_results.pt")

    def __init__(self, context, request):
        super(EnterResults, self).__init__(context, request)
        self.game_id = None

    def __call__(self):
        self.request.set('disable_border', True)
        if self.request.form.get('form.submited'):
            authenticator = getMultiAdapter((self.context, self.request), name=u"authenticator")
            if not authenticator.verify():
                raise Forbidden()
            playing_players = self.request.form.get('played', {})
            yellow = self.request.form.get('yellow', {})
            second_yellow = self.request.form.get('2ndyellow', {})
            red = self.request.form.get('red', {})
            goals = self.request.form.get('goals', {})
            saves = self.request.form.get('saves', {})
            penaltys = self.request.form.get('penalty', {})
            assists = self.request.form.get('assists', {})

            self.write_to_db(playing_players, yellow, second_yellow, red, goals, penaltys, assists, saves)
            self.request.response.redirect(self.context.absolute_url() + '/schedule')
        else:
            session = named_scoped_session('footballchallenge')
            try:
                game = session.query(Game).filter(Game.id_==self.game_id).one()
                game.calculated = False
            except NoResultFound:
                raise NotFound(self, self.game_id, self.request)
            for player in game.players:
                self.request.form[str(player.id_)+'_played'] = "checked"
            for card in game.cards:
                self.request.form[str(card.player_id)+'_'+card.color] = "checked"
            for goal in game.goals:
                if goal.is_penalty == False:
                    self.request.form[str(goal.player_id)+'_goals'] = 1 + self.request.form.get(str(goal.player_id)+'_goals', 0)
                else:
                    self.request.form[str(goal.player_id)+'_penalty'] = 1 + self.request.form.get(str(goal.player_id)+'_penalty', 0)                    
            for assist in game.assists:
                self.request.form[str(assist.player_id)+'_assists'] = 1 + self.request.form.get(str(assist.player_id)+'_assists', 0)
                
            for save in game.saves:
                self.request.form[str(save.player_id)+'_saves'] = 1 + self.request.form.get(str(save.player_id)+'_saves', 0)
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

    def write_to_db(self, playing_players, yellow, second_yellow, red, goals, penalty, assists, saves):
        home_ids = [player.id_ for player in self.get_home_team()]
        home_score = 0
        visitor_score = 0
        session = named_scoped_session('footballchallenge')
        game = session.query(Game).filter(Game.id_ == self.game_id).one()
        if game.cards:
            for card in game.cards:
                session.delete(card)
        if game.goals:
            for goal in game.goals:
                session.delete(goal)
        if game.saves:
            for save in game.saves:
                session.delete(save)
        if game.assists:
            for assist in game.assists:
                session.delete(assist)
        if playing_players:
            players = []
            for player_id in playing_players:
                player = session.query(Player).filter(Player.id_ == player_id).one()
                players.append(player)
            game.players = players
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
                    if long(key) in home_ids:
                        home_score += value_int
                    else:
                        visitor_score += value_int
                except ValueError:
                    continue
                for count in range(0, value_int):
                    goal = Goal(key, game.id_, False)
                    session.add(goal)
        for key, value in penalty.items():
            if not value == '':
                try:
                    value_int = int(value)
                except ValueError:
                    continue
                for count in range(0, value_int):
                    goal = Goal(key, game.id_, True)
                    session.add(goal)
        for key, value in assists.items():
            if not value == '':
                try:
                    value_int = int(value)
                except ValueError:
                    continue
                for count in range(0, value_int):
                    assist = Assist(key, game.id_)
                    session.add(assist)

        game.score_nation1 = home_score
        game.score_nation2 = visitor_score
        for key, value in saves.items():
            if not value == '':
                try:
                    value_int = int(value)
                except ValueError:
                    continue
                for count in range(0, value_int):
                    save = Save(key, game.id_)
                    session.add(save)
        calculate_player_points(game)
        calculate_team_points(game)

    def write_cards(self, player_ids, color, game, session):
        for player_id in player_ids:
            card = Card(player_id, game.id_, color)
            session.add(card)
            
        