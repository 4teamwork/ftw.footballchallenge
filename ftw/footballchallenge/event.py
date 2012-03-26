from sqlalchemy import Column, Integer, String, Date
from ftw.footballchallenge import Base


class Event(Base):
    __tablename__='events'


    id_ = Column('id', Integer, primary_key=True)
    name = Column(String(45))
    LockDate = Column(Date)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Event %s>' % self.name
