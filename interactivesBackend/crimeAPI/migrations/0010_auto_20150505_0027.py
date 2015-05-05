# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crimeAPI', '0009_auto_20150503_2132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offense',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='crimeAPI.Category', null=True),
            preserve_default=True,
        ),
    ]
