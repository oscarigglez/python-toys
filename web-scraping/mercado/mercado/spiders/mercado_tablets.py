# -*- coding: utf-8 -*-
import scrapy


class MercadoTabletsSpider(scrapy.Spider):
    name = 'mercado_tablets'
    allowed_domains = ['listado.mercadolibre.com.mx']
    start_urls = ['https://listado.mercadolibre.com.mx/tablet']

    custom_settings = {
        'FEED_URI':"mercado_%(time)s.json",
        'FEED_FORMAT':'json'
    }

    def parse(self, response):
        print("processing: {}".format(response.url))
        tablet_name = response.css('.main-title::text').extract()
        #price_old = response.xpath("//div[@class='price__container']" +
        #        "/span[@class='price-old']/del/text()").extract()
        price_current = response.xpath("//div[@class='price__container']" +
                "/div[@class='item__price ']" + 
                "/span[@class='price__fraction']/text()").extract()

        row_data = zip(tablet_name, price_current)

        for item in row_data:
            scraped_info = {
                'page':response.url,
                'tablet_name':item[0],
                'price_new':item[1],
            }

            yield scraped_info

        NEXT_PAGE_SELECTOR = '.prefetch::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )
