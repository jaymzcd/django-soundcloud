from django.contrib import admin
from .models import SoundcloudTrack


class SoundcloudTrackAdmin(admin.ModelAdmin):
    list_filter = ('user_name', 'created_at',)
    list_display = ('title', 'id', 'playback_count', 'created_at', 'synced_at',)

admin.site.register(SoundcloudTrack, SoundcloudTrackAdmin)
