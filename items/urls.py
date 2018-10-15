from django.urls import re_path

from items.views import IndexView, AlbumListView, AlbumDetailView, PhotosDetailView

urlpatterns = [
    re_path('^$', IndexView.as_view(), name='index'),
    re_path(r'^items/$', AlbumListView.as_view(), name='item_list'),
    re_path(r'^items/(?P<id>\d+)/$', AlbumDetailView.as_view(), name='item_detail'),
    re_path(r'^photos/(?P<id>\d+)/$', PhotosDetailView.as_view(), name='photo_detail')
]
