from database import Base
from sqlalchemy import (Column, Integer, String, Enum, ForeignKey,
                        Boolean, BigInteger, Date, Float, DateTime)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

class Production(Base):
    """ Movies, TV shows, et cetera. """

    __tablename__ = 'productions'

    # --- Core properties ---
    # 
    # Using the built-in types 'id' and 'type' as property names (and
    # column names) has no effect outside of this file. The effect is
    # that we can't use the 'id' and 'type' functions in this file
    # anymore.
    id = Column(Integer, primary_key=True)
    title = Column(String)
    type = Column(Enum('movie',
                       'tv_show',
                       'episode',
                       'season',
                       'movie_series',
                       name='ProductionTypes'))
    # The parent for an 'episode' is a 'season', a 'tv_show' for a 
    # 'season', and a 'movie_series' for a 'movie'.
    parent_id = Column(Integer, ForeignKey('productions.id'))
    # This is eg. '2' for the second episode of a season. 1-based.
    sequence_no = Column(Integer)
    children = relationship('Production', back_populates='parent',
                            order_by='Production.sequence_no')
    last_dedicated_fetch    = Column(DateTime)
    last_incidental_update  = Column(DateTime)


    # --- Ancillary 'themoviedb.org' properties ---
    # 
    adult                   = Column(Boolean)
    backdrop_path           = Column(String)
    budget                  = Column(BigInteger)
    # We use JSONB instead of JSON, for indexing on these values.
    # See http://stackoverflow.com/a/22910602/2611913
    episode_runtimes        = Column(JSONB)
    first_air_date          = Column(Date)
    genres                  = Column(JSONB)
    homepage                = Column(String)
    tmdb_id                 = Column(Integer)
    imdb_id                 = Column(String)
    in_production           = Column(Boolean)
    languages               = Column(JSONB)
    last_air_date           = Column(Date)
    networks                = Column(JSONB)
    number_of_episodes      = Column(Integer)
    number_of_seasons       = Column(Integer)
    original_language       = Column(String)
    original_title          = Column(String)
    overview                = Column(String)
    popularity              = Column(Float)
    poster_path             = Column(String)
    production_companies    = Column(JSONB)
    production_countries    = Column(JSONB)
    release_date            = Column(Date)
    revenue                 = Column(BigInteger)
    runtime                 = Column(Integer)
    spoken_languages        = Column(JSONB)
    status                  = Column(String)
    tagline                 = Column(String)
    tmdb_tv_type            = Column(String)
    video                   = Column(Boolean)
    vote_average            = Column(Float)
    vote_count              = Column(Integer)

    alternative_titles      = Column(JSONB)
    content_ratings         = Column(JSONB)
    keywords                = Column(JSONB)
    release_dates           = Column(JSONB)
    similar                 = Column(JSONB)
    translations            = Column(JSONB)
    videos                  = Column(JSONB)


    def __repr__(self):
        return u"<Production '{}'>".format(self.title)






# class User(Base):
#     __tablename__ = 'users'

#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     fullname = Column(String)
#     password = Column(String)

#     def __repr__(self):
#         return "<User(name='{}', fullname='{}', password='{}'>"\
#                 .format(self.name, self.fullname, self.password)

# class Address(Base):
#     __tablename__ = 'addresses'

#     id = Column(Integer, primary_key=True)
#     email_address = Column(String, nullable=False)
#     user_id = Column(Integer, ForeignKey('users.id'))

#     user = relationship("User", back_populates='addresses')

#     def __repr__(self):
#         return "<Address(email_address='{}'>"\
#                 .format(self.email_address)

# User.addresses = relationship(
#     "Address", order_by=Address.id, back_populates="user")