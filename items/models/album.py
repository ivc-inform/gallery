import logging

from django.db.models import Model, CharField, TextField

from items import permalink

logger = logging.getLogger(__name__)


class Album(Model):
    name = CharField(verbose_name="Наименование альбома", max_length=250)
    description = TextField(verbose_name="Характеристики альбома", blank=True, null=True)

    class Meta:
        verbose_name = 'Фотоальбом'
        verbose_name_plural = 'Фотоальбомы'

        ordering = ['name']

    def __str__(self):
        return f"{self.name}: {self.id}"

    @permalink
    def get_absolute_url(self):
        return ('item_detail', None, dict(pk=self.id))
