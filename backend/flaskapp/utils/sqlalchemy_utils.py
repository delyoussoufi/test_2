import re

from sqlalchemy import TypeDecorator
from sqlalchemy.dialects.postgresql import TSVECTOR


def parse_to_ts_query_string(search_string: str):
    """
    Parse the search string to postgresql to_tsquery. Use '*' for fuzzy search like in the examples.

    :param search_string: A string to parse
    :return: the parsed string to be used in the match case.

    Examples:
         >>> parse_to_ts_query_string('Cahen* M & Margarete')
        Cahen:* | M & Margarete

        >>> parse_to_ts_query_string('Cahen M & Margar* L M')
        Cahen | M & Margar:* | L | M

        >>> parse_to_ts_query_string('Cahen M Margarete')
        Cahen | M | Margarete

        >>> parse_to_ts_query_string('Cahen Margarete')
        Cahen | Margarete

        >>> parse_to_ts_query_string('Cahen | Margarete')
        Cahen | Margarete
    """
    search_string = re.sub('\\s+<->\\s+', '<->', search_string)
    text_search = [re.sub('\\s+', ' ', ts.strip().replace('|', '')) for ts in re.split('&', search_string)]
    text_search = [' | '.join([f"{s.replace('*', ':*')}" for s in ts.split(' ')]) for ts in text_search]
    text_search = ' & '.join(text_search)
    return text_search


class TSVectorType(TypeDecorator):
    """
    .. note::

        This type is PostgreSQL specific and is not supported by other
        dialects.

    Provides additional functionality for SQLAlchemy PostgreSQL dialect's
    TSVECTOR_ type. This additional functionality includes:

    * Vector concatenation
    * regconfig constructor parameter which is applied to match function if no
      postgresql_regconfig parameter is given
    * Provides extensible base for extensions such as SQLAlchemy-Searchable_

    .. _TSVECTOR:
        http://docs.sqlalchemy.org/en/latest/dialects/postgresql.html#full-text-search

    .. _SQLAlchemy-Searchable:
        https://www.github.com/kvesteri/sqlalchemy-searchable

    ::

        from sqlalchemy_utils import TSVectorType


        class Article(Base):
            __tablename__ = 'user'
            id = sa.Column(sa.Integer, primary_key=True)
            name = sa.Column(sa.String(100))
            search_vector = sa.Column(TSVectorType)


        # Find all articles whose name matches 'finland'
        session.query(Article).filter(Article.search_vector.match('finland'))


    TSVectorType also supports vector concatenation.

    ::


        class Article(Base):
            __tablename__ = 'user'
            id = sa.Column(sa.Integer, primary_key=True)
            name = sa.Column(sa.String(100))
            name_vector = sa.Column(TSVectorType)
            content = sa.Column(sa.String)
            content_vector = sa.Column(TSVectorType)

        # Find all articles whose name or content matches 'finland'
        session.query(Article).filter(
            (Article.name_vector | Article.content_vector).match('finland')
        )

    You can configure TSVectorType to use a specific regconfig.
    ::

        class Article(Base):
            __tablename__ = 'user'
            id = sa.Column(sa.Integer, primary_key=True)
            name = sa.Column(sa.String(100))
            search_vector = sa.Column(
                TSVectorType(regconfig='pg_catalog.simple')
            )


    Now expression such as::


        Article.search_vector.match('finland')


    Would be equivalent to SQL::


        search_vector @@ to_tsquery('pg_catalog.simgle', 'finland')

    """
    impl = TSVECTOR
    cache_ok = True

    class comparator_factory(TSVECTOR.Comparator):
        def match(self, other, **kwargs):
            if 'postgresql_regconfig' not in kwargs:
                if 'regconfig' in self.type.options:
                    kwargs['postgresql_regconfig'] = (
                        self.type.options['regconfig']
                    )
            return TSVECTOR.Comparator.match(self, other, **kwargs)

        def __or__(self, other):
            return self.op('||')(other)

    def __init__(self, *args, **kwargs):
        """
        Initializes new TSVectorType

        :param *args: list of column names
        :param **kwargs: various other options for this TSVectorType
        """
        self.columns = args
        self.options = kwargs
        super(TSVectorType, self).__init__()
