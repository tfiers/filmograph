"""
Provides a handle to the database and a method to initialise a new 
database.

Usage:

To initialise the database:

    from data.db_conn import init_db
    init_db()


To insert entries:

    # Get existing handle or create new handle to the database.
    from data.db_conn import db_session
    from data.data_models import Person
    matt = Person(name='Matt Damon')
    db_session.add(matt)
    db_session.commit()
    # Close the handle to the database.
    db_session.remove()


To make queries:

    from data.data_models import Person
    Person.query.all()
    Person.query.filter(Person.name == 'Matt Damon').first()


This code is heavily based on the 'Declarative SQLAlchemy pattern' in 
the flask documentation:
http://flask.pocoo.org/docs/0.10/patterns/sqlalchemy/#declarative

"""

from settings import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Connect to the database at the url specified in the settings.
# Specify explicitly that all strings going in and coming out of the 
# database should be of the Python `unicode` type.
engine = create_engine(settings['database_url'], convert_unicode=True)

# Create the actual handle to the database.
# See http://docs.sqlalchemy.org/en/rel_1_0/orm/session_basics.html#session-faq-whentocreate
# and http://docs.sqlalchemy.org/en/rel_1_0/orm/contextual.html
db_session = scoped_session(sessionmaker(bind=engine,
                                         autocommit=False,
                                         autoflush=False))
# To make an unscoped session instance, use:
# session = sessionmaker(bind=engine)()

# Create the base class for classes mapped to database tables using 
# SQLAlchemy's ORM.
Base = declarative_base()

# Allow Django-like query syntax, eg.:
# `Person.query. ...` instead of `session.query(Person). ...`.
Base.query = db_session.query_property()


def init_db():
    """ Issue `CREATE TABLE` statements for classes that don't have an
    associated table in the database yet.
    """
    import data_model
    Base.metadata.create_all(engine)
