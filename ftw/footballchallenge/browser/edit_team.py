from z3c.form import form, field, button
from zope import interface, schema
from ftw.footballchallenge import _
from ftw.footballchallenge import Session
from ftw.footballchallenge.player import get_player_term
from Products.CMFCore.utils import getToolByName
from ftw.footballchallenge.team import Team
from ftw.footballchallenge.player import Player
from ftw.footballchallenge.event import Event
from ftw.footballchallenge.Teams_Players import Teams_Players
from datetime import datetime

class EditTeamSchema(interface.Interface):
    
    name = schema.TextLine(title=_(u'label_name', default="Name"),required=True)
    
    keeper = schema.Choice(title=_(u'label_keeper', default="keeper"),
                           vocabulary=get_player_term(Session(), "keeper"))
    
    defender1 = schema.Choice(title=_(u'label_defender', default="defender"),
                              vocabulary=get_player_term(Session(), "defender"))
    defender2 = schema.Choice(title=_(u'label_defender', default="defender"),
                              vocabulary=get_player_term(Session(), "defender"))
    defender3 = schema.Choice(title=_(u'label_defender', default="defender"),
                              vocabulary=get_player_term(Session(), "defender"))
    
    midfield1 = schema.Choice(title=_(u'label_midfield', default="midfield"),
                              vocabulary=get_player_term(Session(), "midfield"))
    midfield2 = schema.Choice(title=_(u'label_midfield', default="midfield"),
                              vocabulary=get_player_term(Session(), "midfield"))
    
    midfield3 = schema.Choice(title=_(u'label_midfield', default="midfield"),
                              vocabulary=get_player_term(Session(), "midfield"))
    midfield4 = schema.Choice(title=_(u'label_midfield', default="midfield"),
                              vocabulary=get_player_term(Session(), "midfield"))
    midfield5 = schema.Choice(title=_(u'label_midfield', default="midfield"),
                              vocabulary=get_player_term(Session(), "midfield"))
    
    striker1 = schema.Choice(title=_(u'label_striker', default="striker"),
                             vocabulary=get_player_term(Session(), "striker"))
    striker2 = schema.Choice(title=_(u'label_striker', default="striker"),
                             vocabulary=get_player_term(Session(), "striker"))


#And now the Substitutes
    substitute_keeper = schema.Choice(title=_(u'label_keeper', default="keeper"),
                           vocabulary=get_player_term(Session(), "keeper"))

    substitute_defender1 = schema.Choice(title=_(u'label_defender', default="defender"),
                              vocabulary=get_player_term(Session(), "defender"))
    substitute_defender2 = schema.Choice(title=_(u'label_defender', default="defender"),
                              vocabulary=get_player_term(Session(), "defender"))
    substitute_defender3 = schema.Choice(title=_(u'label_defender', default="defender"),
                              vocabulary=get_player_term(Session(), "defender"))

    substitute_midfield1 = schema.Choice(title=_(u'label_midfield', default="midfield"),
                              vocabulary=get_player_term(Session(), "midfield"))
    substitute_midfield2 = schema.Choice(title=_(u'label_midfield', default="midfield"),
                              vocabulary=get_player_term(Session(), "midfield"))

    substitute_midfield3 = schema.Choice(title=_(u'label_midfield', default="midfield"),
                              vocabulary=get_player_term(Session(), "midfield"))
    substitute_midfield4 = schema.Choice(title=_(u'label_midfield', default="midfield"),
                              vocabulary=get_player_term(Session(), "midfield"))
    substitute_midfield5 = schema.Choice(title=_(u'label_midfield', default="midfield"),
                              vocabulary=get_player_term(Session(), "midfield"))

    substitute_striker1 = schema.Choice(title=_(u'label_striker', default="striker"),
                             vocabulary=get_player_term(Session(), "striker"))
    substitute_striker2 = schema.Choice(title=_(u'label_striker', default="striker"),
                             vocabulary=get_player_term(Session(), "striker"))



class EditTeamForm(form.Form):
    fields = field.Fields(EditTeamSchema)
    label = _(u'heading_edit_team', 'Edit Team')
  
    ignoreContext = True
    def update_widgets(self, context, request):
        membershiptool = getToolByName(self.context, 'portal_membership')
        userid = membershiptool.getAuthenticatedUser().userid
        session = Session()
        event_id = session.query(Event).filter(Event.lockdate > datetime.now()).one().id_
        team = session.query(Team).filter(Team.userid==userid and Team.event_id == event_id)
        keepers = session.query(Player).filter(team in Player.teams and Player.position=="keeper" and team.Players[Player.id_].is_starter==True).all()
        defenders = session.query(Player).filter(team in Player.teams and Player.position=="defender" and team.Players[Player.id_].is_starter==True).all()
        midfield = session.query(Player).filter(team in Player.teams and Player.position=="midfield" and team.Players[Player.id_].is_starter==True).all()
        strikers = session.query(Player).filter(team in Player.teams and Player.position=="striker" and team.Players[Player.id_].is_starter==True).all()

        subkeepers = session.query(Player).filter(team in Player.teams and Player.position=="keeper" and team.Players[Player.id_].is_starter==False).all()
        subdefenders = session.query(Player).filter(team in Player.teams and Player.position=="defender" and team.Players[Player.id_].is_starter==False).all()
        submidfield = session.query(Player).filter(team in Player.teams and Player.position=="midfield" and team.Players[Player.id_].is_starter==False).all()
        substrikers = session.query(Player).filter(team in Player.teams and Player.position=="striker" and team.Players[Player.id_].is_starter==False).all()

        request.form.widgets['keeper'] = keepers[0]
        for defender in defenders:
            request.form.widgets['defender'+str(defender.id_+1)]
        for midfielder in midfield:
            request.form.widgets['midfield'+str(midfielder.id_+1)]
        for striker in strikers:
            request.form.widgets['striker'+str(striker.id_+1)]

        request.form.widgets['substitute_keeper'] = subkeepers[0]
        for defender in subdefenders:
            request.form.widgets['substitute_defender'+str(defender.id_+1)]
        for midfielder in submidfield:
            request.form.widgets['substitute_midfield'+str(midfielder.id_+1)]
        for striker in substrikers:
            request.form.widgets['substitute_striker'+str(striker.id_+1)]
        
        super(EditTeamForm, self).update_widgets()

    @button.buttonAndHandler(_(u'Edit'))
    def handleEdit(self, action):
        data, errors = self.extractData()
        if len(errors) == 0:
            session = Session()
            membershiptool = getToolByName(self.context, 'portal_membership')
            userid = membershiptool.getAuthenticatedUser().userid
            if not session.query(Team).filter(Team.userid==userid).all():
                team = Team(data['name'], userid)
                session.add(team)
        else:
            team = session.query(Team).filter(Team.name==data['name'] and Team.userid==userid)
        session.delete(team.players[:])
        for k,v in data.items():
            if not k == 'name':
                player = session.query(Player).filter(Player.id_==v).one()
                team.players.append(Teams_Players(player, bool(not 'substitute' in k)))
        session.commit()
        return self.request.RESPONSE.redirect(self.context.absolute_url())
        
    @button.buttonAndHandler(_(u'Cancel'))
    def handleCancel(self, action):
        return self.request.RESPONSE.redirect(self.context.absolute_url())
