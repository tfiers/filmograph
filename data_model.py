from database import Base
from sqlalchemy import (Column, Integer, String, Enum, ForeignKey,
                        Boolean, BigInteger, Date, Float, DateTime)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class TimestampMixin(object):
    # This answer recommends 'server_default' instead of 'default':
    # http://stackoverflow.com/a/33532154/2611913
    # This "creates a default generator on the database side."
    # (http://docs.sqlalchemy.org/en/latest/core/metadata.html)
    # We create PostgreSQL 'TIMESTAMP WITH TIME ZONE' values.
    time_created = Column(DateTime(timezone=True),
                          server_default=func.now())
    time_updated = Column(DateTime(timezone=True),
                          onupdate=func.now())


class LastAPIRequestMixin(object):
    # When was the last time we sent a request specifically for this
    # object?
    last_dedicated_fetch   = Column(DateTime(timezone=True))
    # When was the last time some info on this object was
    # encountered when we sent a request for another object?
    last_incidental_update = Column(DateTime(timezone=True))


class ImageAssociatable(Base,
                        TimestampMixin):
    """ Any object that may have images associated with it. Eg:
    A Production, which has posters, a Person, which has photos, and a
    character Role, which has screencaps.
    """
    __tablename__ = 'image_associatable'
    # Using the built-in Python types 'id' and 'type' as property
    # names (and column names) has no effect outside of this class.
    # The effect in this class is that we can't use the 'id' and
    # 'type' functions in its scope anymore.
    id                   = Column(Integer, primary_key=True)
    type                 = Column(String)
    # For movies (and for non-cast roles), 'title' is a slightly more
    # appropriate column name. We choose for consistency by going with
    # 'name' though.
    name                 = Column(String)
    # 
    image_associations   = relationship('ImageAssociation',
                                        back_populates='associatable')
    # 
    # Set-up joined table inheritance.
    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'image_associatable'
    }


class Production(ImageAssociatable,
                 TimestampMixin,
                 LastAPIRequestMixin):
    """ Movies, TV shows, etc.
    """
    __tablename__ = 'production'

    # ---------------------- Core properties -------------------------
    #
    # Same remark on 'id' and 'type' as in 'ImageAssociatable'.
    id                   = Column(Integer,
                                  ForeignKey('image_associatable.id'),
                                  primary_key=True)
    __mapper_args__      = { 'polymorphic_identity': 'production' }
    # 
    type                 = Column(Enum('movie',
                                       'tv_show',
                                       'episode',
                                       'season',
                                       'movie_series',
                                       name='ProductionTypes'))
    #
    # Genealogy of Production instances by 'type'
    # (using the notation: child --> parent):
    #   'episode' --> 'season' --> 'tv_show'
    #   'movie' --> 'movie_series'
    # We index on the following column to find children in O(1) time.
    parent_id            = Column(Integer,
                                  ForeignKey('production.id'),
                                  index=True)
    # The 'remote_side' argument specifies this direction of the
    # relationship as the many-to-one direction (many children have
    # one parent).
    parent               = relationship('Production',
                                    back_populates='children',
                                    remote_side=[id])
    # (Default direction is one-to-many, so no extra directive
    # is needed).
    children             = relationship('Production',
                                    back_populates='parent',
                                    order_by='Production.sequence_no')
    #
    # 1-based. This is eg. '2' for the second episode of a season.
    sequence_no          = Column(Integer)
    #
    credits              = relationship('Role',
                                    back_populates='production')

    # ------------ Ancillary 'themoviedb.org' properties -------------
    #
    adult                = Column(Boolean)
    backdrop_path        = Column(String)
    budget               = Column(BigInteger)
    # We use JSONB instead of JSON, for faster indexing on properties
    # of these columns. (http://stackoverflow.com/a/22910602/2611913)
    episode_runtimes     = Column(JSONB)
    first_air_date       = Column(Date)
    genres               = Column(JSONB)
    homepage             = Column(String)
    tmdb_id              = Column(Integer)
    imdb_id              = Column(String)
    in_production        = Column(Boolean)
    languages            = Column(JSONB)
    last_air_date        = Column(Date)
    networks             = Column(JSONB)
    number_of_episodes   = Column(Integer)
    number_of_seasons    = Column(Integer)
    original_language    = Column(String)
    original_name        = Column(String)
    overview             = Column(String)
    popularity           = Column(Float)
    poster_path          = Column(String)
    production_companies = Column(JSONB)
    production_countries = Column(JSONB)
    release_date         = Column(Date)
    revenue              = Column(BigInteger)
    runtime              = Column(Integer)
    spoken_languages     = Column(JSONB)
    status               = Column(String)
    tagline              = Column(String)
    tmdb_tv_type         = Column(String)
    video                = Column(Boolean)
    vote_average         = Column(Float)
    vote_count           = Column(Integer)
    #
    alternative_names    = Column(JSONB)
    content_ratings      = Column(JSONB)
    keywords             = Column(JSONB)
    release_dates        = Column(JSONB)
    similar              = Column(JSONB)
    translations         = Column(JSONB)
    videos               = Column(JSONB)

    def __repr__(self):
        return u"<Production '{}'>".format(self.name)


