from z3c.form import form, field, button
from zope import interface, schema
from ftw.footballchallenge import _
from z3c.saconfig import named_scoped_session
from ftw.datepicker.widget import DateTimePickerFieldWidget
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
from zope.publisher.interfaces import IPublishTraverse
from zope.interface import implements
import datetime
from ftw.footballchallenge.game import RoundVocabulary

class CreateGameSchema(interface.Interface):
    """defines which Fields we will schow in the create Form."""
    date = schema.Datetime(title=_('label_date', default="Date"), required=True)
    event = schema.Choice(title=_('label_import_event', default="Event"),
                          vocabulary=u"EventFactory")
    
    nation1 = schema.Choice(title=_('label_hometeam', default="Home Team"),
                            vocabulary=u"NationFactory",
                            required=False)
    nation2 = schema.Choice(title=_('label_visitorteam',
                                    default="Visitor Team"),
                            source=u"NationFactory",
                            required=False)


    nation1_dummy = schema.TextLine(title=_('label_nation1_dummy', default="Home Dummy"),required=False)
    nation2_dummy = schema.TextLine(title=_('label_nation2_dummy', default="Visitor Dummy"),required=False)
    
    round_ = schema.Choice(title=_(u'label_round', default='Round'),
                           vocabulary=RoundVocabulary,
                           required=True)

class CreateGameForm(form.Form):
    """Defines the Form and the behavior."""
    #this sets the Schema as Fields
    implements(IPublishTraverse)
    
    fields = field.Fields(CreateGameSchema)
    fields['date'].widgetFactory = DateTimePickerFieldWidget
    label = _(u'heading_create_game', 'Add Game')
    game_id = None
    # fields['date'].widgetFactory = DatePickerFieldWidget
    #The ignoreContext flag tells the Form not to try to get defaults
    #  from context, since we don't have a request this will fail
    ignoreContext = True

    def publishTraverse(self, request, name):
        self.game_id = name
        return self


    def updateWidgets(self):
        if self.game_id:
            session = named_scoped_session('footballchallenge')
            game = session.query(Game).filter(Game.id_ == self.game_id).one()
            self.fields['date'].field.default = datetime.date(game.date.year, game.date.month, game.date.day)
            self.fields['event'].field.default = game.events_id
            self.fields['nation1'].field.default = game.nation1_id
            self.fields['nation2'].field.default = game.nation2_id
            self.fields['nation1_dummy'].field.default = game.nation1_dummy
            self.fields['nation2_dummy'].field.default = game.nation2_dummy
            self.fields['round_'].field.default = game.round_
        super(CreateGameForm, self).updateWidgets()


    @button.buttonAndHandler(_(u'Save'))
    def handleSave(self, action):
        data, errors = self.extractData()
        if len(errors) == 0:
            nation1 = None
            nation2 = None
            if data['nation1']:
                nation1 = int(data['nation1'])
            if data['nation2']:
                nation2 = int(data['nation2'])
            session = named_scoped_session('footballchallenge')
            if not self.game_id:
                game = Game(data['date'], data['event'], data['round_'], data['nation1_dummy'],
                            data['nation2_dummy'], nation1, nation2)
                session.add(game)
            else:
                session = named_scoped_session('footballchallenge')
                game = session.query(Game).filter(Game.id_ == self.game_id).one()
                game.date = data['date']
                game.nation1_id = data['nation1']
                game.nation2_id = data['nation2']
                game.nation1_dummy = data['nation1_dummy']
                game.nation2_dummy = data['nation2_dummy']
                game.round_ = data['round_']
            #After creating a game we need to update our statstables

            self.request.response.redirect(self.context.absolute_url()+'/schedule')

    @button.buttonAndHandler(_(u'Cancel'))
    def handleCancel(self, action):
        return self.request.RESPONSE.redirect(self.context.absolute_url())
