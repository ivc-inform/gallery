from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

from items.models.album import Album
from items.models.photo import Photo


class PhotoInline(admin.StackedInline):
    model = Photo


class AlbumAdmin(ModelAdmin):
    inlines = [PhotoInline]


admin.site.register(Album, AlbumAdmin)
# admin.site.register(Photo)
