# from items import JobItem
from items import JobItem
from scrapy.spiders import XMLFeedSpider

class XMLSpider(XMLFeedSpider):
    name = 'xml'
    iterator = "iternodes"
    itertag = 'title'

    def parse_node(self, response, node):
        item = JobItem()
        item['title'] = node.xpath('//title[@lang="en"]/text()').extract()
        item['author'] = node.xpath('//author/text()').extract()
        item['year'] = node.xpath('//year/text()').extract()
        item['price'] = node.xpath('//price/text()').extract()
        return item


    def parse_several_nodes(self, response, nodes):
        result = {}
        result_item = self.parse_nodes(response, nodes)
        for i in result_item:
            for field in i:
                if field not in result:
                    result[field] = []
                result[field] += i[field]
        return result

    def parse_wb(self, response, iterator, itertag='title'):
        self.iterator = iterator
        self.itertag = itertag
        try:
            return self.parse(response)
        except:
            return False