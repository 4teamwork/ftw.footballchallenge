from z3c.form import form, field, button
from zope import interface, schema
from ftw.footballchallenge import _
from z3c.saconfig import named_scoped_session
from ftw.datepicker.widget import DatePickerFieldWidget
import transaction
# from ftw.footballchallenge.player import get_player_term, getKeeperTerm
from ftw.footballchallenge.goal import Goal
from ftw.footballchallenge.card import Card
from ftw.footballchallenge.game import Game
from ftw.footballchallenge.player import Player

from ftw.footballchallenge.save import Save
from ftw.footballchallenge.teamstatistics import calculate_team_points
from ftw.footballchallenge.playerstatistics import calculate_player_points
from ftw.footballchallenge.interfaces import IGame

class CreateGameSchema(interface.Interface):
    """defines which Fields we will schow in the create Form."""
    date = schema.Date(title=_('label_date', default="Date"), required=True)
    event = schema.Choice(title=_('label_import_event', default="Event"),
                          vocabulary=u"EventFactory")
    score_home = schema.Int(title=_('label_homescore', default="Home Score"),
                            required=False)
    score_visitor = schema.Int(title=_('label_visitorscore',
                                       default="Visitor Score"),
                               required=False)
    
    nation1 = schema.Choice(title=_('label_hometeam', default="Home Team"),
                            vocabulary=u"NationFactory")
    nation2 = schema.Choice(title=_('label_visitorteam',
                                    default="Visitor Team"),
                            source=u"NationFactory")
    yellow = schema.List(title=_('label_yellow', default="Yellow Cards"),
                           value_type=schema.Choice(
                           vocabulary=u"PlayerFactory"))
    sec_yellow = schema.List(title=_('label_2yellow',
                                     default="Second Yellow Cards"),
                          value_type=schema.Choice(
                          vocabulary=u"PlayerFactory"))
    red = schema.List(title=_('label_red', default="Red Cards"),
                        value_type=schema.Choice(
                        vocabulary=u"PlayerFactory"))
    
    goals = schema.List(title=_('label_goal', default="Goals"),
                        value_type=schema.Choice(
                        vocabulary=u"PlayerFactory"))
    
    saves = schema.List(title=_('label_save', default="Penalty save"),
                          value_type=schema.Choice(
                          vocabulary=u"KeeperFactory"))

    players_played = schema.List(title=_('label_players_played', default="Playing Players"),
                          value_type=schema.Choice(
                            vocabulary=u"PlayerFactory"))
class CreateGameForm(form.Form):
    """Defines the Form and the behavior."""
    #this sets the Schema as Fields
    fields = field.Fields(CreateGameSchema)
    fields['date'].widgetFactory = DatePickerFieldWidget
    label = _(u'heading_create_event', 'Add Game')
    # fields['date'].widgetFactory = DatePickerFieldWidget
    #The ignoreContext flag tells the Form not to try to get defaults
    #  from context, since we don't have a request this will fail
    ignoreContext = True


    # def updateWidgets(self):
    #     try:
    #         IGame(self.context)
    #     except TypeError:
    #         pass
    #     if IGame.providedBy(self.context):
    #         session = named_scoped_session('footballchallenge')
    #         game = session.query(Game.id_ == self.context.id_).one()
    #         

    @button.buttonAndHandler(_(u'Import'))
    def handleImport(self, action):
        data, errors = self.extractData()
        if len(errors) == 0:
            session = named_scoped_session('footballchallenge')
            game = Game(int(data['nation1']), int(data['nation2']),
                        data['date'], data['event'], data['score_home'],
                        data['score_visitor'])
            session.add(game)
            transaction.commit()
            game = session.query(Game).all()[-1]
            for goal in data['goals']:
                obj = Goal(goal, game.id_, False)
                session.add(obj)
            for card in data['yellow']:
                yellow = Card(goal, game.id_, 'yellow')
                session.add(yellow)
            for card in data['sec_yellow']:
                second_yellow = Card(goal, game.id_, 'second_yellow')
                session.add(second_yellow)
            for card in data['red']:
                red = Card(goal, game.id_, 'red')
                session.add(red)
            for save in data['saves']:
                obj = Save(save, game.id_)
                session.add(obj)
            for player in data['players_played']:
                obj = session.query(Player).filter(Player.id_==player).one()
                game.players.append(obj)
            transaction.commit()
            
            #After creating a game we need to update our statstables
            calculate_player_points(game = session.query(Game).all()[-1])
            calculate_team_points(game = session.query(Game).all()[-1])

            self.request.response.redirect(self.context.absolute_url())

    @button.buttonAndHandler(_(u'Cancel'))
    def handleCancel(self, action):
        return self.request.RESPONSE.redirect(self.context.absolute_url())
