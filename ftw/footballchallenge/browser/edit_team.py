from z3c.form import form, field, button
from zope import interface, schema
from ftw.footballchallenge import _
from z3c.saconfig import named_scoped_session
from Products.CMFCore.utils import getToolByName
from ftw.footballchallenge.team import Team
from ftw.footballchallenge.player import Player
from ftw.footballchallenge.event import Event
from ftw.footballchallenge.Teams_Players import Teams_Players
from datetime import datetime
from zope.interface import implements
from ftw.footballchallenge.interfaces import IEditTeam
from zope.interface import invariant
from zope.interface import Invalid
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage


class EditTeamSchema(interface.Interface):
    """Schemadefinition of EditteamSchema"""
    name = schema.TextLine(title=_(u'label_name', default="Name"),
                           required=True)

    keeper = schema.Choice(title=_(u'label_keeper', default="keeper"),
                           vocabulary=u"KeeperFactory",
                           required=False)

    defender1 = schema.Choice(title=_(u'label_defender', default="defender"),
                              vocabulary=u"DefenderFactory",
                              required=False)
    defender2 = schema.Choice(title=_(u'label_defender', default="defender"),
                              vocabulary=u"DefenderFactory",
                              required=False)
    defender3 = schema.Choice(title=_(u'label_defender', default="defender"),
                              vocabulary=u"DefenderFactory",
                              required=False)

    midfield1 = schema.Choice(title=_(u'label_midfield', default="midfield"),
                              vocabulary=u"MidfieldFactory",
                              required=False)
    midfield2 = schema.Choice(title=_(u'label_midfield', default="midfield"),
                              vocabulary=u"MidfieldFactory",
                              required=False)

    midfield3 = schema.Choice(title=_(u'label_midfield', default="midfield"),
                              vocabulary=u"MidfieldFactory",
                              required=False)
    midfield4 = schema.Choice(title=_(u'label_midfield', default="midfield"),
                              vocabulary=u"MidfieldFactory",
                              required=False)
    midfield5 = schema.Choice(title=_(u'label_midfield', default="midfield"),
                              vocabulary=u"MidfieldFactory",
                              required=False)

    striker1 = schema.Choice(title=_(u'label_striker', default="striker"),
                             vocabulary=u"StrikerFactory",
                             required=False)
    striker2 = schema.Choice(title=_(u'label_striker', default="striker"),
                             vocabulary=u"StrikerFactory",
                             required=False)


#And now the Substitutes
    substitute_keeper = schema.Choice(title=_(u'label_keeper',
                                              default="keeper"),
                           vocabulary=u"KeeperFactory",
                           required=False)

    substitute_defender1 = schema.Choice(title=_(u'label_defender',
                                         default="defender"),
                              vocabulary=u"DefenderFactory",
                              required=False)
    substitute_defender2 = schema.Choice(title=_(u'label_defender',
                                         default="defender"),
                              vocabulary=u"DefenderFactory",
                              required=False)
    substitute_defender3 = schema.Choice(title=_(u'label_defender',
                                         default="defender"),
                              vocabulary=u"DefenderFactory",
                              required=False)

    substitute_midfield1 = schema.Choice(title=_(u'label_midfield',
                                         default="midfield"),
                              vocabulary=u"MidfieldFactory",
                              required=False)
    substitute_midfield2 = schema.Choice(title=_(u'label_midfield',
                                         default="midfield"),
                              vocabulary=u"MidfieldFactory",
                              required=False)

    substitute_midfield3 = schema.Choice(title=_(u'label_midfield',
                                         default="midfield"),
                              vocabulary=u"MidfieldFactory",
                              required=False)
    substitute_midfield4 = schema.Choice(title=_(u'label_midfield',
                                         default="midfield"),
                              vocabulary=u"MidfieldFactory",
                              required=False)
    substitute_midfield5 = schema.Choice(title=_(u'label_midfield',
                                         default="midfield"),
                              vocabulary=u"MidfieldFactory",
                              required=False)

    substitute_striker1 = schema.Choice(title=_(u'label_striker',
                                        default="striker"),
                             vocabulary=u"StrikerFactory",
                             required=False)
    substitute_striker2 = schema.Choice(title=_(u'label_striker',
                                        default="striker"),
                             vocabulary=u"StrikerFactory",
                             required=False)

    @invariant
    def player_only_once(data):
        """A Validator that checks if every Player is only used once"""
        keys = EditTeamSchema
        playerset = set([getattr(data, name) for name in keys.names()])
        playerlist = [getattr(data, name) for name in keys.names()]
        if len(playerset) == len(keys.names()):
            return True
        double_players = [x for x in playerset if playerlist.count(x) > 1]
        playernames = ''
        session = named_scoped_session('footballchallenge')
        if len(double_players) == 1:
            if not double_players[0]:
                return True
        for player_id in double_players:
            if player_id:
                playernames += session.query(Player).filter(
                    Player.id_ == player_id).one().name

        raise Invalid(_(u"You can't use the player ${players} multiple times",
                        mapping={'players': playernames}))


