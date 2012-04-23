from z3c.form import form, field, button
from zope import interface, schema
from ftw.footballchallenge import _
from z3c.saconfig import named_scoped_session
from ftw.footballchallenge.team import Team
from ftw.footballchallenge.league import League
from zope.interface import implements
from zope.publisher.interfaces import IPublishTraverse


class AssignLeagueSchema(interface.Interface):

    teams = schema.List(title=_(u'label_teams',
                                     default=u"Teams"),
                          value_type=schema.Choice(
                          vocabulary=u"TeamFactory"))


class AssignLeagueForm(form.Form):
    fields = field.Fields(AssignLeagueSchema)
    label = _(u'heading_assign_teams', default=u'Assign Teams')
    ignoreContext = True

    implements(IPublishTraverse)

    def publishTraverse(self, request, name):
        self.league_id = name
        return self
    
    def updateWidgets(self):
        session = named_scoped_session('footballchallenge')
        league = session.query(League).filter(League.id_ == self.league_id).one()
        if league.teams:
            teams_ids = [team.id_ for team in league.teams]
            self.fields['teams'].field.default = teams_ids
        super(AssignLeagueForm, self).updateWidgets()

    @button.buttonAndHandler(_(u'Save'))
    def handleImport(self, action):
        data, errors = self.extractData()
        if len(errors) == 0:
            session = named_scoped_session('footballchallenge')
            league = session.query(League).filter(League.id_ == self.league_id).one()
            teams = []
            for team_id in data['teams']:
                team = session.query(Team).filter(Team.id_ == team_id).one()
                teams.append(team)
            league.teams = teams
            return self.request.RESPONSE.redirect(self.context.absolute_url())

    @button.buttonAndHandler(_(u'Cancel'))
    def handleCancel(self, action):
        return self.request.RESPONSE.redirect(self.context.absolute_url())
