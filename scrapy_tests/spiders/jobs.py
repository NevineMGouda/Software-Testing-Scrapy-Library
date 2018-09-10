# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
class JobsSpider(scrapy.Spider):
    name = "jobs"
    allowed_domains = []

    def parse(self, response):
        jobs = response.xpath('//p[@class="result-info"]')
        if not jobs:
            yield {}
        for job in jobs:
            title = job.xpath('a/text()').extract_first()
            #titles = response.xpath('//a[@class="result-title hdrlnk"]/text()').extract()
            address = job.xpath('span[@class="result-meta"]/span[@class="result-hood"]/text()').extract_first("")[2:-1]
            relative_url = job.xpath('a/@href').extract_first()
            absolute_url = response.urljoin(relative_url)

            yield {'URL': absolute_url, 'Title': title, 'Address': address}
            # yield {'URL': absolute_url}
            # yield {'Title': title}
            # yield {'Address': address}

    def closed(self, reason):
        return reason

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/','http://quotes.toscrape.com/page/3/',
    ]

    def create_requests(self, requests):
        flag = False
        for request in requests:
            flag = True
            page = request.url.split("/")[-2]
            filename = 'data/quotes-%s.html' % page
            with open(filename, 'wb') as f:
                f.write(request.body)
        return flag


    def create_dep_requests(self, request):
        page = request.url.split("/")[-2]
        filename = 'data/quotes_dep-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(request.body)

    # Uncomment this function to cover the "if" in start_requests in test_parse_17
    def make_requests_from_url(self, url):
        return Request(url, dont_filter=True)

    def update_urls(self, urls):
        self.start_urls = urls
