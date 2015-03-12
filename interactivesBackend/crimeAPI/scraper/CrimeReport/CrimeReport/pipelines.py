# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.contrib.djangoitem import DjangoItem
from crimeAPI.items import Crime, Offense

import django
django.setup()

class CrimeItem(DjangoItem):
	django_model = Crime

class CrimeReportPipeline(object):
    def process_item(self, item, spider):
        i = CrimeItem()
        i['report_number']
        i['report_time']
        i['offense_time']
        i['offenses']
        i['offense_address']
        i['offense_census_tract']
        i['offense_district']
        i['offense_area_command']
        i['offense_investigator_assigned']
        i['geocoded']
        i['geocode_location']













        return i