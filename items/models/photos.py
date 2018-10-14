import logging

from django.db.models import ForeignKey, CASCADE, CharField, Model
from django.db.models.fields.files import ImageField

from items import permalink
from items.models.album import Album

logger = logging.getLogger(__name__)


class Photo(Model):
    album = ForeignKey(Album, on_delete=CASCADE)
    title = CharField(max_length=250)
    image = ImageField(upload_to='photos')

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
        ordering = ['title']

    def __str__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        return ('photo_detail', None, dict(object_id=self.id))
