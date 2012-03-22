from sqlalchemy import Column, Integer, String
from ftw.footballchallenge import Base


class League(Base):
    __tablename__='leagues'
    
    id_ = Column('id', Integer, primary_key=True)
    name = Column(String)
    
    
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<League %s>' % self.name