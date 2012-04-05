from z3c.form import form, field, button
from zope import interface, schema
from ftw.footballchallenge import _
from z3c.saconfig import named_scoped_session
from ftw.datepicker.widget import DatePickerFieldWidget
from ftw.footballchallenge.event import Event
import transaction
from ftw.footballchallenge.interfaces import IEvent

class CreateEventSchema(interface.Interface):

    name = schema.TextLine(title=_(u'label_name', default="Name"),
                                   required=True)
    date = schema.Date(title=_('label_date', default="Date"), required=True)


class CreateEventForm(form.Form):
    fields = field.Fields(CreateEventSchema)
    label = _(u'heading_create_event', 'Add Event')
    fields['date'].widgetFactory = DatePickerFieldWidget
    ignoreContext = True

    def updateWidgets(self):
        try:
            IEvent(self.context)
        except TypeError:
            pass
        if IEvent.providedBy(self.context):
            session = named_scoped_session("footballchallenge")
            event = session.query(Event).filter(Event.id_==self.context.id_).one()
            self.fields['name'].field.default = event.name
            self.fields['date'].field.default = event.LockDate
        super(CreateEventForm, self).updateWidgets()
    
    def update(self):
        self.request['disable_plone.leftcolumn'] = True
        self.request['disable_plone.rightcolumn'] = True
        super(CreateEventForm, self).update()

    @button.buttonAndHandler(_(u'Import'))
    def handleImport(self, action):
        data, errors = self.extractData()
        if len(errors) == 0:
            name = data['name']
            date = data['date']
            session = named_scoped_session('footballchallenge')
            
            if IEvent.providedBy(self.context):
                event = session.query(Event).filter(Event.id_==self.context.id_).one()
                event.name = name
                event.date = date
                transaction.commit()
            else:
                event = Event(name, date)
                session.add(event)
                transaction.commit()
            return self.request.RESPONSE.redirect(self.context.absolute_url())

    @button.buttonAndHandler(_(u'Cancel'))
    def handleCancel(self, action):
        return self.request.RESPONSE.redirect(self.context.absolute_url())
