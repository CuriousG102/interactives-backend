# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime

from scrapy.contrib.djangoitem import DjangoItem
from crimeAPI.models import Crime, Offense

import django
django.setup()


class CrimeItem(DjangoItem):
    django_model = Crime

class CrimeReportPipeline(object):
    def process_item(self, item, spider):
        i, exists = Crime.objects.get_or_create(report_number = item['report_number'])
        if not exists:
            i.report_number = item['report_number']

            time_format = "%a, %b-%d-%Y %H:%M"

            i.report_time = datetime.strptime(item['report_time'],
                                                 time_format)
            i.offense_time = datetime.strptime(item['offense_time'],
                                                  time_format)
            i.offense_address = item['offense_address']
            i.offense_census_tract = item['offense_census_tract']
            i.offense_district = item['offense_district']
            i.offense_area_command = item['offense_area_command']
            i.offense_investigator_assigned = item['offense_investigator_assigned']
            i = i.save()
            for offense in item['offenses']:
                offenseToAdd, created = Offense.objects.get_or_create(name=offense)
                i.offenses.add(offenseToAdd)

        return item