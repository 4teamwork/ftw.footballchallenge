from z3c.form import form, field, button
from zope import interface, schema
from ftw.footballchallenge import _
from z3c.saconfig import named_scoped_session
from ftw.datepicker.widget import DatePickerFieldWidget
from ftw.footballchallenge.event import Event
import transaction


class CreateEventSchema(interface.Interface):

    name = schema.TextLine(title=_(u'label_name', default="Name"),
                                   required=True)
    date = schema.Date(title=_('label_date', default="Date"), required=True)


class CreateEventForm(form.Form):
    fields = field.Fields(CreateEventSchema)
    label = _(u'heading_create_event', 'Add Event')
    fields['date'].widgetFactory = DatePickerFieldWidget
    ignoreContext = True

    @button.buttonAndHandler(_(u'Import'))
    def handleImport(self, action):
        data, errors = self.extractData()
        if len(errors) == 0:
            name = data['name']
            date = data['date']
            session = named_scoped_session('footballchallenge')
            event = Event(name, date)
            session.add(event)
            transaction.commit()
            return self.request.RESPONSE.redirect(self.context.absolute_url())

    @button.buttonAndHandler(_(u'Cancel'))
    def handleCancel(self, action):
        return self.request.RESPONSE.redirect(self.context.absolute_url())
