# Instructions for Docker to run the webapp in a container.

# Parent Dockerfile:
#
#   http://github.com/docker-library/python/blob/master/2.7/onbuild/Dockerfile
#
#   It installs the packages found in 'requirements.txt' and
#   copies the contents of the directory of this Dockerfile
#   to the container (to /usr/src/app).
#
FROM python:2.7-onbuild

# Add the app directory to Python's module search path.
#
ENV PYTHONPATH $PYTHONPATH:/usr/src/app

CMD ["python", "webapp/webapp.py"]
