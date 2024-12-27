from django.contrib import admin
from .models import ZoomMeeting

class ZoomMeetingAdmin(admin.ModelAdmin):
    list_display = ('topic', 'course', 'start_time', 'recording_url')

# Register model
admin.site.register(ZoomMeeting, ZoomMeetingAdmin)
