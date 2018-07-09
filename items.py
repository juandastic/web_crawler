import scrapy
from scrapy import Item, Field

class CrowlItem(scrapy.Item):
    """
    Lists possible fields.
    """
    url = scrapy.Field()
    response_code = scrapy.Field()
    content_type = scrapy.Field()
    level = scrapy.Field()
    referer = scrapy.Field()
    latency = scrapy.Field()
    crawled_at = scrapy.Field()
    title = scrapy.Field()
    meta_robots = scrapy.Field()
    meta_description = scrapy.Field()
    meta_viewport = scrapy.Field()
    meta_keywords = scrapy.Field()
    canonical = scrapy.Field()
    h1 = scrapy.Field()
    wordcount = scrapy.Field()
    content = scrapy.Field()
    XRobotsTag = scrapy.Field()
    outlinks = scrapy.Field()
