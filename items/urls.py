from django.urls import re_path, path

from items.views import IndexView, AlbumListView, AlbumDetailView, PhotosDetailView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    re_path(r'^items/$', AlbumListView.as_view(), name='item_list'),
    re_path(r'^items/(?P<pk>\d+)/$', AlbumDetailView.as_view(), name='item_detail'),
    re_path(r'^photos/(?P<pk>\d+)/$', PhotosDetailView.as_view(), name='photo_detail')
]
