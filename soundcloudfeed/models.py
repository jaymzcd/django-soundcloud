from django.core.urlresolvers import reverse
from django.db import models

from filebrowser.fields import FileBrowseField

from .managers import MostPlayedManager, MostRecentManager


class SoundcloudTrack(models.Model):
    """
        Soundcloud track model - all these fields have been lifted as is from
        http://developers.soundcloud.com/docs/api/reference#tracks and then amended
        to a suitable django model with a quick bit of multiline editing in
        SublimeText.

        Note that the resources returned from the current Soundcloud python API
        do not have all fields so where they dont exist they've been removed and
        left out of the model definition & syncing.
    """

    id = models.IntegerField(primary_key=True)
    artwork_url = models.URLField(max_length=255, blank=True)
    bpm = models.CharField(max_length=255, blank=True)
    comment_count = models.IntegerField(max_length=255, blank=True, null=True)
    commentable = models.BooleanField(default=True)
    created_at = models.DateTimeField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True)
    download_count = models.IntegerField(max_length=255, blank=True, null=True)
    download_url = models.URLField(max_length=255, blank=True)
    downloadable = models.BooleanField(default=True)
    duration = models.CharField(max_length=255, blank=True)
    embeddable_by = models.CharField(max_length=255, blank=True)
    favoritings_count = models.IntegerField(max_length=255, blank=True, null=True)
    genre = models.CharField(max_length=255, blank=True)
    isrc = models.CharField(max_length=255, blank=True)
    key_signature = models.CharField(max_length=255, blank=True)
    label_id = models.IntegerField(max_length=255, blank=True, null=True)
    label_name = models.CharField(max_length=255, blank=True)
    license = models.CharField(max_length=255, blank=True)
    original_content_size = models.IntegerField(max_length=255, blank=True, null=True)
    original_format = models.CharField(max_length=255, blank=True)
    permalink = models.CharField(max_length=255, blank=True)
    permalink_url = models.URLField(max_length=255, blank=True)
    playback_count = models.IntegerField(max_length=255, blank=True, null=True)
    purchase_url = models.URLField(max_length=255, blank=True)
    release = models.CharField(max_length=255, blank=True)
    release_day = models.CharField(max_length=255, blank=True)
    release_month = models.CharField(max_length=255, blank=True)
    release_year = models.CharField(max_length=255, blank=True)
    sharing = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    stream_url = models.URLField(max_length=255, blank=True)
    streamable = models.BooleanField(default=True)
    tag_list = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    track_type = models.CharField(max_length=255, blank=True)
    uri = models.CharField(max_length=255, blank=True)
    user_id = models.IntegerField(max_length=255, blank=True, null=True)
    user_name = models.CharField(max_length=255, blank=True)
    user_permalink = models.CharField(max_length=255, blank=True)
    user_permalink_url = models.URLField(max_length=255, blank=True)
    user_uri = models.URLField(max_length=255, blank=True)
    user_avatar = models.CharField(max_length=255, blank=True)
    user_favorite = models.CharField(max_length=255, blank=True)
    video_url = models.URLField(max_length=255, blank=True)
    waveform_url = models.URLField(max_length=255, blank=True)

    # Add an image field that we will be using to populate with a cached
    # filebrowser bound image
    image = FileBrowseField(directory='soundcloud/', format='image', max_length=5096, blank=True, null=True)

    # And add in our usual other timestamps we use
    modified_at = models.DateTimeField(null=True, blank=True)
    modified_at.help_text = 'Last modification time for this track (sync-side)'
    synced_at = models.DateTimeField(null=True, blank=True)
    synced_at.help_text = 'The last time a sync was ran against this track'

    # Custom managers
    top = MostPlayedManager()
    recent = MostRecentManager()

    class Meta:
        ordering = ('-created_at',)

    @property
    def body(self):
        if self.custom_description != '':
            return self.custom_description

        return self.description

    def __unicode__(self):
        return '%s (%s)' % (self.title, self.id)

    def get_absolute_url(self):
        return reverse('soundcloud:detail', kwargs={'slug': self.permalink})
