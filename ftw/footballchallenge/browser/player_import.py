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
            "http://www.transfermarkt.ch/deutschland/startseite/verein/3262",
            "http://www.transfermarkt.ch/spanien/startseite/verein/3375",
            "http://www.transfermarkt.ch/frankreich/startseite/verein/3377",
            "http://www.transfermarkt.ch/england/startseite/verein/3299",
            "http://www.transfermarkt.ch/belgien/startseite/verein/3382",
            "http://www.transfermarkt.ch/portugal/startseite/verein/3300",
            "http://www.transfermarkt.ch/kroatien/startseite/verein/3556",
            "http://www.transfermarkt.ch/italien/startseite/verein/3376",
            "http://www.transfermarkt.ch/turkei/startseite/verein/3381",
            "http://www.transfermarkt.ch/polen/startseite/verein/3442",
            "http://www.transfermarkt.ch/schweiz/startseite/verein/3384",
            "http://www.transfermarkt.ch/wales/startseite/verein/3864",
            "http://www.transfermarkt.ch/russland/startseite/verein/3448",
            "http://www.transfermarkt.ch/ukraine/startseite/verein/3699",
            "http://www.transfermarkt.ch/osterreich/startseite/verein/3383",
            "http://www.transfermarkt.ch/irland/startseite/verein/3509",
            "http://www.transfermarkt.ch/schweden/startseite/verein/3557",
            "http://www.transfermarkt.ch/slowakei/startseite/verein/3503",
            "http://www.transfermarkt.ch/tschechien/startseite/verein/3445",
            "http://www.transfermarkt.ch/rumanien/startseite/verein/3447",
            "http://www.transfermarkt.ch/albanien/startseite/verein/3561",
            "http://www.transfermarkt.ch/island/startseite/verein/3574",
            "http://www.transfermarkt.ch/nordirland/startseite/verein/5674",
            "http://www.transfermarkt.ch/ungarn/startseite/verein/3468",
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
