from z3c.form import form, field, button
from zope import interface, schema
from ftw.footballchallenge import _
from ftw.footballchallenge import Session
from ftw.footballchallenge.league import League
from ftw.footballchallenge.event import get_events_as_term

class CreateLeagueSchema(interface.Interface):

    name = schema.TextLine(title=_(u'label_name', default="Name"),required=True)
    event = schema.Choice(title=_('label_import_event', default="Event"),
                          vocabulary=get_events_as_term(Session()))
    

class CreateLeagueForm(form.Form):
    fields = field.Fields(CreateLeagueSchema)
    label = _(u'heading_create_league', 'Add League')
    
    
    @button.buttonAndHandler(_(u'Import'))
    def handleImport(self, action):
        data, errors = self.extractData()
        if len(errors) == 0:
            name = data['name']
            event = data['event']
            session = Session()
            league = League(name, event)
            session.add(league)
            session.commit()
            return self.request.RESPONSE.redirect(self.context.absolute_url())
    
    
    @button.buttonAndHandler(_(u'Cancel'))
    def handleCancel(self, action):
        return self.request.RESPONSE.redirect(self.context.absolute_url())
