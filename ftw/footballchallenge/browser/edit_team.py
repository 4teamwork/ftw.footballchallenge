from z3c.form import form, field, button, value
from zope import interface, schema
from ftw.footballchallenge import _
from z3c.saconfig import named_scoped_session
from zope.schema import vocabulary
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
from zope import component

class EditTeamSchema(interface.Interface):
    """Schemadefinition of EditteamSchema"""
    name = schema.TextLine(title=_(u'label_name', default="Name"),
                           required=True)

    keeper = schema.Choice(title=_(u'label_keeper', default="keeper"),
                           vocabulary=u"KeeperFactory")

    defender1 = schema.Choice(title=_(u'label_defender', default="defender"),
                              vocabulary=u"DefenderFactory")
    defender2 = schema.Choice(title=_(u'label_defender', default="defender"),
                              vocabulary=u"DefenderFactory")
    defender3 = schema.Choice(title=_(u'label_defender', default="defender"),
                              vocabulary=u"DefenderFactory")

    midfield1 = schema.Choice(title=_(u'label_midfield', default="midfield"),
                              vocabulary=u"MidfieldFactory")
    midfield2 = schema.Choice(title=_(u'label_midfield', default="midfield"),
                              vocabulary=u"MidfieldFactory")

    midfield3 = schema.Choice(title=_(u'label_midfield', default="midfield"),
                              vocabulary=u"MidfieldFactory")
    midfield4 = schema.Choice(title=_(u'label_midfield', default="midfield"),
                              vocabulary=u"MidfieldFactory")
    midfield5 = schema.Choice(title=_(u'label_midfield', default="midfield"),
                              vocabulary=u"MidfieldFactory")

    striker1 = schema.Choice(title=_(u'label_striker', default="striker"),
                             vocabulary=u"StrikerFactory")
    striker2 = schema.Choice(title=_(u'label_striker', default="striker"),
                             vocabulary=u"StrikerFactory")


#And now the Substitutes
    substitute_keeper = schema.Choice(title=_(u'label_keeper',
                                              default="keeper"),
                           vocabulary=u"KeeperFactory")

    substitute_defender1 = schema.Choice(title=_(u'label_defender',
                                         default="defender"),
                              vocabulary=u"DefenderFactory")
    substitute_defender2 = schema.Choice(title=_(u'label_defender',
                                         default="defender"),
                              vocabulary=u"DefenderFactory")
    substitute_defender3 = schema.Choice(title=_(u'label_defender',
                                         default="defender"),
                              vocabulary=u"DefenderFactory")

    substitute_midfield1 = schema.Choice(title=_(u'label_midfield',
                                         default="midfield"),
                              vocabulary=u"MidfieldFactory")
    substitute_midfield2 = schema.Choice(title=_(u'label_midfield',
                                         default="midfield"),
                              vocabulary=u"MidfieldFactory")

    substitute_midfield3 = schema.Choice(title=_(u'label_midfield',
                                         default="midfield"),
                              vocabulary=u"MidfieldFactory")
    substitute_midfield4 = schema.Choice(title=_(u'label_midfield',
                                         default="midfield"),
                              vocabulary=u"MidfieldFactory")
    substitute_midfield5 = schema.Choice(title=_(u'label_midfield',
                                         default="midfield"),
                              vocabulary=u"MidfieldFactory")

    substitute_striker1 = schema.Choice(title=_(u'label_striker',
                                        default="striker"),
                             vocabulary=u"StrikerFactory")
    substitute_striker2 = schema.Choice(title=_(u'label_striker',
                                        default="striker"),
                             vocabulary=u"StrikerFactory")

    @invariant
    def player_only_once(data):
        """A Validator that checks if every Player is only used once"""
        keys = EditTeamSchema
        if len(set([getattr(data, name) for name in keys.names()])) == \
        len(keys.names()):
            return True
        raise Invalid(_(u"You can't use a player multiple times"))


class EditTeamForm(form.Form):
    fields = field.Fields(EditTeamSchema)
    label = _(u'heading_edit_team', 'Edit Team')
    implements(IEditTeam)

    ignoreContext = True

    def updateWidgets(self):
        membershiptool = getToolByName(self.context, 'portal_membership')
        userid = membershiptool.getAuthenticatedMember().getId()
        session = named_scoped_session('footballchallenge')
        event_id = session.query(Event).filter(Event.LockDate > datetime.now()).one().id_
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
                self.request.form["keeper"] = starter.player.id_
        
        
        count = {'defender':1, 'midfield':1, 'striker':1}
        for substitute in substitutes:
            if not substitute.player.position=="keeper":
                self.fields["substitute_"+(substitute.player.position + str(count[substitute.player.position])).encode('utf-8')].field.default = substitute.player.id_
                count[substitute.player.position] += 1
            else:
                self.request.form["substitute_keeper"] = substitute.player.id_


        super(EditTeamForm, self).updateWidgets()
            
    @button.buttonAndHandler(_(u'Edit'))
    def handleEdit(self, action):
        """Handles the Edit action of the form"""
        data, errors = self.extractData()
        #If all validators are ok: proceed
        if len(errors) == 0:
            #get the session from z3c.sacofig
            session = named_scoped_session('footballchallenge')
            event_id = session.query(Event).filter(
                Event.LockDate > datetime.now()).one().id_
            #get the userid we need it to find the right team
            membershiptool = getToolByName(self.context, 'portal_membership')
            userid = membershiptool.getAuthenticatedMember().getId()
            if not session.query(Team).filter_by(user_id=userid).filter_by(event_id=event_id).all():
                #create the team if it doesn't exist.
                team = Team(data['name'], userid, event_id)
                session.add(team)                
            else:
                team = session.query(Team).filter_by(user_id=userid).filter_by(event_id=event_id).one()
            session.query(Teams_Players).filter(Teams_Players.team_id==\
            team.id_).delete()
            for k, v in data.items():
                if not k == 'name':
                    player = session.query(Player).filter(Player.id_==v).one()
                    #Create relationsship between Team and Player
                    team.players.append(Teams_Players(team.id_, player,
                                        bool(not 'substitute' in k)))
            transaction.commit()
            return self.request.RESPONSE.redirect(self.context.absolute_url())

    @button.buttonAndHandler(_(u'Cancel'))
    def handleCancel(self, action):
        return self.request.RESPONSE.redirect(self.context.absolute_url())


