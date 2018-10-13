import logging

from django.db.models import Model, CharField, TextField
from django.urls import reverse

logger = logging.getLogger(__name__)


class Album(Model):
    name = CharField(verbose_name="Наименование альбома", max_length=250)
    description = TextField(verbose_name="Характеристики альбома", blank=True, null=True)

    class Meta:
        verbose_name = 'Фотоальбом'
        verbose_name_plural = 'Фотоальбомы'

        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('item_detail', kwargs=dict(object_id=self.id))
