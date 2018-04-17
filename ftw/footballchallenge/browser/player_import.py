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
            "https://www.transfermarkt.ch/agypten/startseite/verein/3672",
            "https://www.transfermarkt.ch/argentinien/startseite/verein/3437",
            "https://www.transfermarkt.ch/australien/startseite/verein/3433",
            "https://www.transfermarkt.ch/belgien/startseite/verein/3382",
            "https://www.transfermarkt.ch/brasilien/startseite/verein/3439",
            "https://www.transfermarkt.ch/costa-rica/startseite/verein/8497",
            "https://www.transfermarkt.ch/danemark/startseite/verein/3436",
            "https://www.transfermarkt.ch/deutschland/startseite/verein/3262",
            "https://www.transfermarkt.ch/england/startseite/verein/3299",
            "https://www.transfermarkt.ch/frankreich/startseite/verein/3377",
            "https://www.transfermarkt.ch/iran/startseite/verein/3582",
            "https://www.transfermarkt.ch/island/startseite/verein/3574",
            "https://www.transfermarkt.ch/japan/startseite/verein/3435",
            "https://www.transfermarkt.ch/kolumbien/startseite/verein/3816",
            "https://www.transfermarkt.ch/kroatien/startseite/verein/3556",
            "https://www.transfermarkt.ch/marokko/startseite/verein/3575",
            "https://www.transfermarkt.ch/mexiko/startseite/verein/6303",
            "https://www.transfermarkt.ch/nigeria/startseite/verein/3444",
            "https://www.transfermarkt.ch/panama/startseite/verein/3577",
            "https://www.transfermarkt.ch/peru/startseite/verein/3584",
            "https://www.transfermarkt.ch/polen/startseite/verein/3442",
            "https://www.transfermarkt.ch/portugal/startseite/verein/3300",
            "https://www.transfermarkt.ch/russland/startseite/verein/3448",
            "https://www.transfermarkt.ch/saudi-arabien/startseite/verein/3807",
            "https://www.transfermarkt.ch/schweden/startseite/verein/3557",
            "https://www.transfermarkt.ch/schweiz/startseite/verein/3384",
            "https://www.transfermarkt.ch/senegal/startseite/verein/3499",
            "https://www.transfermarkt.ch/serbien/startseite/verein/3438",
            "https://www.transfermarkt.ch/spanien/startseite/verein/3375",
            "https://www.transfermarkt.ch/sudkorea/startseite/verein/3589",
            "https://www.transfermarkt.ch/tunesien/startseite/verein/3670",
            "https://www.transfermarkt.ch/uruguay/startseite/verein/3449",
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
