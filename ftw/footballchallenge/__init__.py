from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from zope.i18nmessageid import MessageFactory

_ = MessageFactory("ftw.footballchallenge")

Base = declarative_base()


engine = create_engine('mysql://localhost/footballchallenge')

Session = sessionmaker()
Session.configure(bind=engine)
