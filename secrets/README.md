### Purpose ###

This folder should contain a gitignored file called `secrets.json`, 
which provides settings that are not suitable for (public) version 
control, because they are either secret keys or settings particular 
to a developer or production machine.

`dummy_secrets.json` shows how this `secrets.json` file should be 
structured and which key-value pairs it should contain. The dummy 
file can be generated from a real `secrets.json` file by running 
`settings.py` in the root directory.

The secret settings are made available throughout the app through 
`settings.py`.
