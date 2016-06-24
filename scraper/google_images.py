from settings.loggers import logger
from requests import get
from bs4 import BeautifulSoup
from urlparse import urlparse, parse_qs
import json


def get_search_results_metadata(production_name, person_name, character_name):
    """ Searches Google Images for the given terms and returns a list
    of dictionaries containing metadata about each search result,
    including urls to the original image and to a thumbnail version.
    """
    # Clean up the search terms to compose the Google Images search url.
    production_name   =   production_name.strip().replace(' ', '+')
    person_name       =       person_name.strip().replace(' ', '+')
    character_name    =    character_name.strip().replace(' ', '+')
    query = u"{}+{}".format(production_name, person_name)
    url = u'https://www.google.com/search?tbm=isch&q={}'.format(query)
    # Pose as a Firefox browser. (Otherwise we get an older version of
    # the Google Search app, intended for non-javascript browsers, with
    # less relevant search results.)
    headers = {'User-Agent': ('Mozilla/5.0 (Windows NT 6.1; WOW64; '
                              'rv:34.0) Gecko/20100101 Firefox/34.0'),
               'Accept-Language': 'en'}
    # Download and parse the search results page.
    logger.info(u'Requesting Google Images search for {}'.format(query))
    r = get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    # See the appendix below for the HTML structure of the interesting
    # part of this page.
    # We search for all the img-tags within the div with id 'res':
    search_results_img_tags = soup.find('div', {'id': 'res'})\
                                  .find_all('img')
    search_results_metadata = []
    for img in search_results_img_tags:
        # We find interesting metadata in a json-dictionary located in
        # the content of the div-tag immediately after the img's 
        # parent (an a-tag). (This div has class 'rg_meta').
        metadata = json.loads(img.parent.find_next_sibling('div').text)
        # Create a dictionary with interesting metadata and add it to
        # the results.
        search_results_metadata.append({
            'thumb_url':         metadata['tu'],
            'thumb_width':       metadata['tw'],
            'thumb_height':      metadata['th'],
            'image_url':         metadata['ou'],
            'image_width':       metadata['ow'],
            'image_height':      metadata['oh'],
            'image_type':        metadata['ity'],
            'source_page_url':   metadata['ru'],
            'source_domain':     metadata['isu'],
            'title':             metadata['pt'],
            'description':       metadata['s'],
            # Other possibly interesting metadata:
            # 'cb', 'cl', 'cr', 'ct'
            # 'itg', 'sc'
            # (^what are those?)
            # 'id', 'rid'   (thumb id, doc id)
        })
    return search_results_metadata


# Appendix: HTML Structure of the part of the Google Images search
# results page in which we are interested (simplified):
#    <div id="res">
#        ...
#                      <div>
#                          .
#                          .
#                          <div>
#                              <a><img></a>
#                              <div class="rg_meta">"{..}"</div>
#                          </div>
#                          <div>
#                              <a><img></a>
#                              <div class="rg_meta">"{..}"</div>
#                          </div>
#                          .
#                          .
#                      </div>
#        ...
#    </div>
#
# Emmet shorthand:
#   div#res>div>div>div>div>div>div>div>div>div*20>a>img^+div.rg_meta


# Example div.rg_meta content (processed with json.loads):
# 
# {u'cb': 21,
#  u'cl': 9,
#  u'cr': 21,
#  u'ct': 6,
#  u'id': u'ebcXDoHn5dsLhM:',
#  u'isu': u'meatgrinder.co',
#  u'itg': False,
#  u'ity': u'jpg',
#  u'oh': 1200,
#  u'ou': u'https://meatgrinder.co/photos/oona-chaplin/full-oona-chaplin-quantum-of-solace-4c91bca59c4b158fbbc06c2cc2384609-large-262761.jpg',
#  u'ow': 800,
#  u'pt': u'Full Oona Chaplin Quantum Of Solace',
#  u'rid': u'-A2cJogE8TscFM',
#  u'ru': u'https://meatgrinder.co/full--quantum-of-solace-oona-chaplin-262761.html',
#  u's': u'',
#  u'sc': 1,
#  u'th': 275,
#  u'tu': u'https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcRBXJz3wULp5cA6kqOyn0LEJ5je54N4cNlZ2kW3Qwn0ljrjNn-3',
#  u'tw': 183}