class EditTeamForm(form.Form):
    fields = field.Fields(EditTeamSchema)

    label = _(u'heading_edit_team', 'Edit Team')
    implements(IEditTeam)

    ignoreContext = True

    template = ViewPageTemplateFile("edit_team.pt")

    def __call__(self):
        session = named_scoped_session('footballchallenge')
        if not session.query(Event).filter(
                Event.deadline > datetime.now()).first():
            msg = _(u'label_not_edit',
                    default="The Event has started. You can't edit your Team "
                    "now.")
            IStatusMessage(self.request).addStatusMessage(
                msg, type='error')
            return self.request.response.redirect(self.context.absolute_url())
        else:
            return super(EditTeamForm, self).__call__()

    def updateWidgets(self):
        super(EditTeamForm, self).updateWidgets()
        membershiptool = getToolByName(self.context, 'portal_membership')
        userid = membershiptool.getAuthenticatedMember().getId()
        session = named_scoped_session('footballchallenge')
        event_id = session.query(Event).filter(
            Event.deadline > datetime.now()).first().id_

        team = session.query(Team).filter_by(user_id=userid).filter_by(
            event_id=event_id).first()

        if not team:
            return

        self.widgets['name'].value = team.name

        pos_counts = {
            'defender': 0,
            'midfield': 0,
            'striker': 0,
            'substitute_defender': 0,
            'substitute_midfield': 0,
            'substitute_striker': 0,
        }

        players = session.query(Teams_Players).filter_by(
            team_id=team.id_).all()
        for player in players:
            position = player.player.position
            if player.is_starter:
                widget_key = position
            else:
                widget_key = 'substitute_' + position
            if position != 'keeper':
                pos_counts[widget_key] += 1
                widget_key += str(pos_counts[widget_key])

            self.widgets[widget_key].value = [str(player.player_id)]

    @button.buttonAndHandler(_(u'Save'))
    def handleSave(self, action):
        """Handles the Edit action of the form"""
        data, errors = self.extractData()

        # If all validators are ok: proceed
        if len(errors) == 0:
            session = named_scoped_session('footballchallenge')
            event_id = session.query(Event).filter(
                Event.deadline > datetime.now()).one().id_

            membershiptool = getToolByName(self.context, 'portal_membership')
            userid = membershiptool.getAuthenticatedMember().getId()

            team = session.query(Team).filter_by(user_id=userid).filter_by(
                event_id=event_id).first()

            # Create team if it doesn't exist.
            if not team:
                team = Team(userid, event_id, name=data['name'])
                session.add(team)

            # First remove all players from team.
            session.query(Teams_Players).filter(
                Teams_Players.team_id == team.id_).delete()

            team.name = data['name']

            starter_nations = set()
            all_nations = set()
            for k, v in data.items():
                if not k == 'name' and v:
                    player = session.query(Player).filter(
                        Player.id_ == v).first()

                    is_starter = not k.startswith('substitute')
                    if is_starter:
                        starter_nations.add(player.nation_id)
                    all_nations.add(player.nation_id)

                    team.players.append(Teams_Players(
                        team.id_, player, is_starter))

            if (len(starter_nations) >= 6 and len(all_nations) >= 12 and
                    len(team.players) == 22):
                team.valid = True
            else:
                msg = _(u'label_not_valid',
                        default=u'Your Team is not valid and will not receive '
                        'any points')
                IStatusMessage(self.request).addStatusMessage(
                    msg, type='warning')
                team.valid = False

            msg = _(u'label_changes_saved',
                    default=u'Your changes are saved successfully')
            IStatusMessage(self.request).addStatusMessage(msg, type='info')

            return self.request.RESPONSE.redirect(
                self.context.absolute_url() + '/team_overview/' + str(team.id_)
            )

    @button.buttonAndHandler(_(u'Cancel'))
    def handleCancel(self, action):
        return self.request.RESPONSE.redirect(self.context.absolute_url())
