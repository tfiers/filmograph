"""
Provides access across modules to app settings.

Usage:

    from settings import settings
    settings['key']

This includes access to secret settings, which should be saved in a
gitignored file named 'secrets.json'. The file 'dummy_secrets.json'
shows how this file should be structured and which secret keys should
be defined. See 'settings/README.md'.

Running the current file on its own will update 'dummy_secrets.json' 
to reflect the current state of a real 'secrets.json' file.
(As a bonus, this also validates the json in the secrets file).
"""

import os
import json
from collections import OrderedDict

def absolute(path):
    """ Make the given path, relative to the current file, absolute.
    This means this file can also be executed from a working directory
    that is not the one this file resides in.
    """
    return os.path.join(os.path.dirname(__file__), path)

# Note: make sure SECRET_SETTINGS_FILE is gitignored.
SECRET_SETTINGS_FILE        = absolute('./secrets.json')
DUMMY_SECRET_SETTINGS_FILE  = absolute('./dummy_secrets.json')

settings = {}
with open(SECRET_SETTINGS_FILE) as f:
    # We use an OrderedDict to preserve the logical ordering 
    # ("key", "value", "description").
    secrets = json.load(f, object_pairs_hook=OrderedDict)
for secret in secrets:
    settings[secret['key']] = secret['value']

# --------------------------------------------------------------------

def generate_dummy_secrets():
    """ Based on the real 'secrets.json' file, creates a dummy 
    version of this file that shows how it should be structured and 
    which key-value pairs should be defined. The keys and the 
    descriptions are preserved, and the secret values are replaced by 
    a default instantiation of their original datatype ('0' for ints, 
    '{}' for dicts, etc.).
    """
    with open(SECRET_SETTINGS_FILE) as f:
        secrets = json.load(f, object_pairs_hook=OrderedDict)
    for secret in secrets:
        t = type(secret['value'])
        secret['value'] = t.__new__(t)
    with open(DUMMY_SECRET_SETTINGS_FILE, 'w') as f:
        json.dump(secrets, f, indent=4)

if __name__ == '__main__':
    generate_dummy_secrets()
