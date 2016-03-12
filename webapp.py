"""
Filmograph web app.

Lets the user search for movies, TV shows and people, and shows them
a comprehensive graphical overview of the roles that people played in
different productions.
"""

from settings import settings
from flask import Flask, request, render_template
from database import db_session
import themoviedb
import google_images


def get_cast_filmographies_with_images(query, num_cast_members=4,
                                       num_screen_items=4,
                                       num_images=4):
    """ Combines the cast filmographies of the screen item best match-
    ing the given query with images of the actors in their roles. Lim-
    its the number of cast members, screen items per cast member, and
    images per screen item to the supplied numbers. Returns two items:
    1. The name of the screen item best matching the given query;
    2. The cast filmographies with images, as described above.
    """
    if query is None:
        screen_item_title = None
        cast_filmographies = None
    else:
        screen_item, cast_filmographies = themoviedb.\
                                    get_cast_filmographies(query)
        # Fetch the title of the screen item.
        title_key = 'title' \
            if screen_item['media_type'] == 'movie'\
            else 'name'
        screen_item_title = screen_item[title_key]
        # Limit the number of cast members.
        cast_filmographies = cast_filmographies[:num_cast_members]
        # Add a limited number of images for each of the cast member's
        # roles. Also limit the number of roles per cast member.
        for cast_entry in cast_filmographies:
            cast_entry['filmography'] = \
                        cast_entry['filmography'][:num_screen_items]
            cast_entry['role']['images_metadata'] = google_images.\
                                get_search_results_metadata(
                                    screen_item_title,
                                    cast_entry['role']['name'],
                                    cast_entry['role']['character']
                                )[:num_images]
            for credit in cast_entry['filmography']:
                credit_title_key = 'title' \
                        if credit['media_type'] == 'movie' else 'name'
                credit['images_metadata'] = google_images.\
                                    get_search_results_metadata(
                                        credit[credit_title_key],
                                        cast_entry['role']['name'],
                                        credit['character']
                                    )[:num_images]
    return screen_item_title, cast_filmographies


# --------------------------------------------------------------------

# Create the Flask WSGI application, our central webapp object.
app = Flask('filmograph')


# Automatically remove database sessions at the end of each request
# or when the application shuts down.
@app.teardown_appcontext
def shutdown_sessions(exception=None):
    db_session.remove()


# Respond to requests at the root url.
@app.route('/')
def search():
    query = request.args.get('q')
    screen_item_title, cast_filmographies = \
        get_cast_filmographies_with_images(query)
    return render_template('screen_item.html',
                           screen_item_title=screen_item_title,
                           cast_filmographies=cast_filmographies)


if __name__ == '__main__':
    # Run the application on a development server.
    app.run(host=settings['host'],
            debug=settings['debug'])
