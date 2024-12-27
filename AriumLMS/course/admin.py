from django.contrib import admin
from .models import Course, CourseEnrollment

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'start_date', 'end_date',)
    search_fields = ('title',)  # Assuming instructor is a related user

class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course')

# Register models
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseEnrollment, CourseEnrollmentAdmin)
