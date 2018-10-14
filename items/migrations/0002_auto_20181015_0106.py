# Generated by Django 2.1.2 on 2018-10-14 22:06

from django.db import migrations, models
import items.fields


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='caption',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=items.fields.ThumbnailImageField(upload_to='photos%Y%m%d%H%M%S'),
        ),
    ]
