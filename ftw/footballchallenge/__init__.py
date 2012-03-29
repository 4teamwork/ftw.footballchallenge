from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from zope.i18nmessageid import MessageFactory
from z3c.saconfig import named_scoped_session

_ = MessageFactory("ftw.footballchallenge")

Base = declarative_base()


engine = create_engine('mysql://fbc:footballchallenge@localhost/footballchallenge')

Session = named_scoped_session('footballchallenge')
