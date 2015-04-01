# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photoMap', '0005_auto_20150328_2018'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subevent',
            name='event',
        ),
        migrations.DeleteModel(
            name='SubEvent',
        ),
        migrations.RemoveField(
            model_name='map',
            name='subevent_type',
        ),
        migrations.AddField(
            model_name='event',
            name='eventLink',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