class Role(ImageAssociatable,
           TimestampMixin,
           LastAPIRequestMixin):
    """ A character in a movie, the director of an episode, etc.
    """
    __tablename__ = 'role'

    # ---------------------- Core properties -------------------------
    #
    # Same remark on 'id' as in 'ImageAssociatable'.
    id                   = Column(Integer,
                                  ForeignKey('image_associatable.id'),
                                  primary_key=True)
    __mapper_args__      = { 'polymorphic_identity': 'role' }
    # The inherited column 'name' can be the name of the character
    # ('Harry Potter') or the title of the job ('Executive Producer').
    # 'department' is 'cast' for characters, or anything else for
    # crewmembers (eg: 'Editing', 'Camera', or 'Art'.)
    department           = Column(String)
    #
    # On the indexes: finding all roles of a person or of a production
    # is one of the primary functions of the application. Indexing
    # on these columns makes these lookups faster. Also note: indexes
    # are not automatically created on foreign keys.
    production_id        = Column(Integer,
                                  ForeignKey('production.id'),
                                  index=True)
    production           = relationship('Production',
                                         back_populates='credits')
    #
    person_id            = Column(Integer,
                                  ForeignKey('person.id'),
                                  index=True)
    person               = relationship('Person',
                                         back_populates='credits')

    # Only for TV
    tmdb_id              = Column(String)

    def __repr__(self):
        return u"<Role '{}' for '{}' in '{}'>".format(
                 self.name,
                 self.person.name,
                 self.production.name)


class Person(ImageAssociatable,
             TimestampMixin,
             LastAPIRequestMixin):
    """ A real-life person.
    """
    __tablename__ = 'person'

    # ---------------------- Core properties -------------------------
    #
    # Same remark on 'id' as in 'ImageAssociatable'.
    id                   = Column(Integer,
                                  ForeignKey('image_associatable.id'),
                                  primary_key=True)
    __mapper_args__      = { 'polymorphic_identity': 'person' }
    #
    credits              = relationship('Role',
                                         back_populates='person')

    # ------------ Ancillary 'themoviedb.org' properties -------------
    #
    adult                = Column(Boolean)
    # JSONB again, see 'Production'.
    also_known_as        = Column(JSONB)
    biography            = Column(String)
    birthday             = Column(Date)
    deathday             = Column(Date)
    homepage             = Column(String)
    tmdb_id              = Column(Integer)
    imdb_id              = Column(String)
    place_of_birth       = Column(String)
    popularity           = Column(Float)
    profile_path         = Column(String)
    #
    external_ids         = Column(JSONB)

    def __repr__(self):
        return u"<Person '{}'>".format(self.name)


class Image(Base,
            TimestampMixin):
    """ Points to an image file
    (or multiple versions of this same image.
    """
    __tablename__ = 'image'

    # Same remark on 'id' and 'type' as in 'ImageAssociatable'.
    id                   = Column(Integer, primary_key=True)
    type                 = Column(Enum('poster',
                                       'screencap',
                                       'photo',
                                       'tmdb_backdrop',
                                       name='ImageTypes'))
    original_url         = Column(String)
    #
    associations         = relationship('ImageAssociation',
                                         back_populates='image')
    #
    original_width       = Column(Integer)
    original_height      = Column(Integer)
    original_filetype    = Column(String)
    thumb_url            = Column(String)
    thumb_width          = Column(Integer)
    thumb_height         = Column(Integer)
    source_page_url      = Column(String)
    source_domain        = Column(String)
    Google_title         = Column(String)
    Google_description   = Column(String)
    # JSONB again, see 'Production'.
    other_data           = Column(JSONB)

    def __repr__(self):
        return u"<Image at {}>".format(self.original_url)


class ImageAssociation(Base,
                       TimestampMixin):
    """ Links a Production, a Role or a Person with an Image.
    """
    __tablename__ = 'image_association'

    # Same remark on 'id' as in 'ImageAssociatable'.
    id                   = Column(Integer, primary_key=True)
    #
    image_id             = Column(Integer,
                                  ForeignKey('image.id'),
                                  index=True)
    image                = relationship('Image',
                                  back_populates='associations')
    #
    associatable_id      = Column(Integer,
                                  ForeignKey('image_associatable.id'),
                                  index=True)
    associatable         = relationship('ImageAssociatable',
                                  back_populates='image_associations')
    # 
    # Position in the Google Image search results. 1-based.
    Google_position      = Column(Integer)
    upvotes              = Column(Integer)
    downvotes            = Column(Integer)

    # Maybe also, for associations with Roles:
    # whether we Google Image searched for:
    # <person name> + <production name>
    # or
    # <character name> + <production name>

    def __repr__(self):
        return u"<ImageAssociation between '{}' and '{}'>".format(
                 self.associatable.name, self.image.original_url)
