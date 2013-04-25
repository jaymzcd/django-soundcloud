#!/usr/bin/env python2
from __future__ import division

from soundcloud import Client
from django.conf import settings

from .logger import setup_logging
logger = setup_logging()


class SoundcloudFeedError(Exception):
    pass


class SoundcloudFieldKeyError(Exception):
    pass


class SoundcloudBase(object):
    pass


class SoundcloudFeed(SoundcloudBase):

    tracks = []

    def __init__(self, endpoint='/me/tracks', parse_now=True, access_token=None, **kwargs):
        self.endpoint = endpoint

        if access_token is None:
            self.access_token = settings.SOUNDCLOUD_ACCESS_TOKEN
        else:
            self.access_token = access_token

        self.kwargs = kwargs

        if parse_now:
            logger.info('Parsing feed on init')
            self.get()

        logger.info('Soundcloud:%s Feed ready' % endpoint)

    def get(self, **kwargs):
        """
            Reads in the json feed and updates _raw attribute
        """
        client = Client(access_token=self.access_token)
        self.tracks = client.get(self.endpoint, limit=kwargs.get('limit', 200), offset=kwargs.get('offset', 0))
        return self.tracks
