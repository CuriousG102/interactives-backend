from django.core.management.base import BaseCommand, CommandError
from crimeAPI.scraper.CrimeReport.CrimeReport.spiders import apd

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings

def Command(BaseCommand):
    help = 'Update the PostGIS backend with the latest crimes\
            reported in the city of Austin'

    def handle_noargs(self, *args, **options):
        spider = apd.ApdSpider()
        settings = get_project_settings()
        crawler = Crawler(settings)
        crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
        crawler.configure()
        crawler.crawl(spider)
        crawler.start()
        log.start(loglevel=scrapy.log.INFO)
        reactor.run()