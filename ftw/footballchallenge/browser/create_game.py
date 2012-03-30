from z3c.form import form, field, button
from zope import interface, schema
from ftw.footballchallenge import _
from z3c.saconfig import named_scoped_session
from ftw.datepicker.widget import DatePickerFieldWidget
from ftw.footballchallenge.event import get_events_as_term
import transaction
from ftw.footballchallenge.nation import get_nations_term
from ftw.footballchallenge.player import get_player_term, get_keeper_term
from ftw.footballchallenge.goal import Goal
from ftw.footballchallenge.card import Card
from ftw.footballchallenge.game import Game
from ftw.footballchallenge.save import Save
from ftw.footballchallenge.teamstatistics import calculate_team_points
from ftw.footballchallenge.playerstatistics import calculate_player_points

class CreateGameSchema(interface.Interface):

    date = schema.Date(title=_('label_date', default="Date"),required=True)
    event = schema.Choice(title=_('label_import_event', default="Event"),
                          source=get_events_as_term)
    score_home = schema.Int(title=_('label_homescore', default="Home Score"), required=False)
    score_visitor = schema.Int(title=_('label_visitorscore', default="Visitor Score"), required=False)
    
    nation1 = schema.Choice(title=_('label_hometeam', default="Home Team"),
                            source=get_nations_term)
    nation2 = schema.Choice(title=_('label_visitorteam', default="Visitor Team"),
                            source=get_nations_term)
    yellow = schema.List(title=_('label_yellow', default="Yellow Cards"),
                           value_type=schema.Choice(
                           source=get_player_term))
    sec_yellow = schema.List(title=_('label_2yellow', default="Second Yellow Cards"),
                          value_type=schema.Choice(
                          source=get_player_term))
    red = schema.List(title=_('label_red', default="Red Cards"),
                        value_type=schema.Choice(
                        source=get_player_term))
    
    goals = schema.List(title=_('label_goal', default="Goals"),
                        value_type=schema.Choice(
                        source=get_player_term))
    
    saves = schema.List(title=_('label_save', default="Penalty save"),
                          value_type=schema.Choice(
                          source=get_keeper_term))

class CreateGameForm(form.Form):
    fields = field.Fields(CreateGameSchema)
    label = _(u'heading_create_event', 'Add Game')
    fields['date'].widgetFactory = DatePickerFieldWidget
    ignoreContext = True

    @button.buttonAndHandler(_(u'Import'))
    def handleImport(self, action):
        data, errors = self.extractData()
        if len(errors) == 0:
            session = named_scoped_session('footballchallenge')
            game = Game(int(data['nation1']), int(data['nation2']), data['date'], data['event'], data['score_home'], data['score_visitor'])
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
            transaction.commit()
            calculate_player_points(game = session.query(Game).all()[-1])
            calculate_team_points(game = session.query(Game).all()[-1])

            self.request.response.redirect(self.context.absolute_url())


    @button.buttonAndHandler(_(u'Cancel'))
    def handleCancel(self, action):
        return self.request.RESPONSE.redirect(self.context.absolute_url())
