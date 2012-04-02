from z3c.saconfig import named_scoped_session
from ftw.footballchallenge import Base


def create_sql_tables(event):
    """This function creates the SQL tables if they don't exist"""
    session = named_scoped_session('footballchallenge')
    Base.metadata.create_all(session.bind)
