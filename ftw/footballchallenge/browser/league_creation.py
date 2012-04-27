from z3c.form import form, field, button
from zope import interface, schema
from ftw.footballchallenge import _
from z3c.saconfig import named_scoped_session
from ftw.footballchallenge.league import League
from Products.CMFCore.ActionInformation import Action
from Products.CMFCore.utils import getToolByName
from ftw.footballchallenge.interfaces import ILeague
import transaction


class CreateLeagueSchema(interface.Interface):


    name = schema.TextLine(title=_(u'label_name', default="Name"),
                                   required=True)
    event = schema.Choice(title=_('label_import_event', default="Event"),
                          vocabulary=u"EventFactory")


class CreateLeagueForm(form.Form):
    fields = field.Fields(CreateLeagueSchema)
    label = _(u'heading_create_league', 'Add League')
    ignoreContext = True
    
    def update(self):
        self.request['disable_plone.leftcolumn'] = True
        self.request['disable_plone.rightcolumn'] = True
        super(CreateLeagueForm, self).update()
        
    @button.buttonAndHandler(_(u'Import'))
    def handleImport(self, action):
        data, errors = self.extractData()
        if len(errors) == 0:
            name = data['name']
            event = data['event']
            session = named_scoped_session('footballchallenge')
            league = League(name, event)
            session.add(league)
            portal_actions = getToolByName(self.context, 'portal_actions')
            transaction.commit()
            league = session.query(League).filter(League.name==data['name']).all()[-1]
            cat = portal_actions['portal_tabs']
            urltool = getToolByName(self.context, 'portal_url')
            portal = urltool.getPortalObject()
            url_expr = 'string: '+portal.absolute_url()+'/ranking/'+str(league.id_)
            action = Action(league.id_, **{'title':name,'url_expr':url_expr, 'visible':True})
            cat[str(league.id_)] = action

            return self.request.RESPONSE.redirect(self.context.absolute_url())

    @button.buttonAndHandler(_(u'Cancel'))
    def handleCancel(self, action):
        return self.request.RESPONSE.redirect(self.context.absolute_url())
