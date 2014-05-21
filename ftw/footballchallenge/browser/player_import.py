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
          "http://www.transfermarkt.ch/algerien/startseite/verein/3614/saison_id/2013",
          "http://www.transfermarkt.ch/argentinien/startseite/verein/3437/saison_id/2013",
          "http://www.transfermarkt.ch/australien/startseite/verein/3433/saison_id/2013",
          "http://www.transfermarkt.ch/belgien/startseite/verein/3382/saison_id/2013",
          "http://www.transfermarkt.ch/bosnien-h-/startseite/verein/3446/saison_id/2013",
          "http://www.transfermarkt.ch/brasilien/startseite/verein/3439/saison_id/2013",
          "http://www.transfermarkt.ch/chile/startseite/verein/3700/saison_id/2013",
          "http://www.transfermarkt.ch/costa-rica/startseite/verein/8497/saison_id/2013",
          "http://www.transfermarkt.ch/deutschland/startseite/verein/3262/saison_id/2013",
          "http://www.transfermarkt.ch/ecuador/startseite/verein/5750/saison_id/2013",
          "http://www.transfermarkt.ch/elfenbeinkuste/startseite/verein/3591/saison_id/2013",
          "http://www.transfermarkt.ch/england/startseite/verein/3299/saison_id/2013",
          "http://www.transfermarkt.ch/frankreich/startseite/verein/3377/saison_id/2013",
          "http://www.transfermarkt.ch/ghana/startseite/verein/3441/saison_id/2013",
          "http://www.transfermarkt.ch/griechenland/startseite/verein/3378/saison_id/2013",
          "http://www.transfermarkt.ch/honduras/startseite/verein/3590/saison_id/2013",
          "http://www.transfermarkt.ch/iran/startseite/verein/3582/saison_id/2013",
          "http://www.transfermarkt.ch/italien/startseite/verein/3376/saison_id/2013",
          "http://www.transfermarkt.ch/japan/startseite/verein/3435/saison_id/2013",
          "http://www.transfermarkt.ch/kamerun/startseite/verein/3434/saison_id/2013",
          "http://www.transfermarkt.ch/kolumbien/startseite/verein/3816/saison_id/2013",
          "http://www.transfermarkt.ch/kroatien/startseite/verein/3556/saison_id/2013",
          "http://www.transfermarkt.ch/mexiko/startseite/verein/6303/saison_id/2013",
          "http://www.transfermarkt.ch/niederlande/startseite/verein/3379/saison_id/2013",
          "http://www.transfermarkt.ch/nigeria/startseite/verein/3444/saison_id/2013",
          "http://www.transfermarkt.ch/portugal/startseite/verein/3300/saison_id/2013",
          "http://www.transfermarkt.ch/russland/startseite/verein/3448/saison_id/2013",
          "http://www.transfermarkt.ch/schweiz/startseite/verein/3384/saison_id/2013",
          "http://www.transfermarkt.ch/spanien/startseite/verein/3375/saison_id/2013",
          "http://www.transfermarkt.ch/sudkorea/startseite/verein/3589/saison_id/2013",
          "http://www.transfermarkt.ch/uruguay/startseite/verein/3449/saison_id/2013",
          "http://www.transfermarkt.ch/usa/startseite/verein/3505/saison_id/2013",
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
