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
          "http://www.transfermarkt.ch/de/spanien/startseite/nationalmannschaft_3375.html",
          "http://www.transfermarkt.ch/de/deutschland/startseite/nationalmannschaft_3262.html",
          "http://www.transfermarkt.ch/de/portugal/startseite/nationalmannschaft_3300.html",
          "http://www.transfermarkt.ch/de/brasilien/startseite/nationalmannschaft_3439.html",
          "http://www.transfermarkt.ch/de/kolumbien/startseite/nationalmannschaft_3816.html",
          "http://www.transfermarkt.ch/de/uruguay/startseite/nationalmannschaft_3449.html",
          "http://www.transfermarkt.ch/de/argentinien/startseite/nationalmannschaft_3437.html",
          "http://www.transfermarkt.ch/de/schweiz/startseite/nationalmannschaft_3384.html",
          "http://www.transfermarkt.ch/de/italien/startseite/nationalmannschaft_3376.html",
          "http://www.transfermarkt.ch/de/griechenland/startseite/nationalmannschaft_3378.html",
          "http://www.transfermarkt.ch/de/england/startseite/nationalmannschaft_3299.html",
          "http://www.transfermarkt.ch/de/belgien/startseite/nationalmannschaft_3382.html",
          "http://www.transfermarkt.ch/de/chile/startseite/nationalmannschaft_3700.html",
          "http://www.transfermarkt.ch/de/vereinigte-staaten/startseite/nationalmannschaft_3505.html",
          "http://www.transfermarkt.ch/de/niederlande/startseite/nationalmannschaft_3379.html",
          "http://www.transfermarkt.ch/de/frankreich/startseite/nationalmannschaft_3377.html",
          "http://www.transfermarkt.ch/de/russland/startseite/nationalmannschaft_3448.html",
          "http://www.transfermarkt.ch/de/mexiko/startseite/nationalmannschaft_6303.html",
          "http://www.transfermarkt.ch/de/kroatien/startseite/nationalmannschaft_3556.html",
          "http://www.transfermarkt.ch/de/elfenbeinkueste/startseite/nationalmannschaft_3591.html",
          "http://www.transfermarkt.ch/de/algerien/startseite/nationalmannschaft_3614.html",
          "http://www.transfermarkt.ch/de/bosnien-herzegowina/startseite/nationalmannschaft_3446.html",
          "http://www.transfermarkt.ch/de/ecuador/startseite/nationalmannschaft_5750.html",
          "http://www.transfermarkt.ch/de/honduras/startseite/nationalmannschaft_3590.html",
          "http://www.transfermarkt.ch/de/costa-rica/startseite/nationalmannschaft_8497.html",
          "http://www.transfermarkt.ch/de/iran/startseite/nationalmannschaft_3582.html",
          "http://www.transfermarkt.ch/de/ghana/startseite/nationalmannschaft_3441.html",
          "http://www.transfermarkt.ch/de/nigeria/startseite/nationalmannschaft_3444.html",
          "http://www.transfermarkt.ch/de/japan/startseite/nationalmannschaft_3435.html",
          "http://www.transfermarkt.ch/de/kamerun/startseite/nationalmannschaft_3434.html",
          "http://www.transfermarkt.ch/de/suedkorea/startseite/nationalmannschaft_3589.html",
          "http://www.transfermarkt.ch/de/australien/startseite/nationalmannschaft_3433.html"
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
