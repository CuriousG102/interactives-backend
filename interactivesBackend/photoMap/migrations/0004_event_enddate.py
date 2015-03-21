# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('photoMap', '0003_auto_20150307_0330'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='endDate',
            field=models.DateField(default=datetime.datetime(2015, 3, 21, 4, 8, 42, 378573, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
