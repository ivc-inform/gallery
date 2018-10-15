from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve

from project import settings
from project.settings import ROOT_URL

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'{ROOT_URL[1:]}', include('items.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        path(r'%smedia/<path>.*' % ROOT_URL[1:], serve, {'document_root': settings.MEDIA_ROOT, }),
    ]
