from django.conf.urls import url
from django.views.generic import TemplateView, ListView, DetailView

from items.models.album import Album
from items.models.photo import Photo

# extra_context={'item_list': lambda: Album.objects.all()}),
urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^items/$', ListView.as_view(template_name='items_list.html', queryset=Album.objects.all(), allow_empty=True), name='item_list'),
    url(r'^items/(?P<object_id>\d+)/$', DetailView.as_view(template_name='items_detail.html', queryset=Album.objects.all()), name='item_detail'),
    url(r'^photos/(?P<object_id>\d+)/$', DetailView.as_view(template_name='photos_detail.html', queryset=Photo.objects.all()), name='photo_detail')
]
