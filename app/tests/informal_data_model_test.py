"""
Does some tests on the data model.
Afterwards, the entire database transaction is rolled back.


SQLAlchemy technicalities

Based on:
http://docs.sqlalchemy.org/en/latest/orm/session_transaction.html?highlight=test#joining-a-session-into-an-external-transaction-such-as-for-test-suites

We bind a session to an already established transaction.
(Normally, a transaction ends when a session closes).

Step by step:

We create a Connection with an established Transaction.
We bind a Session to it.
Now we can work freely with the Session, including the ability to call
Session.commit(), where afterwards the entire database interaction is
rolled back.

"""

def test_data_models():

    # ------------- Setup --------------------------------------------

    from data.db_conn import init_db, engine
    from sqlalchemy.orm import sessionmaker
    from data.data_model import (Production, Person, Role, Image, 
                                 ImageLink)

    # Print generated SQL
    # See: http://docs.sqlalchemy.org/en/latest/core/engines.html#configuring-logging
    # import logging
    # logging.basicConfig()
    # logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    # Create new tables.
    init_db()

    # Connect to the database.
    connection = engine.connect()

    # Begin a non-ORM transaction.
    trans = connection.begin()

    # Create an individual (unscoped) session.
    # Bind it to the connection.
    session = sessionmaker(bind=connection)()



    # ------------- Tests --------------------------------------------

    martian = Production(name='The Martian')
    identity = Production(name='The Bourne Identity')
    matt = Person(name='Matt Damon')
    kate = Person(name='Kate Mara')

    astronaut = Role(name='Mark Watney',
                     production=martian,
                     person=matt)
    bourne    = Role(name='Jason Bourne',
                     production=identity,
                     person=matt)
    hacker    = Role(name='Beth Johanssen',
                     production=martian,
                     person=kate)

    session.add_all([astronaut, bourne, hacker])
    session.commit()

    session.add_all([
        Image(type='poster',
              links=[ImageLink(linked=martian)]),
        Image(type='poster',
              links=[ImageLink(linked=martian)]),
        Image(type='poster',
              links=[ImageLink(linked=identity)]),
        Image(type='tmdb_backdrop',
              links=[ImageLink(linked=martian)]),
        Image(type='photo',
              links=[ImageLink(linked=matt)]),
        Image(type='photo',
              links=[ImageLink(linked=matt),
                     ImageLink(linked=kate),]),
        Image(type='screencap',
              links=[ImageLink(linked=astronaut)]),
        Image(type='screencap',
              links=[ImageLink(linked=astronaut)]),
        Image(type='screencap',
              links=[ImageLink(linked=hacker)]),
        Image(type='screencap',
              links=[ImageLink(linked=astronaut),
                     ImageLink(linked=hacker),]),
        Image(type='screencap',
              links=[ImageLink(linked=astronaut),
                     ImageLink(linked=martian),]),
    ])
    session.commit()


    # ------------- Teardown -----------------------------------------

    session.close()

    # # Everything that happened with the session above is rolled back.
    trans.rollback()
    # trans.commit()

    # # Return connection to the Engine.
    connection.close()


if __name__ == '__main__':
    test_data_models()
