# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Crime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('report_number', models.CharField(max_length=50, null=True)),
                ('report_time', models.DateTimeField(null=True, db_index=True)),
                ('offense_time', models.DateTimeField(null=True, db_index=True)),
                ('offense_address', models.CharField(max_length=100, null=True)),
                ('offense_census_tract', models.CharField(max_length=20, null=True)),
                ('offense_district', models.CharField(max_length=5, null=True)),
                ('offense_area_command', models.CharField(max_length=50, null=True)),
                ('offense_investigator_assigned', models.CharField(max_length=50, null=True)),
                ('geocoded', models.BooleanField(default=False)),
                ('geocode_location', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Offense',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='crime',
            name='offenses',
            field=models.ManyToManyField(to='crimeAPI.Offense', db_index=True),
            preserve_default=True,
        ),
    ]
