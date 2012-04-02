from z3c.form import form, field, button
from zope import interface, schema
from ftw.footballchallenge import _
from z3c.saconfig import named_scoped_session
from ftw.footballchallenge.league import League
from ftw.footballchallenge.event import get_events_as_term
import transaction


class CreateLeagueSchema(interface.Interface):


    name = schema.TextLine(title=_(u'label_name', default="Name"),
                                   required=True)
    event = schema.Choice(title=_('label_import_event', default="Event"),
                          source=get_events_as_term)


class CreateLeagueForm(form.Form):
    fields = field.Fields(CreateLeagueSchema)
    label = _(u'heading_create_league', 'Add League')
    ignoreContext = True

    @button.buttonAndHandler(_(u'Import'))
    def handleImport(self, action):
        data, errors = self.extractData()
        if len(errors) == 0:
            name = data['name']
            event = data['event']
            session = named_scoped_session('footballchallenge')
            league = League(name, event)
            session.add(league)
            transaction.commit()
            return self.request.RESPONSE.redirect(self.context.absolute_url())

    @button.buttonAndHandler(_(u'Cancel'))
    def handleCancel(self, action):
        return self.request.RESPONSE.redirect(self.context.absolute_url())
