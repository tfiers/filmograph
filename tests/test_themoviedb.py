from ..themoviedb import get_api_response, get_cast_filmographies

def test_get_api_response():
    config = get_api_response('/configuration')
    assert config['images']['base_url'] == 'http://image.tmdb.org/t/p/'
    assert config['images']['secure_base_url'] == 'https://image.tmdb.org/t/p/'
    r = get_api_response('/movie/popular', {'page': 2})
    assert r['page'] == 2

def test_get_cast_filmographies():
    cf = get_cast_filmographies('the martian')
    assert cf[0]['role']['character'] == 'Mark Watney'
    assert cf[0]['role']['name'] == 'Matt Damon'
    movies = [screen_item['title'] for screen_item in \
        cf[0]['filmography'] if screen_item['media_type'] == 'movie']
    assert 'Interstellar' in movies
    tv_shows = [screen_item['name'] for screen_item in \
        cf[0]['filmography'] if screen_item['media_type'] == 'tv']
    assert 'De Wereld Draait Door' in tv_shows
