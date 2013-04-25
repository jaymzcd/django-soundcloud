from django.conf.urls import patterns, url
from django.contrib.admin.views.decorators import staff_member_required

from .views import SoundCloudAuth, SoundCloudTracks, SoundCloudTrackView

urlpatterns = patterns('',
    url(r'^$', SoundCloudTracks.as_view(), name='list'),
    url(r'^(?P<slug>[\w-]+)/$', SoundCloudTrackView.as_view(), name='detail'),
    url(r'^auth/$', staff_member_required(SoundCloudAuth.as_view()), name='auth'),
)
