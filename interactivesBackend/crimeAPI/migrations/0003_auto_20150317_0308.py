# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('crimeAPI', '0002_auto_20150316_2028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crime',
            name='geocode_location',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offense',
            name='name',
            field=models.CharField(max_length=80, db_index=True),
            preserve_default=True,
        ),
    ]
