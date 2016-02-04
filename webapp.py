"""
Filmograph web app.

Lets the user search for movies, TV shows and people, and shows them
a comprehensive graphical overview of the roles that people played in 
different productions.
"""

from settings import settings
from flask import Flask, request, Response
from themoviedb import get_cast_filmographies_as_string

# Create the Flask WSGI application, our central webapp object.
app = Flask('filmograph')

@app.route('/')
def search():
    query = request.args.get('q')
    if query is None:
        resp = 'Hello there!'
    else:
        resp = get_cast_filmographies_as_string(query)
    return Response(resp, mimetype='text/plain')

if __name__ == '__main__':
    # Run the application on a development server.
    app.run(host=settings['host'],
            debug=settings['debug'])
