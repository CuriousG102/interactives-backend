# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import photoMap.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('latitude', models.FloatField(validators=[photoMap.models.validate_latitude])),
                ('longitude', models.FloatField(validators=[photoMap.models.validate_longitude])),
                ('name', models.CharField(max_length=80)),
                ('description', models.TextField(null=True, blank=True)),
                ('date', models.DateField()),
                ('image', models.ImageField(null=True, upload_to=b'photoMap', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Map',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('event_type', models.CharField(max_length=20)),
                ('subevent_type', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SubEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80)),
                ('description', models.TextField()),
                ('time', models.DateTimeField(null=True, blank=True)),
                ('image', models.ImageField(null=True, upload_to=b'photoMap', blank=True)),
                ('event', models.ForeignKey(to='photoMap.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='event',
            name='map',
            field=models.ForeignKey(to='photoMap.Map'),
            preserve_default=True,
        ),
    ]
