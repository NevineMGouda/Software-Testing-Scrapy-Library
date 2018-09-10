from scrapy.spiders import CSVFeedSpider
from items import StudentItem
from os.path import join, realpath, dirname

class CSVSpider(CSVFeedSpider):
    name = 'csv'
    filename = "csv_sample.csv"
    afile = join(dirname(realpath(__file__)), 'data', filename)
    start_urls = [afile]
    delimiter = ','
    quotechar = "'"
    headers = ['id', 'name', 'gender']

    def parse_row(self, response, row):

        item = StudentItem()
        item['id'] = row['id']
        item['name'] = row['name']
        item['gender'] = row['gender']
        return item

    def parse_several_rows(self, response):
        result = []
        result_item = self.parse_rows(response)
        for record in result_item:
            result.append(record)
        return result