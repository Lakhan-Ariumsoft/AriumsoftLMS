from django.db import models
from course.models import Course


class ZoomMeeting(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    topic = models.CharField(max_length=200)
    meeting_id = models.CharField(max_length=50)
    start_time = models.DateTimeField()
    duration = models.IntegerField()
    recording_url = models.URLField()