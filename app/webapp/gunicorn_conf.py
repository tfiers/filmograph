from multiprocessing import cpu_count

bind      = '0.0.0.0:8000'
workers   = cpu_count() * 2 + 1

# Also set:
# access-logfile, error-logfile, access-logformat, error-logformat

# All possible settings:
# docs.gunicorn.org/en/stable/settings.html
