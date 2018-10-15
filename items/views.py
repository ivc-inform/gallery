from django.views.generic import TemplateView, ListView, DetailView

from items.models.album import Album
from items.models.photos import Photo


class IndexView(TemplateView):
    template_name = 'index.html'
    extra_context = {'item_list': lambda: Album.objects.all()}


class AlbumListView(ListView):
    template_name = 'items_list.html'
    context_object_name = 'object_list'
    allow_empty = True

    def get_queryset(self):
        return Album.objects.all()


class AlbumDetailView(DetailView):

    model = Album
    template_name = 'items_detail.html'

    def get_queryset(self):
        return Album.objects.all()


class PhotosDetailView(DetailView):
    model = Photo
    template_name = 'photos_detail.html'

    def get_queryset(self):
        return Photo.objects.all()
