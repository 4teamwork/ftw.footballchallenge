from ftw.footballchallenge import Base
from plone.testing import Layer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from z3c.saconfig.zcml import engine, session
from zope.configuration import xmlconfig
from z3c.saconfig import named_scoped_session
from StringIO import StringIO
import z3c.saconfig
from z3c.saconfig.interfaces import IEngineFactory
from zope import component


class DatabaseLayer(Layer):

    def __init__(self, *args, **kwargs):
        Layer.__init__(self, *args, **kwargs)
        self._engine = None
        self._session = None

    def testSetUp(self):
        xmlconfig.XMLConfig('meta.zcml', z3c.saconfig)()
        self.disconnect()
        self.get_connection()

    def testTearDown(self):
        self.disconnect()

    def get_connection(self):
        if not self._engine:
            xmlconfig.xmlconfig(StringIO("""
               <configure xmlns="http://namespaces.zope.org/db">
                 <engine name="footballchallenge.db" url="sqlite:///:memory:"
                     />
              </configure>"""))
            Factory = component.getUtility(IEngineFactory, name="footballchallenge.db")
            self._engine = Factory()
            Base.metadata.bind = self._engine
            Base.metadata.create_all()
        return self._engine

    def disconnect(self):
        self.close_session()
        self._engine = None

    @property
    def session(self):
        if not self._session:
            xmlconfig.xmlconfig(StringIO("""
             <configure xmlns="http://namespaces.zope.org/db">
               <session name="footballchallenge" engine="footballchallenge.db" />
             </configure>"""))
            
            self._session = named_scoped_session("footballchallenge")

        return self._session

    def close_session(self):
        if not self._session:
            return False

        else:
            self.session.close()
            self._session = None
            return True

    def commit(self):
        self.session.commit()
        self.close_session()


DATABASE_LAYER = DatabaseLayer()