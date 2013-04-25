from django.db import models


class MostRecentManager(models.Manager):

    def get_query_set(self):
        return super(MostRecentManager, self).get_query_set().order_by('-created_at')


class MostPlayedManager(models.Manager):

    def get_query_set(self):
        return super(MostPlayedManager, self).get_query_set().order_by('-playback_count')
