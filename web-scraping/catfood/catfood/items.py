# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CatfoodItem(scrapy.Item):
    name = scrapy.Field()
    brand = scrapy.Field()
    dry_wet = scrapy.Field()
    ingredients_paws = scrapy.Field()
    nutrition_paws = scrapy.Field()
    ingredients = scrapy.Field()
    allergens = scrapy.Field()
    carb_cals = scrapy.Field()
    fat_cals = scrapy.Field()
    prot_cals = scrapy.Field()
    total_cals = scrapy.Field()
    ga_prot = scrapy.Field()
    ga_fat = scrapy.Field()
    ga_fiber = scrapy.Field()
    ga_carbs = scrapy.Field()
    ga_ash = scrapy.Field()
    ga_moist = scrapy.Field()
    dma_prot = scrapy.Field()
    dma_fat = scrapy.Field()
    dma_fiber = scrapy.Field()
    dma_carbs = scrapy.Field()
    dma_ash = scrapy.Field()
    dma_cals = scrapy.Field()
