from z3c.form import form, field, button
from zope import interface, schema
from ftw.footballchallenge import _
from ftw.footballchallenge import Session
from ftw.footballchallenge.playerimport import import_team
from ftw.footballchallenge.event import get_events_as_term


class PlayerImportSchema(interface.Interface):

    urls = schema.List(title=_(u'label_import_urls', default="Urls"))
    event = schema.Choice(title=_('label_import_event', default="Event"),
                          vocabulary=get_events_as_term(Session()))

class PlayerImportForm(form.Form):
    fields = field.Fields(PlayerImportSchema)
    label = _(u'heading_import_players', 'Import Players')
    
    
    @button.buttonAndHandler(_(u'Import'))
    def handleImport(self, action):
        data, errors = self.extractData()
        if len(errors) == 0:
            urls = data['urls']
            event = data['event']
            session = Session()
            import_team(urls, session, event)
            return self.request.RESPONSE.redirect(self.context.absolute_url())
    
    
    @button.buttonAndHandler(_(u'Cancel'))
    def handleCancel(self, action):
        return self.request.RESPONSE.redirect(self.context.absolute_url())


