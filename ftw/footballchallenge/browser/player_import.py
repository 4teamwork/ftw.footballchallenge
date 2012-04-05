from z3c.form import form, field, button
from zope import interface, schema
from ftw.footballchallenge import _
from z3c.saconfig import named_scoped_session
from ftw.footballchallenge.playerimport import import_team


class PlayerImportSchema(interface.Interface):

    urls = schema.List(title=_(u'label_import_urls', default="Urls"),
                       value_type = schema.TextLine())
    event = schema.Choice(title=_('label_import_event', default="Event"),
                          source=u"EventFactory")


class PlayerImportForm(form.Form):
    fields = field.Fields(PlayerImportSchema)
    label = _(u'heading_import_players', 'Import Players')
    ignoreContext = True

    @button.buttonAndHandler(_(u'Import'))
    def handleImport(self, action):
        data, errors = self.extractData()
        if len(errors) == 0:
            urls = data['urls']
            event = data['event']
            session = named_scoped_session('footballchallenge')
            import_team(urls, session, event)
            return self.request.RESPONSE.redirect(self.context.absolute_url())

    @button.buttonAndHandler(_(u'Cancel'))
    def handleCancel(self, action):
        return self.request.RESPONSE.redirect(self.context.absolute_url())
