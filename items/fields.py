import os

from PIL import Image
from django.db.models import ImageField
from django.db.models.fields.files import ImageFieldFile


class ThumbnailImageFieldFile(ImageFieldFile):
    def _add_thumb(self, s):
        """
        Modifies a string (filename, URL) containing an image filename, to insert
        '.thumb'
        """
        parts = s.split(".")
        parts.insert(-1, "thumb")
        if parts[-1].lower() not in ['jpeg', 'jpg']:
            parts[-1] = 'jpg'
        return ".".join(parts)

    @property
    def thumb_path(self):
        return self._add_thumb(self.path)

    @property
    def thumb_url(self):
        return self._add_thumb(self.url)

    def save(self, name, content, save=True):
        super().save(name, content, save)
        img = Image.open(self.path)
        img.thumbnail((self.field.thumb_width, self.field.thumb_height), Image.ANTIALIAS)
        img.save(self.thumb_path, 'JPEG')

    def delete(self, save=True):
        if os.path.exists(self.thumb_path):
            os.remove(self.thumb_path)
        super().delete(save)


class ThumbnailImageField(ImageField):
    attr_class = ThumbnailImageFieldFile

    def __init__(self, thumb_width=128, thumb_height=128, *args, **kwargs):
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height
        super().__init__(*args, **kwargs)
