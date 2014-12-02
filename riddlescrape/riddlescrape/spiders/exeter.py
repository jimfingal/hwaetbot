# -*- coding: utf-8 -*-
import scrapy


class ExeterSpider(scrapy.Spider):
    name = "exeter"
    allowed_domains = ["http://en.wikisource.org/wiki/Anglo-Saxon_Riddles_of_the_Exeter_Book"]
    start_urls = (
        'http://en.wikisource.org/wiki/Anglo-Saxon_Riddles_of_the_Exeter_Book',
    )

    def parse(self, response):
        filename = response.url.split("/")[-1] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
