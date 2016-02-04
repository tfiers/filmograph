from settings import settings
import requests
import argparse

popularities = {}

def get_api_response(path, params={}):
    url = 'https://api.themoviedb.org/3'+path
    params.update({'api_key': settings['themoviedb_api_key']})
    return requests.get(url, params=params).json()

def get_all_entries(path, start_page=1, end_page=None, 
                    entries_key='results'):
    response = get_api_response(path, {'page': start_page})
    results = response[entries_key]
    if end_page == None:
        end_page = response.get('total_pages', 1)
    for page in range(start_page+1, end_page+1):
        results += get_api_response(path, {'page': page})[entries_key]
    return results

def cache_popularities():
    movies = get_all_entries('/movie/popular', end_page=5)
    tv_shows = get_all_entries('/tv/popular', end_page=2)
    for watchable in movies + tv_shows:
        popularities[watchable['id']] = watchable['popularity']
    print(('Cached the {} most popular movies and {} most popular '
           'TV shows.').format(len(movies), len(tv_shows)))

def get_cast_filmographies(query):
    first_result = get_api_response('/search/multi', 
                    {'query': query})['results'][0]
    cast = get_api_response(
            '/{media_type}/{id}/credits'.format(
                **first_result))['cast']
    cast_filmographies = []
    for role in cast[:7]:
        filmography = sorted(\
                get_api_response('/person/{id}/combined_credits'\
                    .format(**role))['cast'], 
                key=lambda w: popularities.get(w["id"], 0),
                reverse=True)
        cast_filmographies.append((role, [w for w in filmography \
            if w["id"] != first_result["id"]],))
    return cast_filmographies

def print_cast_filmographies(cast_filmographies):
    width = 40
    for role, filmography in cast_filmographies:
        print(u'\n\n\n\n{character:>{width}} -- {name}\n'.format(
            character=role['character'], width=width, name=role['name']))
        for w in filmography[:5]:
            if w['media_type'] == 'movie':
                print(u'{character:>{width}} in "{title}"'.format(
                    character=w['character'], width=width, title=w['title']))
            elif w['character'] != '':
                print(u'{character:>{width}} in "{name}"'.format(
                    character=w['character'], width=width, name=w['name']))
            else:
                print(u' '*(width-8)+'appeared in "{name:}"'.format(
                    name=w['name']))

def cli(query):
    if popularities == {}:
        cache_popularities()
    print_cast_filmographies(
        get_cast_filmographies(query))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('query', help=('Search for a movie or a TV '
        'show of which you want to see the actors\' other roles.'))
    cli(parser.parse_args().query)
