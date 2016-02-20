from loggers import logger
from requests import get
from bs4 import BeautifulSoup
from urlparse import urlparse, parse_qs
import json


def get_search_results_metadata(screen_item_name, person_name, character_name):
    """ Searches Google Images for the given terms and returns a list
    of dictionaries containing metadata about each search result,
    including urls to the original image and to a thumbnail version.
    """
    # Clean up the search terms to compose the Google Images search url.
    screen_item_name  =  screen_item_name.strip().replace(' ', '+')
    person_name       =       person_name.strip().replace(' ', '+')
    character_name    =    character_name.strip().replace(' ', '+')
    query = u"{}+{}".format(screen_item_name, person_name)
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
        # The href-attribute of the a-tag contains an url with
        # interesting data in its query-string.
        url_metadata = parse_qs(urlparse(img.parent['href']).query)
        # The rest of the metadata we save is found as a json-dictionary
        # located in the content of the div-tag immediately after the
        # a-tag (with class 'rg_meta').
        div_metadata = json.loads(img.parent.find_next_sibling('div').text)
        # Create a dictionary with interesting metadata and add it to
        # the results.
        search_results_metadata.append({
            'thumb_url':         div_metadata['tu'],
            'thumb_width':       div_metadata['tw'],
            'thumb_height':      div_metadata['th'],
            'image_url':         url_metadata['imgurl'][0],
            'image_width':       div_metadata['ow'],
            'image_height':      div_metadata['oh'],
            'image_type':        div_metadata['ity'],
            'source_page_url':   url_metadata['imgrefurl'][0],
            'source_domain':     div_metadata['isu'],
            'title':             div_metadata['pt'],
            'description':       div_metadata['s'],
            # Other possibly interesting metadata:
            # - url_metadata's 'tbnid' & 'docid'
            #       (== div_metadata's 'id' & 'rid')
            # - div_metadata's 'cb', 'cl', 'cr', 'ct' (what are those?)
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
#                              <a href=".."><img></a>
#                              <div class="rg_meta">"{..}"</div>
#                          </div>
#                          <div>
#                              <a href=".."><img></a>
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
