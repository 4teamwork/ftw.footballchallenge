from z3c.form import form, field, button, group
from zope import interface, schema
from ftw.footballchallenge import _
from z3c.saconfig import named_scoped_session
from Products.CMFCore.utils import getToolByName
from ftw.footballchallenge.team import Team
from ftw.footballchallenge.player import Player
from ftw.footballchallenge.event import Event
from ftw.footballchallenge.Teams_Players import Teams_Players
from datetime import datetime
import transaction
from zope.interface import implements
from ftw.footballchallenge.interfaces import IEditTeam
from zope.interface import invariant
from zope.interface import Invalid
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
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

        raise Invalid(_(u"You can't use the player ${players} multiple times", mapping={'players':playernames}))


class EditTeamForm(form.Form):
    fields = field.Fields(EditTeamSchema)

    label = _(u'heading_edit_team', 'Edit Team')
    implements(IEditTeam)

    ignoreContext = True

    template = ViewPageTemplateFile("edit_team.pt")

    def __call__(self):
        session = named_scoped_session('footballchallenge')
        if not session.query(Event).filter(Event.deadline > datetime.now()).all():
            msg = _(u'label_not_edit', default="The Event has started. You can't edit your Team now.")
            IStatusMessage(self.request).addStatusMessage(
                msg, type='error')
            return self.request.response.redirect(self.context.absolute_url())
        else:
            return super(EditTeamForm, self).__call__()
            

    def updateWidgets(self):
        membershiptool = getToolByName(self.context, 'portal_membership')
        userid = membershiptool.getAuthenticatedMember().getId()
        session = named_scoped_session('footballchallenge')
        event_id = session.query(Event).filter(Event.deadline > datetime.now()).one().id_
        for field in self.fields.values():
            field.field.default = None
        if not len(session.query(Team).filter_by(user_id=userid).filter_by(event_id=event_id).all()):
            super(EditTeamForm, self).updateWidgets()
            return

        team = session.query(Team).filter_by(user_id=userid).filter_by(event_id=event_id).one()
        starters = session.query(Teams_Players).filter_by(team_id=team.id_).filter_by(is_starter=True).all()
        substitutes = session.query(Teams_Players).filter_by(team_id=team.id_).filter_by(is_starter=False).all()

        self.fields['name'].field.default = team.name
        count = {'defender':1, 'midfield':1, 'striker':1}    
        for starter in starters:
            if not starter.player.position=="keeper":
                self.fields[(starter.player.position + str(count[starter.player.position])).encode('utf-8')].field.default = starter.player.id_
                count[starter.player.position] += 1
            else:
                self.fields["keeper"].field.default = starter.player.id_
        
        
        count = {'defender':1, 'midfield':1, 'striker':1}
        for substitute in substitutes:
            if not substitute.player.position=="keeper":
                self.fields["substitute_"+(substitute.player.position + str(count[substitute.player.position])).encode('utf-8')].field.default = substitute.player.id_
                count[substitute.player.position] += 1
            else:
                self.fields["substitute_keeper"].field.default = substitute.player.id_
        super(EditTeamForm, self).updateWidgets()



        
    @button.buttonAndHandler(_(u'Save'))
    def handleSave(self, action):
        """Handles the Edit action of the form"""
        data, errors = self.extractData()
        #If all validators are ok: proceed
        if len(errors) == 0:
            #get the session from z3c.sacofig
            session = named_scoped_session('footballchallenge')
            event_id = session.query(Event).filter(
                Event.deadline > datetime.now()).one().id_
            #get the userid we need it to find the right team
            membershiptool = getToolByName(self.context, 'portal_membership')
            userid = membershiptool.getAuthenticatedMember().getId()
            if not session.query(Team).filter_by(user_id=userid).filter_by(event_id=event_id).all():
                #create the team if it doesn't exist.
                team = Team(userid, event_id, name=data['name'])
                session.add(team)                
            else:
                team = session.query(Team).filter_by(user_id=userid).filter_by(event_id=event_id).one()
            session.query(Teams_Players).filter(Teams_Players.team_id==\
            team.id_).delete()
            team.name = data['name']
            nations = []
            all_nations = []
            for k, v in data.items():
                if not k == 'name' and v:
                    player = session.query(Player).filter(Player.id_ == v).one()
                    #Create relationsship between Team and Player
                    if bool(not 'substitute' in k):
                        if not player.nation_id in nations:
                            nations.append(player.nation_id)
                        if not player.nation_id in all_nations:
                            all_nations.append(player.nation_id)
                    else:
                        if not player.nation_id in all_nations:
                            all_nations.append(player.nation_id)

                    team.players.append(Teams_Players(team.id_, player,
                                        bool(not 'substitute' in k)))

            if len(nations) >= 6 and len(all_nations) >=12 and len(team.players) == 22:
                team.valid = True
            else:
                msg = _(u'label_not_valid', default=u'Your Team is not valid and will not receive any points')
                IStatusMessage(self.request).addStatusMessage(
                    msg, type='warning')
                team.valid = False

            msg = _(u'label_changes_saved', default=u'Your changes are saved successfully')
            IStatusMessage(self.request).addStatusMessage(
                msg, type='info')

            return self.request.RESPONSE.redirect(self.context.absolute_url()+'/team_overview/' + str(team.id_))

    @button.buttonAndHandler(_(u'Cancel'))
    def handleCancel(self, action):
        return self.request.RESPONSE.redirect(self.context.absolute_url())

