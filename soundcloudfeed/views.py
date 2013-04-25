from django.views.generic import View, TemplateView, ListView, DetailView
from django.conf import settings
from soundcloud import Client

from .models import SoundcloudTrack


class SoundCloudAuth(TemplateView):
    """
        Authentication view for SC using OAuth - this is basically just here
        to generate an access token as they don't have a console like Facebook
        to quickly create one manually.

        Since we are likely to need this in future might as well create it in
        a class view now
    """

    template_name = 'radio/auth.html'

    def __init__(self):
        # Initialize the auth - we will want to get a non-expiring token
        # You can read and see flow here: http://developers.soundcloud.com/docs/api/guide#authentication
        self.sc = Client(
            client_id=settings.SOUNDCLOUD_CLIENT,
            client_secret=settings.SOUNDCLOUD_SECRET,
            redirect_uri=settings.SOUNDCLOUD_REDIRECT,
            scope='non-expiring'
        )

    def get_context_data(self, **kwargs):
        context = super(SoundCloudAuth, self).get_context_data(**kwargs)
        context['auth_url'] = self.sc.authorize_url()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        code = request.GET.get('code', None)

        if code is not None:
            access_token = self.sc.exchange_token(code)
            context['access_token'] = access_token

        return self.render_to_response(context)


class SoundCloudBaseView(View):

    model = SoundcloudTrack
    template_name = 'radio/soundcloudtrack_list.html'

    def __init__(self):
        # Initialize the auth - we will want to get a non-expiring token
        # You can read and see flow here: http://developers.soundcloud.com/docs/api/guide#authentication
        super(SoundCloudBaseView, self).__init__()
        self.sc = Client(
            access_token=settings.SOUNDCLOUD_ACCESS_TOKEN,
        )

    def get_context_data(self, **kwargs):
        context = super(SoundCloudBaseView, self).get_context_data(**kwargs)
        context['most_played_tracks'] = SoundcloudTrack.top_radio.all()[:settings.NUMBER_RADIO_SIDEBAR_TRACKS]
        context['radio_tracks'] = SoundcloudTrack.recent_radio.all()[:settings.NUMBER_RADIO_SIDEBAR_TRACKS + 1]
        context['archive_hide_after'] = settings.NUMBER_RADIO_SIDEBAR_ARCHIVE
        return context


class SoundCloudTracks(SoundCloudBaseView, TemplateView):

    def get_context_data(self, **kwargs):
        context = super(SoundCloudTracks, self).get_context_data(**kwargs)
        context['object'] = SoundcloudTrack.recent_radio.all()[0]
        return context


class SoundCloudTrackView(SoundCloudBaseView, DetailView):
    slug_field = 'permalink'
