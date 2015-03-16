# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrimeReportItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    report_number = scrapy.Field()
    report_time = scrapy.Field()
    offense_time = scrapy.Field()
    offenses = scrapy.Field()
    offense_address = scrapy.Field()
    offense_census_tract = scrapy.Field()
    offense_district = scrapy.Field()
    offense_area_command = scrapy.Field()
    offense_investigator_assigned = scrapy.Field()