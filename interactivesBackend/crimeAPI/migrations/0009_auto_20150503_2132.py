# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def subtract_times(apps, schema_editor):
    Crime = apps.get_model("crimeAPI", "Crime")
    for crime in Crime.objects.all():
        crime.time_to_report_in_seconds = (crime.report_time - crime.offense_time).total_seconds()
        crime.save()

class Migration(migrations.Migration):

    dependencies = [
        ('crimeAPI', '0008_crime_time_to_report_in_seconds'),
    ]

    operations = [
        migrations.RunPython(subtract_times),
    ]
