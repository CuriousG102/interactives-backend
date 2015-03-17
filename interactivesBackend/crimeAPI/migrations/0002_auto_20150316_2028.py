# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('crimeAPI', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crime',
            name='geocode_location',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='crime',
            name='geocoded',
            field=models.BooleanField(default=False, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='crime',
            name='offense_address',
            field=models.CharField(max_length=100, null=True, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='crime',
            name='offense_area_command',
            field=models.CharField(max_length=50, null=True, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='crime',
            name='offense_census_tract',
            field=models.CharField(max_length=20, null=True, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='crime',
            name='offense_district',
            field=models.CharField(max_length=5, null=True, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='crime',
            name='offense_investigator_assigned',
            field=models.CharField(max_length=50, null=True, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='crime',
            name='report_number',
            field=models.CharField(max_length=50, null=True, db_index=True),
            preserve_default=True,
        ),
    ]
