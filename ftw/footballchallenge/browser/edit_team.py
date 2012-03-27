from z3c.form import form, field, button
from zope import interface, schema
from ftw.footballchallenge import _
from ftw.footballchallenge import Session


class EditTeamSchema(interface.Interface):
    
    name = schema.TextLine(title=_(u'label_name', default="Name"),required=True)
    
    starters = 