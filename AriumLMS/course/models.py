from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.timezone import now
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# # Create your models here.

# # Course Model
class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# Course Enrollment Model
class CourseEnrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateTimeField(default=now)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('completed', 'Completed')])

    def __str__(self):
        return f"{self.user.email} - {self.course.title}"

# Assignment Model
class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# Submission Model
class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submissions')
    file = models.FileField(upload_to='submissions/')
    grade = models.FloatField(null=True, blank=True)
    feedback = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(default=now)

class CourseMaterial(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='course_materials/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title