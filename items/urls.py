from django.urls import path
from django.views.generic import TemplateView, ListView, DetailView

from items.models.album import Album
from items.models.photos import Photo

# extra_context={'item_list': lambda: Album.objects.all()}),
urlpatterns = [
    # path('', TemplateView.as_view(template_name='index.html'), name='index'),
    # path('items/<int:pk>/', DetailView.as_view(template_name='items_detail.html', queryset=Album.objects.all()), name='album_detail'),
    # path('items/', ListView.as_view(template_name='items_list.html', queryset=Album.objects.all(), allow_empty=True), name='item_list'),
    # path('photos/<int:pk>/', DetailView.as_view(template_name='photos_detail.html', queryset=Photo.objects.all()), name='photo_detail')
]
