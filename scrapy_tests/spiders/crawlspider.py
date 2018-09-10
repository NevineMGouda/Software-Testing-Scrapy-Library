from scrapy.spiders import CrawlSpider
class CrawlJobsSpider(CrawlSpider):
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

    def closed(self, reason):
        return reason