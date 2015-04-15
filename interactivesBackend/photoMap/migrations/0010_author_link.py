# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photoMap', '0008_auto_20150414_1805'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='link',
            field=models.URLField(default='http://www.dailytexanonline.com/'),
            preserve_default=False,
        ),
    ]
