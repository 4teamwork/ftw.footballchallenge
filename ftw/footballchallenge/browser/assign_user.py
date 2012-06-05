from z3c.form import form, field, button
from zope import interface, schema
from ftw.footballchallenge import _
from z3c.saconfig import named_scoped_session
from ftw.footballchallenge.team import Team
from ftw.footballchallenge.league import League
from zope.interface import implements
from zope.publisher.interfaces import IPublishTraverse
from Products.statusmessages.interfaces import IStatusMessage
from ftw.footballchallenge.event import Event
from datetime import date


class AssignUserSchema(interface.Interface):

    teams = schema.List(title=_(u'label_teams',
                                     default=u"Teams"),
                          value_type=schema.Choice(
                          vocabulary=u"TeamFactory"))


class AssignUserForm(form.Form):
    fields = field.Fields(AssignUserSchema)
    label = _(u'heading_assign_teams', default=u'Assign Teams')
    ignoreContext = True

    def publishTraverse(self, request, name):
        self.league_id = name
        return self
    
    def updateWidgets(self):
        session = named_scoped_session('footballchallenge')
        league = session.query(League).filter(League.id_ == self.league_id).one()
        if league.teams:
            user_ids = [team.user_id for team in league.teams]
            self.fields['teams'].field.default = user_ids
        super(AssignUserForm, self).updateWidgets()

    @button.buttonAndHandler(_(u'Save'))
    def handleImport(self, action):
        data, errors = self.extractData()
        if len(errors) == 0:
            session = named_scoped_session('footballchallenge')
            league = session.query(League).filter(League.id_ == self.league_id).one()
            teams = []
            event_id = session.query(Event).filter(Event.LockDate > date.today()).one().id_
            for user_id in data['teams']:
                if session.query(Team).filter(Team.user_id == user_id).all():
                    team = session.query(Team).filter(Team.user_id == user_id).one()
                else:
                    team = Team(user_id, event_id)
                    session.add(team)
                teams.append(team)
            league.teams = teams
            msg = _(u'label_teams_assign', default=u'Teams were assigned successfully.')
            IStatusMessage(self.request).addStatusMessage(
                msg, type='information')
            return self.request.RESPONSE.redirect(self.context.absolute_url() + '/assign_users/'+self.league_id)

    @button.buttonAndHandler(_(u'Cancel'))
    def handleCancel(self, action):
        return self.request.RESPONSE.redirect(self.context.absolute_url())
