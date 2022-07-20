from django.contrib import admin
from .models import Video

class VideoAdmin(admin.ModelAdmin):
    fields = ('title', 'created_at', 'description', 'video_file')
    list_display = ('title', 'created_at', 'description', 'video_file')
    search_fields = ('title',)



admin.site.register(Video, VideoAdmin),
