import datetime
import re
from collections import deque

import scrapy
from scrapy.contrib.loader import ItemLoader
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from scrapy import log

from bs4 import BeautifulSoup

from ..items import CrimeReportItem

class ApdSpider(scrapy.Spider):
    name = "apd"
    allowed_domains = ["www.austintexas.gov"]

    def start_requests(self):
        start_page_url = 'https://www.austintexas.gov/police/reports/search2.cfm'
        return [Request(url=start_page_url, callback=self.clickThrough)]

    def clickThrough(self, response):
        return [FormRequest.from_response(response,
                                          callback = self.searchSelect)]

    def searchSelect(self, response):
        payload = {'choice':'criteria'}
        return [FormRequest.from_response(response,
                                          formdata=payload,
                                          callback = self.landing)]

    def landing(self, response):
        earliestDateString = response.selector.xpath("/html/body/div/div/div/div[2]/table[2]/tr/td/table/tr[1]/td[1]/p/b/text()").extract()[0]
        latestDateString = response.selector.xpath("/html/body/div/div/div/div[2]/table[2]/tr/td/table/tr[1]/td[2]/p/b/text()").extract()[0]
        dateStringFormat = "%m/%d/%Y"
        earliestDate = datetime.datetime.strptime(earliestDateString,
                                                  dateStringFormat).date()
        latestDate = datetime.datetime.strptime(latestDateString,
                                                dateStringFormat).date()

        ONE_DAY = datetime.timedelta(days = 1)

        while earliestDate <= latestDate:
            payload = { 'Submit':'Submit',
                        'address':'',
                        'choice':'criteria',
                        'city':'',
                        'district':'',
                        'numdays':'0',
                        'rucrext':'',
                        'startdate':earliestDate.strftime(dateStringFormat),
                        'tract_num':'',
                        'zipcode':'',
                        'zone':'' }

            yield FormRequest('https://www.austintexas.gov/police/reports/search2.cfm',
                              formdata = payload,
                              method = 'GET',
                              callback = self.listing)
            earliestDate += ONE_DAY

    def listing(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')

        crimes = []
        if not soup.find_all(text = 
        re.compile('You may have selected mutually exclusive criteria')):
            tables = soup.find_all(name = 'table', recursive = False)
            table = tables[0]
            crimes.append(self.scrapeFirstCrime(table))

            for i in xrange(1, len(tables), 2):
                table = tables[i]
                crimes.append(self.scrapeCrime(table))
        return crimes

    def scrapeFirstCrime(self, table):
        i = CrimeReportItem()

        position = [('tr', 0), ('td', 0), ('table', 0), ('tr', 0), ('td', 1)]
        i['report_number'] = self.getInfo(self.traverseToTag(position, table)).strip()
        position = [('tr', 0), ('td', 0), ('table', 0), ('tr', 0), ('td', 3)]
        i['report_time'] = self.getInfo(self.traverseToTag(position, table)).strip() 
        position = [('tr', 0), ('td', 0), ('table', 0), ('tr', 2), ('td', 1)]
        i['offense_time'] = self.getInfo(self.traverseToTag(position, table)).strip()
        position = [('tr', 0), ('td', 0), ('table', 0), ('tr', 4), ('td', 1)]
        offenses = self.traverseToTag(position, table)
        offenseList = []
        for offense in offenses.find_all(name = 'table', recursive = False):
            offenseList.append(self.getInfo(self.traverseToTag([('tr', 0), ('td', 0)],
                                                                offense)).strip())
        i['offenses'] = offenseList
        position = [('tr', 0), ('td', 0), ('table', 0), ('tr', 6), ('td', 1)]
        i['offense_address'] = unicode(self.getInfo(self.traverseToTag(position, 
                                                         table))).strip()
        position = [('tr', 0), ('td', 0), ('table', 0), ('tr', 7), ('td', 1)]
        i['offense_census_tract'] = unicode(self.traverseToTag(position, table).find_all(text = True)[1][2:]).strip()
        position = [('tr', 0), ('td', 0), ('table', 0), ('tr', 7), ('td', 1)]
        i['offense_district'] = unicode(self.traverseToTag(position, table).find_all(text = True)[3][2:]).strip()
        position = [('tr', 0), ('td', 0), ('table', 0), ('tr', 7), ('td', 1)]
        i['offense_area_command'] = unicode(self.traverseToTag(position, table).find_all(text = True)[5][2:]).strip()

        position = [('tr', 0), ('td', 0), ('table', 0), ('tr', 9), ('td', 1)]
        i['offense_investigator_assigned'] = self.getInfo(self.traverseToTag(position, 
                                                                             table)).strip()

        return i

    def scrapeCrime(self, table):
        i = CrimeReportItem()

        position = [('tr', 0), ('td', 1)]
        i['report_number'] = self.getInfo(self.traverseToTag(position, table)).strip()
        position = [('tr', 0), ('td', 3)]
        i['report_time'] = self.getInfo(self.traverseToTag(position, table)).strip()
        position = [('tr', 2), ('td', 1)]
        i['offense_time'] = self.getInfo(self.traverseToTag(position, 
                                                           table)).strip()

        position = [('tr', 4), ('td', 1)]
        offenses = self.traverseToTag(position, table)
        offenseList = []
        for offense in offenses.find_all(name = 'table', recursive = False):
            offenseList.append(self.getInfo(self.traverseToTag([('tr', 0), ('td', 0)],
                                            offense)).strip())
        i['offenses'] = offenseList
        position = [('tr', 6), ('td', 1)]
        i['offense_address'] = unicode(self.getInfo(self.traverseToTag(position, 
                                                                   table))).strip()
        position = [('tr', 7), ('td', 1)]
        i['offense_census_tract'] = unicode(self.traverseToTag(position, table).find_all(text = True)[1][2:]).strip()
        position = [('tr', 7), ('td', 1)]
        i['offense_district'] = unicode(self.traverseToTag(position, table).find_all(text = True)[3][2:]).strip()
        position = [('tr', 7), ('td', 1)]
        i['offense_area_command'] = unicode(self.traverseToTag(position, table).find_all(text = True)[5][2:]).strip()

        position = [('tr', 9), ('td', 1)]
        i['offense_investigator_assigned'] = self.getInfo(self.traverseToTag(position, 
                                                                   table)).strip()
       
        return i

    def getTag(self, tagToSearch, tagToFind, num):
        return tagToSearch.find_all(name = tagToFind, recursive = False)[num]

    def traverseToTag(self, tagList, rootTag):
        return self.traverseToTagb(deque(tagList), rootTag)

    def traverseToTagb(self, tagList, rootTag):
        if len(tagList) <= 0:
            return rootTag
        
        item = tagList.popleft()

        tagToFind = item[0]
        numTag = item[1]

        return self.traverseToTagb(tagList, self.getTag(rootTag, tagToFind, numTag))

    def getInfo(self, tag):
        return unicode(tag.find_all(text = True)[0])





















