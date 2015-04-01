from django.core.management.base import BaseCommand, CommandError
from crimeAPI.scraper.CrimeReport.CrimeReport.spiders import apd

import scrapy
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.settings import Settings

class Command(BaseCommand):
    help = 'Update the PostGIS backend with the latest crimes\
            reported in the city of Austin'

    def handle(self, *args, **options):
        spider = apd.ApdSpider()
        settings = Settings()

        settings.setdict({ 'BOT_NAME':'CrimeReport',
                            'USER_AGENT':'Crime Scraper (+http://www.dailytexanonline.com/)',
                            'ITEM_PIPELINES':['crimeAPI.scraper.CrimeReport.CrimeReport.pipelines.CrimeReportPipeline'],
            })
        crawler = Crawler(settings)
        crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
        crawler.configure()
        crawler.crawl(spider)
        crawler.start()
        log.start(loglevel=scrapy.log.INFO)
        reactor.run()
