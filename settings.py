"""
Provides access accross modules to app settings.

Usage:

    from settings import settings
    settings['key']

This includes access to secret settings, which should be saved in the 
directory 'secrets', in a gitignored file named 'secrets.json'. The 
file 'dummy_secrets.json' shows which secret keys should be defined.

Running this file on its own will update 'dummy_secrets.json' to 
reflect the current state of the real 'secrets.json' file.
"""

import json

settings = {}
with open('secrets/secrets.json') as f:
    settings.update(json.load(f))

# -------------------------------------------------------------------

def generate_dummy_secrets():
    """ Based on the real 'secrets/secrets.json' file, creates a dummy 
    version of this file that shows which key-value pairs should be 
    defined. The keys are preserved and the secret values are replaced 
    by a default instantiation of their original datatype ('0' for 
    ints, '{}' for dicts, etc.).
    """
    with open('secrets/secrets.json') as f:
        secrets = json.load(f)
    for key in secrets:
        t = type(secrets[key])
        secrets[key] = t.__new__(t)
    with open('secrets/dummy_secrets.json', 'wb') as f:
        json.dump(secrets, f, indent=4)

if __name__ == '__main__':
    generate_dummy_secrets()
