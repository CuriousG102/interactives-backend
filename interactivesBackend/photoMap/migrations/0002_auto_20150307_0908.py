# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photoMap', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='map',
            field=models.ForeignKey(related_name='maps', to='photoMap.Map'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subevent',
            name='event',
            field=models.ForeignKey(related_name='events', to='photoMap.Event'),
            preserve_default=True,
        ),
    ]
