from z3c.form import form, field, button
from zope import interface, schema
from ftw.footballchallenge import _
from z3c.saconfig import named_scoped_session
from ftw.footballchallenge.playerimport import import_team


class PlayerImportSchema(interface.Interface):

    urls = schema.List(
        title=_(u'label_import_urls', default="Urls"),
        value_type=schema.TextLine(),
        default=[
            'http://www.transfermarkt.ch/de/daenemark/startseite/nationalmannschaft_3436.html',
            'http://www.transfermarkt.ch/de/deutschland/startseite/nationalmannschaft_3262.html',
            'http://www.transfermarkt.ch/de/england/startseite/nationalmannschaft_3299.html',
            'http://www.transfermarkt.ch/de/frankreich/startseite/nationalmannschaft_3377.html',
            'http://www.transfermarkt.ch/de/griechenland/startseite/nationalmannschaft_3378.html',
            'http://www.transfermarkt.ch/de/irland/startseite/nationalmannschaft_3509.html',
            'http://www.transfermarkt.ch/de/italien/startseite/nationalmannschaft_3376.html',
            'http://www.transfermarkt.ch/de/kroatien/startseite/nationalmannschaft_3556.html',
            'http://www.transfermarkt.ch/de/niederlande/startseite/nationalmannschaft_3379.html',
            'http://www.transfermarkt.ch/de/polen/startseite/nationalmannschaft_3442.html',
            'http://www.transfermarkt.ch/de/portugal/startseite/nationalmannschaft_3300.html',
            'http://www.transfermarkt.ch/de/russland/startseite/nationalmannschaft_3448.html',
            'http://www.transfermarkt.ch/de/schweden/startseite/nationalmannschaft_3557.html',
            'http://www.transfermarkt.ch/de/spanien/startseite/nationalmannschaft_3375.html',
            'http://www.transfermarkt.ch/de/tschechien/startseite/nationalmannschaft_3445.html',
            'http://www.transfermarkt.ch/de/ukraine/startseite/nationalmannschaft_3699.html',
        ],
    )
    event = schema.Choice(
        title=_('label_import_event', default="Event"),
        source=u"EventFactory",
    )


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
