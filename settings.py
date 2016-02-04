"""
Provides access across modules to app settings.

Usage:

    from settings import settings
    settings['key']

This includes access to secret settings, which should be saved in the 
directory 'secrets', in a gitignored file named 'secrets.json'. The 
file 'dummy_secrets.json' shows how this file should be structured and
which secret keys should be defined. See 'secrets/README.md'.

Running this file on its own will update 'dummy_secrets.json' to 
reflect the current state of the real 'secrets.json' file.
"""

import json
from collections import OrderedDict

settings = {}
with open('secrets/secrets.json') as f:
    # We use an OrderedDict to preserve the logical ordering 
    # ("key", "value", "description").
    secrets = json.load(f, object_pairs_hook=OrderedDict)
for secret in secrets:
    settings[secret['key']] = secret['value']

# --------------------------------------------------------------------

def generate_dummy_secrets():
    """ Based on the real 'secrets/secrets.json' file, creates a dummy 
    version of this file that shows how it should be structured and 
    which key-value pairs should be defined. The keys and the 
    descriptions are preserved, and the secret values are replaced by 
    a default instantiation of their original datatype ('0' for ints, 
    '{}' for dicts, etc.).
    """
    with open('secrets/secrets.json') as f:
        secrets = json.load(f, object_pairs_hook=OrderedDict)
    for secret in secrets:
        t = type(secret['value'])
        secret['value'] = t.__new__(t)
    with open('secrets/dummy_secrets.json', 'w') as f:
        json.dump(secrets, f, indent=4)

if __name__ == '__main__':
    generate_dummy_secrets()
