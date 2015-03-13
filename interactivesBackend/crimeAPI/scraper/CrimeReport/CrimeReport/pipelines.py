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

from scrapy import log

class CrimeItem(DjangoItem):
    django_model = Crime

class CrimeReportPipeline(object):
    def process_item(self, item, spider):
        log.msg("what", levl=log.INFO)
        try:
            log.msg("in try", levl=log.INFO)
            i = Crime.objects.filter(report_number__exact = item['report_number'])[0]
        except IndexError:
            log.msg("in except", level=log.INFO)
            i = CrimeItem()
            i['report_number'] = item['report_number']

            time_format = "%a, %b-%d-%Y %H:%M"

            i['report_time'] = datetime.strptime(item['report_time'],
                                                 time_format)
            i['offense_time'] = datetime.strptime(item['offense_time'],
                                                  time_format)
            i['offense_address'] = item['offense_address']
            i['offense_census_tract'] = item['offense_census_tract']
            i['offense_district'] = item['offense_district']
            i['offense_area_command'] = item['offense_area_command']
            i['offense_investigator_assigned'] = item['offense_investigator_assigned']
            i = i.save(commit=False)
            for offense in item['offenses']:
                try:
                    offenseToAdd = Offense.objects.filter(name__exact = offense)[0]
                except IndexError:
                    offenseToAdd = Offense(name = offense)
                i.offenses.add(offenseToAdd)

            i.save()
            log.msg(i, level=log.INFO)

        return item