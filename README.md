# Django Soundcloud Feed

![logo](http://i.imgur.com/rduXHbq.png)

A django app for pulling in content from soundcloud and storing data locally.

## Requirements

This uses the following third party libraries:

* filebrowser: https://github.com/sehmaschine/django-filebrowser/
* soundcloud python library: https://github.com/soundcloud/soundcloud-python

## Installation

- Add `soundcloudfeed` to your `INSTALLED_APPS`
- Include soundcloud `urls.py`
- Run syncdb to create the tables
- Set your `SOUNDCLOUD_ACCESS_TOKEN` in `settings.py`
- Run management command `sync_soundcloud` to pull in data

A copy of the original artwork image is stored locally under your filebrowser 
upload directory within _soundcloud_. 

### Getting an access token

You must first create an application on Soundcloud with your user. To get
a permananet token you can go to the _auth_ view of the app and follow the
instructions.

## Creds

More at [udox](http://github.com/udox).

### Contributions

Thoughts, support, modifications from the team at UDOX.

* [TomViner](http://github.com/tomviner)
* [SebastianThomas](http://github.com/sebastianthomas)
* [CDennington](http://github.com/cdennington)

