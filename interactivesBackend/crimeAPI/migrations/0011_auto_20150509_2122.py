# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crimeAPI', '0010_auto_20150505_0027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offense',
            name='category',
            field=models.ForeignKey(related_name='offense', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='crimeAPI.Category', null=True),
            preserve_default=True,
        ),
    ]
