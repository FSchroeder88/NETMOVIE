from django.contrib import admin
from .models import Video

class VideoAdmin(admin.ModelAdmin):
    fields = ('title', 'created_at', 'description', 'video_file', 'image_file', 'speciality')
    list_display = ('title', 'created_at', 'description', 'video_file', 'image_file', 'speciality')
    search_fields = ('title',)



admin.site.register(Video, VideoAdmin),
