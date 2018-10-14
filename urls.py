from django.conf.urls.defaults import *
from django.urls import path, include

urlpatterns = [
    path('/', include('gallery.project.urls')),
]
