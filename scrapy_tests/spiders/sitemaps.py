from os import name as os_name
from os.path import abspath, dirname
from scrapy.spiders import SitemapSpider


class LocalSitemapsSpider(SitemapSpider):
    name = "localsitemaps"
    #_local_dir = "file:///127.0.0.1/" + dirname(abspath(__file__)) + "/"
    _prefix = "file:///" if os_name is 'nt' else "file://"
    # The testing local directory, in proper URL syntax.
    local_dir = (_prefix + dirname(dirname(abspath(__file__))) +
                 "/").replace('\\', '/')
    # The relative path, from the testing main folder, where the scraped website
    # is included.
    website_folder = "data/fake_website"

    def __init__(self):
        super(LocalSitemapsSpider, self).__init__()
        self.crawled = []

    # Hacky way to support local website testing
    def _parse_sitemap(self, response):
        # Get the response body
        body = self._get_sitemap_body(response)
        # Decode the body properly
        if hasattr(response, 'encoding'):
            body = str(body.decode(response.encoding))
        else:
            body = str(body.decode())
        # Replace our special keyword
        body = body.replace('FOLDER', self.local_dir + self.website_folder)
        # Re-encode properly the body and create a proper `Response`
        if hasattr(response, 'encoding'):
            correct_response = response.replace(
                body=body.encode(response.encoding))
        else:
            correct_response = response.replace(body=body.encode())
        # Use the magical Scrapy code
        # Calling just the parent function does not work
        for element in super(LocalSitemapsSpider, self)._parse_sitemap(correct_response):
            yield element

    def parse(self, response):
        # return {response.url: response.body}
        title = response.xpath('//title/text()').extract_first()
        body = response.xpath('//body/text()').extract_first().strip()
        self.crawled.append((title, body))
        return {title: body}
