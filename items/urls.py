from django.urls import re_path, path

from items.views import IndexView, AlbumListView, AlbumDetailView, PhotosDetailView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('items/', AlbumListView.as_view(), name='item_list'),
    path('items/<int:pk>/', AlbumDetailView.as_view(), name='item_detail'),
    path(r'photos/<int:pk>/', PhotosDetailView.as_view(), name='photo_detail')
]
