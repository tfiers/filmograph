from settings import settings
from loggers import logger
import requests
from collections import OrderedDict

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
    # Convert the json to an ordered dictionary, preserving the 
    # insertion order of key-value pairs in the original json.
    return (requests.get(url, params=params)
                    .json(object_pairs_hook=OrderedDict))

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
    its name and returns a list with, for each actor of the movie or 
    the TV show's top billed cast, the role that they played in it, 
    and all other roles they played in other movies and TV shows, 
    sorted by popularity of these movies and shows.
    """
    first_result = get_api_response('/search/multi', 
                    {'query': query})['results'][0]
    cast = get_api_response('/{media_type}/{id}/credits'
                                .format(**first_result))['cast']
    cast_filmographies = []
    if popularities == {}:
        cache_popularities(20, 10)
    for role in cast[:7]:
        filmography = get_api_response('/person/{id}/combined_credits'
                                        .format(**role) )['cast']
        # Annotate each screen item with its popularity.
        for screen_item in filmography:
            screen_item['popularity'] = \
                popularities.get(screen_item["id"], 0)
        # Sort on popularity, from hight to low.
        filmography = sorted(filmography, key=lambda screen_item: \
            screen_item["popularity"], reverse=True)
        # Don't include the queried movie in the filmography.
        filmography = filter(lambda screen_item: \
            screen_item["id"] != first_result["id"], filmography)
        # Add the new cast entry.
        cast_filmographies.append({'role': role, 
                                   'filmography': filmography })

    return cast_filmographies

def get_cast_filmographies_as_string(query):
    """ Returns a string representation of the result of 
    get_cast_filmographies(query), where for each actor only the top 5 
    most popular movies and TV shows are shown.
    """
    cast_filmographies = get_cast_filmographies(query)
    s = ''
    width = 40
    for cast_entry in cast_filmographies:
        s += 4*u'\n' + u'{:>{}} -- {}\n\n'.format(
            cast_entry['role']['character'], 
            width, 
            cast_entry['role']['name'])
        for screen_item in cast_entry['filmography'][:5]:
            if screen_item['media_type'] == 'movie':
                s += u'{:>{}} in "{}"\n'.format(
                    screen_item['character'], 
                    width, 
                    screen_item['title'])
            elif screen_item['character'] != '':
                s += u'{:>{}} in "{}"\n'.format(
                    screen_item['character'], 
                    width, 
                    screen_item['name'])
            else:
                s += (width-8)*u' ' + u'appeared in "{}"\n'.format(
                    screen_item['name'])
    return s

# Command line interface for this module.
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('query', help=('Search for a movie or a TV '
        'show of which you want to see the actors\' other roles.'))
    q = parser.parse_args().query
    print(get_cast_filmographies_as_string(q))
