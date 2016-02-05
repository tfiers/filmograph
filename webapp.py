"""
Filmograph web app.

Lets the user search for movies, TV shows and people, and shows them
a comprehensive graphical overview of the roles that people played in 
different productions.
"""

from settings import settings
from flask import Flask, request, render_template
from themoviedb import get_cast_filmographies

# Create the Flask WSGI application, our central webapp object.
app = Flask('filmograph')

@app.route('/')
def search():
    query = request.args.get('q')
    if query == None:
        cast_filmographies = None
    else:
        cast_filmographies = get_cast_filmographies(query)
    return render_template('screen_item.html', 
        cast_filmographies=cast_filmographies)

if __name__ == '__main__':
    # Run the application on a development server.
    app.run(host=settings['host'],
            debug=settings['debug'])
