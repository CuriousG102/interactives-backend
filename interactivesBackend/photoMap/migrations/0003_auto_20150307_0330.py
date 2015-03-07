# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photoMap', '0002_auto_20150307_0908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='map',
            field=models.ForeignKey(related_name='events', to='photoMap.Map'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subevent',
            name='event',
            field=models.ForeignKey(related_name='subevents', to='photoMap.Event'),
            preserve_default=True,
        ),
    ]
