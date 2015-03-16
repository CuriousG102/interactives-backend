# -*- coding: utf-8 -*-

# Scrapy settings for apdCrimeReport project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'CrimeReport'

SPIDER_MODULES = ['CrimeReport.spiders']
NEWSPIDER_MODULE = 'CrimeReport.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Crime Scraper (+http://www.dailytexanonline.com/)'

ITEM_PIPELINES = [
        'CrimeReport.pipelines.CrimeReportPipeline'
    ]

LOG_LEVEL = 'INFO'