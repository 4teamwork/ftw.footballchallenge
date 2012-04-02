from z3c.form import form, field, button
from zope import interface, schema
from ftw.footballchallenge import _
from z3c.saconfig import named_scoped_session
from ftw.footballchallenge.player import get_keeper_term, get_defender_term
from ftw.footballchallenge.player import get_midfield_term, get_striker_term
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


class EditTeamSchema(interface.Interface):
    """Schemadefinition of EditteamSchema"""
    name = schema.TextLine(title=_(u'label_name', default="Name"),
                           required=True)

    keeper = schema.Choice(title=_(u'label_keeper', default="keeper"),
                           source=get_keeper_term)

    defender1 = schema.Choice(title=_(u'label_defender', default="defender"),
                              source=get_defender_term)
    defender2 = schema.Choice(title=_(u'label_defender', default="defender"),
                              source=get_defender_term)
    defender3 = schema.Choice(title=_(u'label_defender', default="defender"),
                              source=get_defender_term)

    midfield1 = schema.Choice(title=_(u'label_midfield', default="midfield"),
                              source=get_midfield_term)
    midfield2 = schema.Choice(title=_(u'label_midfield', default="midfield"),
                              source=get_midfield_term)

    midfield3 = schema.Choice(title=_(u'label_midfield', default="midfield"),
                              source=get_midfield_term)
    midfield4 = schema.Choice(title=_(u'label_midfield', default="midfield"),
                              source=get_midfield_term)
    midfield5 = schema.Choice(title=_(u'label_midfield', default="midfield"),
                              source=get_midfield_term)

    striker1 = schema.Choice(title=_(u'label_striker', default="striker"),
                             source=get_striker_term)
    striker2 = schema.Choice(title=_(u'label_striker', default="striker"),
                             source=get_striker_term)


#And now the Substitutes
    substitute_keeper = schema.Choice(title=_(u'label_keeper',
                                              default="keeper"),
                           source=get_keeper_term)

    substitute_defender1 = schema.Choice(title=_(u'label_defender',
                                         default="defender"),
                              source=get_defender_term)
    substitute_defender2 = schema.Choice(title=_(u'label_defender',
                                         default="defender"),
                              source=get_defender_term)
    substitute_defender3 = schema.Choice(title=_(u'label_defender',
                                         default="defender"),
                              source=get_defender_term)

    substitute_midfield1 = schema.Choice(title=_(u'label_midfield',
                                         default="midfield"),
                              source=get_midfield_term)
    substitute_midfield2 = schema.Choice(title=_(u'label_midfield',
                                         default="midfield"),
                              source=get_midfield_term)

    substitute_midfield3 = schema.Choice(title=_(u'label_midfield',
                                         default="midfield"),
                              source=get_midfield_term)
    substitute_midfield4 = schema.Choice(title=_(u'label_midfield',
                                         default="midfield"),
                              source=get_midfield_term)
    substitute_midfield5 = schema.Choice(title=_(u'label_midfield',
                                         default="midfield"),
                              source=get_midfield_term)

    substitute_striker1 = schema.Choice(title=_(u'label_striker',
                                        default="striker"),
                             source=get_striker_term)
    substitute_striker2 = schema.Choice(title=_(u'label_striker',
                                        default="striker"),
                             source=get_striker_term)

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

    # def update_widgets(self, context, request):
    #     membershiptool = getToolByName(self.context, 'portal_membership')
    #     userid = membershiptool.getAuthenticatedUser().userid
    #     session = named_scoped_session('footballchallenge')
    #     event_id = session.query(Event).filter(Event.lockdate > datetime.now()).one().id_
    #     team = session.query(Team).filter(Team.userid==userid and Team.event_id == event_id)
    #     keepers = session.query(Player).filter(team in Player.teams and Player.position=="keeper" and team.Players[Player.id_].is_starter==True).all()
    #     defenders = session.query(Player).filter(team in Player.teams and Player.position=="defender" and team.Players[Player.id_].is_starter==True).all()
    #     midfield = session.query(Player).filter(team in Player.teams and Player.position=="midfield" and team.Players[Player.id_].is_starter==True).all()
    #     strikers = session.query(Player).filter(team in Player.teams and Player.position=="striker" and team.Players[Player.id_].is_starter==True).all()
    # 
    #     subkeepers = session.query(Player).filter(team in Player.teams and Player.position=="keeper" and team.Players[Player.id_].is_starter==False).all()
    #     subdefenders = session.query(Player).filter(team in Player.teams and Player.position=="defender" and team.Players[Player.id_].is_starter==False).all()
    #     submidfield = session.query(Player).filter(team in Player.teams and Player.position=="midfield" and team.Players[Player.id_].is_starter==False).all()
    #     substrikers = session.query(Player).filter(team in Player.teams and Player.position=="striker" and team.Players[Player.id_].is_starter==False).all()
    # 
    #     request.form.widgets['keeper'] = keepers[0]
    #     for defender in defenders:
    #         request.form.widgets['defender'+str(defender.id_+1)]
    #     for midfielder in midfield:
    #         request.form.widgets['midfield'+str(midfielder.id_+1)]
    #     for striker in strikers:
    #         request.form.widgets['striker'+str(striker.id_+1)]
    # 
    #     request.form.widgets['substitute_keeper'] = subkeepers[0]
    #     for defender in subdefenders:
    #         request.form.widgets['substitute_defender'+str(defender.id_+1)]
    #     for midfielder in submidfield:
    #         request.form.widgets['substitute_midfield'+str(midfielder.id_+1)]
    #     for striker in substrikers:
    #         request.form.widgets['substitute_striker'+str(striker.id_+1)]
    # 
    #     super(EditTeamForm, self).update_widgets()
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
            if not session.query(Team).filter(Team.user_id==userid).all():
                #create the team if it doesn't exist.
                team = Team(data['name'], userid, event_id)
                session.add(team)
            else:
                team = session.query(Team).filter(Team.name==data['name'] and\
                Team.userid==userid and Team.event_id == event_id)
            session.query(Teams_Players).filter(Teams_Players.team_id==\
            team.id_).delete()
            for k, v in data.items():
                if not k == 'name':
                    player = session.query(Player).filter(Player.id_==v).one()
                    #Create relationsship between Team and Player
                    team.players.append(Teams_Players(player,
                                        bool(not 'substitute' in k)))
            transaction.commit()
            return self.request.RESPONSE.redirect(self.context.absolute_url())

    @button.buttonAndHandler(_(u'Cancel'))
    def handleCancel(self, action):
        return self.request.RESPONSE.redirect(self.context.absolute_url())
