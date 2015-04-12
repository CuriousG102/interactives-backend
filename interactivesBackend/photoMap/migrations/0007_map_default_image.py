# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photoMap', '0006_auto_20150401_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='map',
            name='default_image',
            field=models.ImageField(default='f', upload_to=b'photoMapDefaults'),
            preserve_default=False,
        ),
    ]
