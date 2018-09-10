"""
Custom Scrapy crawling process that allow to carry results.
Based on code found here: https://tryolabs.com/blog/2011/09/27/calling-scrapy-python-script/
"""
from scrapy import signals
from scrapy.crawler import Crawler
from pydispatch import dispatcher

class CrawlerWithResults(Crawler):
    """
    Crawler which hold results.
    Results are stored in a list named `items`.
    """
    def __init__(self, spidercls, settings=None):
        super(CrawlerWithResults, self).__init__(spidercls, settings)
        self.items = []
        self.signals.connect(self._item_passed, signals.item_passed)

    def _item_passed(self, item, response, spider):
        if spider.name == self.spider.name:
            self.items.append(item)
