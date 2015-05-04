# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crimeAPI', '0007_remove_crime_time_to_report_in_seconds'),
    ]

    operations = [
        migrations.AddField(
            model_name='crime',
            name='time_to_report_in_seconds',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
    ]
