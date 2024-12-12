from django.urls import path
from . import views

urlpatterns = [
    path('zoom/webhook/', views.zoom_webhook, name='zoom_webhook'),
]
