"""
Filmograph web app.

Lets the user search for movies, TV shows and people, and shows them
a comprehensive graphical overview of the roles that people played in
different productions.
"""

from settings import settings
from flask import Flask, request, render_template
import themoviedb
import google_images

# Create the Flask WSGI application, our central webapp object.
app = Flask('filmograph')


@app.route('/')
def search():
    query = request.args.get('q')
    if query is None:
        screen_item_title = None
        cast_filmographies = None
    else:
        screen_item, cast_filmographies = \
                        themoviedb.get_cast_filmographies(query)
        # import json
        # with open('the_martian_cast_filmographies.json') as f:
        #     cast_filmographies = json.load(f)
        title_key = 'title' \
                if screen_item['media_type'] == 'movie' else 'name'
        screen_item_title = screen_item[title_key]
        cast_filmographies = cast_filmographies[:4]
        for cast_entry in cast_filmographies:
            cast_entry['filmography'] = cast_entry['filmography'][:4]
            cast_entry['role']['images_metadata'] = \
                google_images.get_search_results_metadata(
                                    screen_item_title,
                                    cast_entry['role']['name'],
                                    cast_entry['role']['character'])[:4]
            for credit in cast_entry['filmography']:
                credit_title_key = 'title' \
                        if credit['media_type'] == 'movie' else 'name'
                credit['images_metadata'] = \
                    google_images.get_search_results_metadata(
                                        credit[credit_title_key],
                                        cast_entry['role']['name'],
                                        credit['character'])[:4]
    return render_template('screen_item.html',
                           screen_item_title=screen_item_title,
                           cast_filmographies=cast_filmographies)


if __name__ == '__main__':
    # Run the application on a development server.
    app.run(host=settings['host'],
            debug=settings['debug'])
