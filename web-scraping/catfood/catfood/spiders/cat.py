# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from catfood.items import CatfoodItem
import urllib

class CatSpider(scrapy.Spider):
    name = 'cat'
    allowed_domains = ['catfooddb.com']
    start_urls = ['http://catfooddb.com/']
    custom_settings = {
        'FEED_URI':"food_%(time)s.csv",
        'FEED_FORMAT':'csv',
        #'FEED_EXPORT_FIELDS': ["page", "page_ix", "text", "url"]
    }

    def parse(self, response):
        """Follow links to brand pages"""
        # The cleanest way to get to the brand pages is through the dropdown menu
        path = "//ul[@class='dropdown-menu']/li/a/@href"
        for href in response.xpath(path)[:-6][0:2]:
            print(href)
            yield response.follow(href, self.parse_brand)

    def parse_brand(self, response):
        """Follow links to product pages"""
        # All product pages have the .product class
        for href in response.xpath("//td[@class='product']/a/@href"):
            yield response.follow(href, self.printwhatever)

    def printwhatever(self, response):
        """Populate the item CatfoodItem with all the relevant product information"""
        l = ItemLoader(item=CatfoodItem(), response=response)
        # Get the product name from the response url
        name = response.url.split('/')[-1].replace('+', ' ')
        name = urllib.parse.unquote(name)
        l.add_value('name', name)
        # Get the brand name from the response url
        brand = response.url.split('/')[-2]
        brand = urllib.parse.unquote(brand)
        l.add_value('brand', brand)
        # Determine wether the food is dry or wet
        # Count the number of ingredients paws
        i_paws = len(response.xpath("//i[@class='fa fa-paw ingredients-paws']"))
        l.add_value('ingredients_paws', i_paws)
        # Count the number of nutrition paws
        n_paws = len(response.xpath("//i[@class='fa fa-paw nutrition-paws']"))
        l.add_value('nutrition_paws', n_paws)
        # Get the list of ingredients
        ingredients = response.xpath('//small/text()')[2].extract().split(', ')
        l.add_value('ingredients', ingredients)
        # General xpath for calorie info
        #cal_xpath = '//*[@id="calorie-chart"]/div/div[1]/div/div/table/tbody/tr[{}]/td[2]'
        # Get the carbohydrate calories
        #l.add_xpath('carb_cals', cal_xpath.format(1))
        # Get the fat calories
        #l.add_xpath('fat_cals', cal_xpath.format(2))
        # Get the protein calories
        #l.add_xpath('prot_cals', cal_xpath.format(3))
        # Get nutritional values as a list and assign them
        ga_list = response.xpath('//div[@class="panel panel-default"]'
                '[div[@class="panel-heading"]/h3/text()="Guaranteed Analysis"]'
                '/div[@class="panel-body"]'
                '/div/div[contains(@class,"text-right")]/text()').extract()
        dma_list = response.xpath('//div[@class="panel panel-default"]'
                '[div[@class="panel-heading"]/h3/text()="Dry Matter Analysis"]'
                '/div[@class="panel-body"]'
                '/div/div[contains(@class,"text-right")]/text()').extract()
        l.add_value(None, {'ga_prot':ga_list[0],
                           'ga_fat':ga_list[1],
                           'ga_fiber':ga_list[2],
                           'ga_carbs':ga_list[3],
                           'ga_ash':ga_list[4],
                           'ga_moist':ga_list[5],
                           'dma_prot':dma_list[0],
                           'dma_fat':dma_list[1],
                           'dma_fiber':dma_list[2],
                           'dma_carbs':dma_list[3],
                           'dma_ash':dma_list[4],
                           'dma_cals':dma_list[-1]})
        fooditem = l.load_item()
        if int(fooditem['ga_moist'][0].split('.')[0]) > 50:
            fooditem['dry_wet'] = 'wet'
        else:
            fooditem['dry_wet'] = 'dry'
        yield fooditem
