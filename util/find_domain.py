from requests import get

url = 'https://domainr.p.mashape.com/v2/status'
with open('domainr_mashape_key.txt') as f:
    params = { 'mashape-key': f.read() }


def dotcom_default(domain):
    if '.' not in domain:
        domain += '.com'
    return domain


def check(domain):
    params.update({'domain': domain})
    response = get(url, params=params).json()
    if response['status'][0]['summary'] == 'inactive':
        return 'ok'
    else:
        return '/'

# Some particles:
# vi, vis, viz, vy, vys, vyz
# mov, mo, movie
# film, screen, vid, vide, video
# fa, face, faces

# Available:
# moviefacer
# tvfacer
# filmfacer
# filmofacer
# filmoface
# filmofaces 
# filmershot
# filmoshot
# filmoshots
# filmopics
# filmopic <<
# filmostills
# filmknow
# filmfamiliar <<
# filmnear
# filmeven
# filmostill
# filmoshow
# filmosee
# 
# actorsee
# actorsea

# http://sentiwordnet.isti.cnr.it/

# a b c d e f g h i j k l m n o p q r s t u v w x y z

# Hip hoi!
# filmopic is overal nog vrij: .com, fb, yt, tw, gh, ig, ...
# Geldt ook allemaal voor filmopick.
# (Geldt niet voor filmpic, filmpick, filmepic)
# (filmpics.com bestaat, biedt film-afbeeldingen aan.)



# --------------- Ancillaries ----------------------------------------


def test_dotcom_default():
    assert dotcom_default('google')     == 'google.com'
    assert dotcom_default('google.com') == 'google.com'
    assert dotcom_default('google.net') == 'google.net'


def test_check():
    assert check('facebook.com') == '/'
    assert check('xwquieoj.com') == 'ok'


def cli():
    import argparse
    parser = argparse.ArgumentParser(description=\
        'Checks whether the given domain name is still available.')
    parser.add_argument('domain')
    domain = dotcom_default(parser.parse_args().domain)
    print('{}: {}'.format(domain, check(domain)))


def repl():
    while True:
        domain = dotcom_default(raw_input('> '))
        print(check(domain))


if __name__ == '__main__':
    # cli()
    repl()
