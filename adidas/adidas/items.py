# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AdidasItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class AdidasProductItems(scrapy.Item):
    name = scrapy.Field()
    colour = scrapy.Field()
    images = scrapy.Field()
    manufacturer = scrapy.Field()
    sku = scrapy.Field()
    url = scrapy.Field()
    category = scrapy.Field()
    availability = scrapy.Field()
    priceUSD = scrapy.Field()
    brandName = scrapy.Field()
    shippingRateValue = scrapy.Field()
    sellerName = scrapy.Field()
    sellerURL = scrapy.Field()
    applicableReturnCountry = scrapy.Field()
    returnPolicyCategory = scrapy.Field()
    merchantReturnDays = scrapy.Field()
    returnMethod = scrapy.Field()
    returnFees = scrapy.Field()
    ratingValue = scrapy.Field()
    reviewCount = scrapy.Field()
    bestRating = scrapy.Field()
    worstRating = scrapy.Field()
