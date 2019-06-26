# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class JobsSpider(CrawlSpider):
    name = 'jobs'
    allowed_domains = ['www.python.org']
    start_urls = ['http://www.python.org/',
                  'https://www.python.org/jobs/']

    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=('.list-recent-jobs')),
        callback="parse_item",
        follow=True)
        ,)

    def parse_item(self, response):
        item_links = response.css('.text > .listing-company > .listing-location > a::text').extract()
        for x in item_links:
            yield scrapy.Request(x, callback=self.GeekItem)

