from z3c.form import form, field, button
from zope import interface, schema
from ftw.footballchallenge import _
from ftw.footballchallenge import Session
from ftw.datepicker.widget import DatePickerFieldWidget
from ftw.footballchallenge.event import Event


class CreateEventSchema(interface.Interface):

    name = schema.TextLine(title=_(u'label_name', default="Name"),required=True)
    date = schema.Date(title=_('label_date', default="Date"),required=True)
    form.widget(date=DatePickerFieldWidget)

class CreateEventForm(form.Form):
    fields = field.Fields(CreateEventSchema)
    label = _(u'heading_create_event', 'Add Event')
    
    
    @button.buttonAndHandler(_(u'Import'))
    def handleImport(self, action):
        data, errors = self.extractData()
        if len(errors) == 0:
            name = data['name']
            date = data['date']
            session = Session()
            event = Event(name, date)
            session.add(event)
            session.commit()
            return self.request.RESPONSE.redirect(self.context.absolute_url())
    
    
    @button.buttonAndHandler(_(u'Cancel'))
    def handleCancel(self, action):
        return self.request.RESPONSE.redirect(self.context.absolute_url())
