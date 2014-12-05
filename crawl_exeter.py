from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from testspiders.spiders.followall import FollowAllSpider
from scrapy.utils.project import get_project_settings


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
        Rule(LinkExtractor(allow=".*wiki/Anglo-Saxon_Riddles_of_the_Exeter_Book.*"),
            callback='save_file',
            follow=True),
    )

    def save_file(self, response):
        p = Path("data/" + response.url.split("/")[-1] + '.html')
        p.write_file(response.body)

spider = ExeterSpider()
settings = get_project_settings()
crawler = Crawler(settings)
crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
crawler.configure()
crawler.crawl(spider)
crawler.start()
log.start()
reactor.run() 