from sqlalchemy import Column, Integer, String
from ftw.footballchallenge import Base


class Nation(Base):
    __tablename__='nations'
    
    id_ = Column('id', Integer, primary_key=True)
    name = Column(String)
    
    
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Nation %s>' % self.name