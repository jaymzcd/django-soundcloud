import os
import urllib

from filebrowser.base import FileObject
from filebrowser.functions import handle_file_upload

from django.conf import settings
from django.core.files.base import ContentFile

from radio.models import SoundcloudTrack


class ImageImportError(Exception):
    pass


class FilebrowserImage(object):

    def __init__(self, url, code):
        self.url = url
        self.code = code
        self.fn = '%s.jpg' % code

    def process(self):
        return self.make_file_obj()

    def download_img(self):
        IMAGE_MISSING_SIZE = 779
        bytes = urllib.urlopen(self.url).read()
        if len(bytes) == IMAGE_MISSING_SIZE:
            raise ImageImportError('Image missing at %s' % self.url)
        return ContentFile(bytes, name='%s.jpg' % self.code)

    def make_file_obj(self):
        field = SoundcloudTrack._meta.get_field('image')
        # filebrowser needs a FileObject so we can't return a
        # ContentFile like we would for an ImageField
        # so we use filebrowser's own handler, which seems to work fine
        path = field.directory + self.fn
        full_path = os.path.join(settings.MEDIA_ROOT, path)
        # assert os.path.exists(full_path), full_path
        if os.path.exists(full_path):
            stored_at = path
        else:
            content_file = self.download_img()
            stored_at = handle_file_upload(field.directory, content_file, field.site)
        return FileObject(stored_at, site=field.site)
