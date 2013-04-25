from optparse import make_option

from django.core.management.base import BaseCommand
from django.utils import timezone

from dateutil import parser as date_parser
from soundcloudfeed.models import SoundcloudTrack
from soundcloudfeed.scloudlib import SoundcloudFeed
from soundcloudfeed.logger import setup_logging
from soundcloudfeed.image_handler import ImageHandlerFactory

logger = setup_logging(name="soundcloud_sync")


class Command(BaseCommand):
    help = 'Creates or updates Soundcloud track data'

    option_list = BaseCommand.option_list + (
        make_option(
            '-s', '--stats-only', action='store_true', dest='stats_only',
            help='Only update statistics - do not overwrite images & other data',
        ),
    )

    def _convert_date(self, date_string):
        return date_parser.parse(date_string).replace(tzinfo=timezone.utc)

    def _get_tracks(self):
        feed = SoundcloudFeed()
        return feed.tracks

    def _set_image(self, _track):
        # Pull in the source image. You can see a list of these here:
        # http://stackoverflow.com/a/13989369/1617409 though they seem to have
        # been removed (or more likely shifted elsewhere) on the original
        # linked API reference sections
        url = _track.artwork_url.replace('-large.', '-original.')
        return ImageHandlerFactory(url, _track.id).get().process()

    def _add_track(self, _track, stats_only=False):
        track, created = SoundcloudTrack.objects.get_or_create(id=_track.id)

        if not stats_only or created:
            track.artwork_url = _track.artwork_url or ''
            if _track.artwork_url is not None:
                # Cache our image locally
                track.image = self._set_image(_track)
            track.bpm = _track.bpm or ''
            track.comment_count = _track.comment_count
            track.commentable = _track.commentable
            track.created_at = self._convert_date(_track.created_at)
            track.description = _track.description or ''
            track.download_count = _track.download_count
            track.download_url = _track.download_url or ''
            track.downloadable = _track.downloadable
            track.duration = _track.duration or ''
            track.embeddable_by = _track.embeddable_by or ''
            track.favoritings_count = _track.favoritings_count
            track.genre = _track.genre or ''
            track.isrc = _track.isrc or ''
            track.key_signature = _track.key_signature or ''
            track.label_id = _track.label_id
            track.label_name = _track.label_name or ''
            track.license = _track.license or ''
            track.original_content_size = _track.original_content_size
            track.original_format = _track.original_format or ''
            track.permalink = _track.permalink or ''
            track.permalink_url = _track.permalink_url or ''
            track.playback_count = _track.playback_count
            track.purchase_url = _track.purchase_url or ''
            track.release = _track.release or ''
            track.release_day = _track.release_day or ''
            track.release_month = _track.release_month or ''
            track.release_year = _track.release_year or ''
            track.sharing = _track.sharing or ''
            track.state = _track.state or ''
            track.stream_url = _track.stream_url or ''
            track.streamable = _track.streamable
            track.tag_list = _track.tag_list or ''
            track.title = _track.title or ''
            track.track_type = _track.track_type or ''
            track.uri = _track.uri or ''
            track.user_id = _track.user['id']
            track.user_name = _track.user['username'] or ''
            track.user_permalink = _track.user['permalink'] or ''
            track.user_permalink_url = _track.user['permalink_url'] or ''
            track.user_uri = _track.user['uri'] or ''
            track.user_avatar = _track.user['avatar_url'] or ''
            track.user_favorite = _track.user_favorite or ''
            track.video_url = _track.video_url or ''
            track.waveform_url = _track.waveform_url or ''

        track.synced_at = timezone.now()
        track.save()

        if created:
            db_op = 'Added'
        else:
            db_op = 'Updated'

        info_string = "%s %s" % (db_op, _track.id)
        logger.info(info_string)
        self.stdout.write(info_string)

    def handle(self, *args, **kwargs):
        stats_only = kwargs.get('stats_only')
        self.stdout.write('Synchronizing with Soundcloud')

        tracks = self._get_tracks()
        for track in tracks:
            self._add_track(track, stats_only=stats_only)
