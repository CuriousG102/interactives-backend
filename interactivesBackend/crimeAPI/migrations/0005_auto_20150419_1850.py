# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crimeAPI', '0004_auto_20150419_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offense',
            name='category',
            field=models.ForeignKey(blank=True, to='crimeAPI.Category', null=True),
            preserve_default=True,
        ),
    ]
