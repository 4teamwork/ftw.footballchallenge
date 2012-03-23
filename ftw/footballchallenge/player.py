from sqlalchemy import Column, Integer, String
from ftw.footballchallenge import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref


class Player(Base):
    __tablename__='players'


    id_ = Column('id', Integer, primary_key=True)
    name = Column(String(128))
    position = Column(String(45))
    
    nation_id = Column(Integer, ForeignKey('nations.id'), nullable=False)

    nation = relationship("Nation", backref=backref('players', order_by=id_))

    def __init__(self, name, position, nation_id):
        self.name = name
        self.position = position
        self.nation_id = nation_id

    def __repr__(self):
         return '<Player %s>' % self.name
