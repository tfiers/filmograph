'''
Provides access accross modules to app settings.

Usage:

    from settings import settings
    settings['key']

This includes access to secret settings, which should be saved in the 
directory 'secrets', in a gitignored file called 'secret_settings.json'. 
The file 'dummy_secret_settings.json' shows which secret keys should be 
defined.

Running this file on its own will update 'dummy_secret_settings.json'
to reflect the current state of the real 'secret_settings.json' file.
'''

import json

settings = {}
with open('secrets/secret_settings.json') as f:
    settings.update(json.load(f))

# -------------------------------------------------------------------

def generate_dummy_secret_settings():
    '''
    Based on the real 'secrets/secret_settings.json' file, creates a 
    dummy version of this file that shows which key-value pairs should 
    be defined. The keys are preserved and the secret values are 
    replaced by a default instantiation of their original datatype 
    ('0' for ints, '{}' for dicts, etc.).
    '''
    with open('secrets/secret_settings.json') as f:
        secrets = json.load(f)
    for key in secrets:
        t = type(secrets[key])
        secrets[key] = t.__new__(t)
    with open('secrets/dummy_secret_settings.json', 'wb') as f:
        json.dump(secrets, f, indent=4)

if __name__ == '__main__':
    generate_dummy_secret_settings()
