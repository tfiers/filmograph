from settings import settings
from loggers import logger
import requests

popularities = {}

def get_api_response(path, params={}):
    """ Queries v3 of themoviedb.org's API for the resource at the 
    given path, with the optional url params, and returns the result 
    as a dictionary. API reference: http://docs.themoviedb.apiary.io/
    The current rate limit is 40 requests every 10 seconds.
    """
    url = 'https://api.themoviedb.org/3'+path
    params.update({'api_key': settings['themoviedb_api_key']})
    logger.info('Requesting {}'.format(path))
    return requests.get(url, params=params).json()

def get_all_entries(path, start_page=1, end_page=None, 
                    entries_key='results'):
    """ Most API resources contain a list of entries (under the key 
    given by 'entries_key'). This method returns this list. If the API
    paginates the list, this method will, by default, query all pages 
    and return the resulting concatenated list. Alternatively, you may
    specify a particular starting and/or ending page.
    """
    # (Specifying a 'page' parameter when requesting a resource that 
    # is not paginated is harmless).
    response = get_api_response(path, {'page': start_page})
    results = response[entries_key]
    if end_page == None:
        end_page = response.get('total_pages', 1)
    for page in range(start_page+1, end_page+1):
        results += get_api_response(path, {'page': page})[entries_key]
    return results

def cache_popularities(movie_pages=5, tv_show_pages=2):
    """ Saves the popularity scores of the most popular movies and TV 
    shows in a dictionary in memory.
    """
    movies = get_all_entries('/movie/popular', end_page=movie_pages)
    tv_shows = get_all_entries('/tv/popular', end_page=tv_show_pages)
    for screen_item in movies + tv_shows:
        popularities[screen_item['id']] = screen_item['popularity']
    logger.info(('Cached the {} most popular movies and {} most '
            'popular TV shows.').format(len(movies), len(tv_shows)))

def get_cast_filmographies(query):
    """ Searches for the most popular movie or TV show with 'query' in 
    its name. Returns a dictionary with, for each actor of its top 
    billed cast, all movies and TV shows in which they appeared, sorted 
    by popularity, and annotated with their role in that production.
    """
    first_result = get_api_response('/search/multi', 
                    {'query': query})['results'][0]
    cast = get_api_response('/{media_type}/{id}/credits'
                                .format(**first_result))['cast']
    cast_filmographies = []
    if popularities == {}:
        cache_popularities()
    for role in cast[:7]:
        filmography = sorted(
                get_api_response('/person/{id}/combined_credits'
                                    .format(**role))['cast'], 
                key=lambda w: popularities.get(w["id"], 0),
                reverse=True)
        cast_filmographies.append((role, [w for w in filmography \
            if w["id"] != first_result["id"]],))
    return cast_filmographies

def get_cast_filmographies_as_string(query):
    """ Returns a string representation of the result of 
    get_cast_filmographies(query), where for each actor only the top 5 
    most popular movies and TV shows are shown.
    """
    cast_filmographies = get_cast_filmographies(query)
    s = ''
    width = 40
    for role, filmography in cast_filmographies:
        s += 4*u'\n' + u'{:>{}} -- {}\n\n'\
              .format(role['character'], width, role['name'])
        for w in filmography[:5]:
            if w['media_type'] == 'movie':
                s += u'{:>{}} in "{}"\n'\
                      .format(w['character'], width, w['title'])
            elif w['character'] != '':
                s += u'{:>{}} in "{}"\n'\
                      .format(w['character'], width, w['name'])
            else:
                s += (width-8)*u' ' + u'appeared in "{}"\n'\
                      .format(w['name'])
    return s

# Command line interface for this module.
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('query', help=('Search for a movie or a TV '
        'show of which you want to see the actors\' other roles.'))
    q = parser.parse_args().query
    print(get_cast_filmographies_as_string(q))
