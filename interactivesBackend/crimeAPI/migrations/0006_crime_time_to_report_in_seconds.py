# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crimeAPI', '0005_auto_20150419_1850'),
    ]

    operations = [
        migrations.AddField(
            model_name='crime',
            name='time_to_report_in_seconds',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
    ]
