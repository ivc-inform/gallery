from django.conf.urls import url, include

from project.settings import ROOT_URL

urlpatterns = [
    url(r'^%s' % ROOT_URL[1:], include('project.urls')),
]