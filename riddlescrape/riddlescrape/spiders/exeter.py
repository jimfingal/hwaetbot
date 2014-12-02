# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from unipath import Path

class ExeterSpider(CrawlSpider):
    name = "exeter"
    allowed_domains = ["en.wikisource.org"]
    start_urls = (
        'http://en.wikisource.org/wiki/Anglo-Saxon_Riddles_of_the_Exeter_Book',
    )

    rules = (
        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=".*wiki/Anglo-Saxon_Riddles_of_the_Exeter_Book.*"), callback='save_file'),
    )

    def save_file(self, response):
        self.log('Hi, this is an item page! %s' % response.url)
        p = Path("data/" + response.url.split("/")[-1] + '.html')
        p.write_file(response.body)