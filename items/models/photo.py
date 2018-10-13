import logging

from django.db.models import ForeignKey, CASCADE, CharField, Model
from django.urls import reverse

from items.fields import ThumbnailImageField
from items.models.album import Album

logger = logging.getLogger(__name__)


class Photo(Model):
    album = ForeignKey(Album, on_delete=CASCADE)
    title = CharField(max_length=100)
    image = ThumbnailImageField(upload_to='photos')
    caption = CharField(max_length=250, blank=True)

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('photo_detail', kwargs=dict(object_id=self.id))
