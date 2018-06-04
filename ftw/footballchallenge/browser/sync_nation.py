from z3c.form import form, field, button
from zope import interface, schema
from ftw.footballchallenge import _
from ftw.footballchallenge.sync_nation import sync_nation


class SyncNationFormSchema(interface.Interface):

    url = schema.TextLine(
        title=u'URL',
    )

    event = schema.Choice(
        title=_('label_import_event', default="Event"),
        source=u"EventFactory",
    )


class SyncNationForm(form.Form):
    fields = field.Fields(SyncNationFormSchema)
    label = u'Synchronize roster'
    ignoreContext = True

    @button.buttonAndHandler(_(u'Synchronize'))
    def handleSync(self, action):
        data, errors = self.extractData()
        if not errors == 0:
            url = data['url']
            event = data['event']
            sync_nation(url, event)
            return self.request.RESPONSE.redirect(self.context.absolute_url())

    @button.buttonAndHandler(_(u'Cancel'))
    def handleCancel(self, action):
        return self.request.RESPONSE.redirect(self.context.absolute_url())
