import unittest
from pathlib import Path
from spiders import jobs
from spiders import xml
from spiders import csv
from spiders import sitemaps
from spiders import crawlspider
from crawler import CrawlerWithResults
from scrapy.crawler import CrawlerProcess
from scrapy.spiders.sitemap import iterloc
from scrapy.selector import Selector
from response import fake_response_from_file
from os.path import join, realpath, dirname
from random import sample, randint
import string
import logging

# TODO: maybe automate taking the url, downloading it and extracting results in required csvs


class SpiderTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(SpiderTests, self).__init__(*args, **kwargs)
        # Variables initializations
        self.xml_file_results = {}
        self.csv_file_results = []
        self._open_csv('csv_sample.csv')
        self._open_xml_results('xml-results.txt')

    def setUp(self):
        # Base/Super spider instantiations
        self.html_spider = jobs.JobsSpider()
        self.quotes_spider = jobs.QuotesSpider()

        # Crawl spider instantiations
        self.crawl_spider = crawlspider.CrawlJobsSpider()

        # CSV spider instantiations
        self.csv_spider = csv.CSVSpider()

        # Sitemap spider instantiations
        self.sitemaps_spider = sitemaps.LocalSitemapsSpider()
        self.sitemaps_spider.sitemap_urls = []

        # XML spider instantiations
        self.xml_spider = xml.XMLSpider()

    def _test_results_count(self, results, expected_length):
        count = 0
        for item in results:
            count += 1
        self.assertEqual(count, expected_length)
        return True

    def _test_each_field(self, results, filename, field):
        count = 0
        titles = []
        afile = join(dirname(realpath(__file__)), 'data', filename)
        with open(afile, 'r') as csv_file:
            csv_file.readline()  # Skip first line
            for line in csv_file.readlines():
                titles.append(line.strip())

        for item in results:
            response_item = item[field].encode(
                'ascii', 'ignore').decode('ascii')
            file_item = titles[count].encode('ascii', 'ignore').decode('ascii')
            count += 1
            self.assertEqual(response_item, file_item)
        return True

    def _open_xml_results(self, filename):
        afile = join(dirname(realpath(__file__)), 'data', filename)
        with open(afile, 'r') as text_file:
            for line in text_file.readlines():
                line_list = line.strip().split(":")
                cat = line_list[0]
                values = line_list[1].split(",")
                self.xml_file_results[cat] = values

    def _open_csv(self, filename):
        afile = join(dirname(realpath(__file__)), 'data', filename)
        with open(afile, 'r') as csv_file:
            for line in csv_file.readlines():
                line_list = line.strip().split(",")
                if len(line_list) != 3:
                    logging.getLogger(__name__).error('Warning!: Broken record in:' + filename)
                    continue
                record = {}
                record["id"] = line_list[0]
                record["name"] = line_list[1]
                record["gender"] = line_list[2]
                self.csv_file_results.append(record)

    def _test_xml(self, response_results, field):
        self.assertEqual(response_results[field], self.xml_file_results[field])
        return True

    # BASIC SPIDER TEST CASES
    def test_1(self):
        results = self.html_spider.parse(
            fake_response_from_file('sample1.html'))
        self._test_results_count(results, 120)

    def test_2(self):
        results = self.html_spider.parse(
            fake_response_from_file('sample1.html'))
        self._test_each_field(results, 'result-titles-1.csv', 'Title')

    def test_3(self):
        results = self.html_spider.parse(
            fake_response_from_file('sample1.html'))
        self._test_each_field(results, 'result-url-1.csv', 'URL')

    def test_4(self):
        results = self.html_spider.parse(
            fake_response_from_file('sample1.html'))
        self._test_each_field(results, 'result-address-1.csv', 'Address')

    def test_5(self):
        results = self.html_spider.parse(
            fake_response_from_file('sample2.html'))
        self._test_results_count(results, 120)

    def test_6(self):
        results = self.html_spider.parse(
            fake_response_from_file('sample2.html'))
        self._test_each_field(results, 'result-titles-2.csv', 'Title')

    def test_7(self):
        results = self.html_spider.parse(
            fake_response_from_file('sample2.html'))
        self._test_each_field(results, 'result-url-2.csv', 'URL')

    def test_8(self):
        results = self.html_spider.parse(
            fake_response_from_file('sample2.html'))
        self._test_each_field(results, 'result-address-2.csv', 'Address')

    #Test empty html
    def test_9(self):
        results = self.html_spider.parse(
            fake_response_from_file('sample3.html'))
        for i in results:
            self.assertEqual(i, {})

    # XML TEST CASES
    def test_10(self):
        html_response = fake_response_from_file('xml_sample.xml')
        sel = Selector(html_response)
        results = self.xml_spider.parse_node(html_response, sel)
        self._test_xml(results, 'title')

    def test_11(self):
        html_response = fake_response_from_file('xml_sample.xml')
        sel = Selector(html_response)
        results = self.xml_spider.parse_node(html_response, sel)
        self._test_xml(results, 'author')

    def test_12(self):
        html_response = fake_response_from_file('xml_sample.xml')
        sel = Selector(html_response)
        results = self.xml_spider.parse_node(html_response, sel)
        self._test_xml(results, 'year')

    def test_13(self):
        html_response = fake_response_from_file('xml_sample.xml')
        sel = Selector(html_response)
        results = self.xml_spider.parse_node(html_response, sel)
        self._test_xml(results, 'price')

    def test_14(self):
        html_response = fake_response_from_file('sample2.html')
        results = self.crawl_spider.parse(html_response)
        self._test_each_field(results, 'result-url-2.csv', 'URL')

    def test_15(self):
        html_response = fake_response_from_file('sample2.html')
        results = self.crawl_spider.parse(html_response)
        self._test_each_field(results, 'result-titles-2.csv', 'Title')

    def test_16(self):
        html_response = fake_response_from_file('sample2.html')
        results = self.crawl_spider.parse(html_response)
        self._test_each_field(results, 'result-address-2.csv', 'Address')

    def test_17(self):
        html_response = fake_response_from_file('sample3.html')
        results = self.crawl_spider.parse(html_response)
        for i in results:
            self.assertEqual(i,{})

    def test_18(self):
        html_response = fake_response_from_file('sample2.html')
        results = self.crawl_spider.parse(html_response)
        self._test_results_count(results, 120)

    # test parse_node with an empty xml
    def test_19(self):
        html_response = fake_response_from_file('xml_sample3.xml')
        sel = Selector(html_response)
        results = self.xml_spider.parse_node(html_response, sel)
        # Test generator for each field
        for field in results:
            self.assertEqual(len(results[field]), 0)

    # test parse_nodes with one node
    def test_20(self):
        html_response_1 = fake_response_from_file('xml_sample.xml')
        nodes = [Selector(html_response_1)]
        results = self.xml_spider.parse_several_nodes(html_response_1, nodes)
        # Test generator for each field
        for field in results:
            self._test_xml(results, field)

    # test parse_nodes with no nodes
    def test_21(self):
        html_response_1 = fake_response_from_file('xml_sample.xml')
        nodes = []
        results = self.xml_spider.parse_several_nodes(html_response_1, nodes)
        self.assertEqual(len(results), 0)

    # test parse_nodes with two nodes
    def test_22(self):
        self._open_xml_results('xml-total-results.txt')
        html_response_1 = fake_response_from_file('xml_sample.xml')
        html_response_2 = fake_response_from_file('xml_sample2.xml')
        nodes = [Selector(html_response_1), Selector(html_response_2)]
        results = self.xml_spider.parse_several_nodes(html_response_1, nodes)
        # Test generator for each field
        for field in results:
            self._test_xml(results, field)


    # Trying white box for feed.p/Class: XMLSpider, Function: parse
    def test_23(self):
        self._open_xml_results('xml-results2.txt')
        html_response = fake_response_from_file('xml_sample2.xml')
        result = self.xml_spider.parse_wb(response=html_response, iterator="xml", itertag='title')
        self.assertNotEqual(result, False)
        for record in result:
            for field in record:
                    self._test_xml(record, field)

    def test_24(self):
        self._open_xml_results('xml-results2.txt')
        html_response = fake_response_from_file('xml_sample2.xml')
        result = self.xml_spider.parse_wb(response=html_response, iterator="html", itertag='title')
        self.assertNotEqual(result,False)
        for record in result:
            for field in record:
                    self._test_xml(record, field)

    def test_25(self):
        self._open_xml_results('xml-results2.txt')
        html_response = fake_response_from_file('xml_sample2.xml')
        result = self.xml_spider.\
            parse_wb(response=html_response, iterator="iternodes", itertag='title')
        self.assertNotEqual(result, False)

    # corner case handling
    def test_26(self):
        html_response = fake_response_from_file('sample1.html')
        result = self.xml_spider.parse_wb(
            response=html_response, iterator="unknowniteratortest")
        self.assertFalse(result)


    # CSV TEST CASES
    # Test parse_row for each row in csv_sample.csv
    def test_27(self):
        html_response = fake_response_from_file('csv_sample.csv')
        for row in self.csv_file_results:
            results = self.csv_spider.parse_row(html_response, row)
            self.assertEqual(row, results)

    # Test parse_row for an empty csv file
    def test_28(self):
        html_response = fake_response_from_file('csv_sample_1.csv')
        # sel = Selector(html_response)
        results = self.csv_spider.parse_row(html_response)
        self.assertEqual(len(results), 0)

    # Test parse_rows for all rows in csv_sample.csv
    def test_29(self):
        html_response = fake_response_from_file('csv_sample.csv')
        # sel = Selector(html_response)
        results = self.csv_spider.parse_several_rows(html_response)
        self.assertEqual(results, self.csv_file_results)

    # Test parse_rows for an empty csv file
    def test_30(self):
        html_response = fake_response_from_file('csv_sample_1.csv')
        # sel = Selector(html_response)
        results = self.csv_spider.parse_several_rows(html_response)
        self.assertEqual(len(results), 0)


    # White box Testing __init__.py/start_requests
    def test_31(self):
        # test with default start_urls (3 urls)
        requests = self.quotes_spider.start_requests()
        self.quotes_spider.create_requests(requests)
        quotes_1 = Path("data/quotes-1.html")
        quotes_2 = Path("data/quotes-2.html")
        self.assertTrue(quotes_1.is_file())
        self.assertTrue(quotes_2.is_file())

    def test_32(self):
        # test with 2 urls
        self.quotes_spider.update_urls(['http://quotes.toscrape.com/page/1/', 'http://quotes.toscrape.com/page/2/'])
        requests = self.quotes_spider.start_requests()
        return_value = self.quotes_spider.create_requests(requests)
        self.assertTrue(return_value)
        quotes_1 = Path("data/quotes-1.html")
        quotes_2 = Path("data/quotes-2.html")
        self.assertTrue(quotes_1.is_file())
        self.assertTrue(quotes_2.is_file())

    def test_33(self):
        # test with 1 url
        self.quotes_spider.update_urls(['http://quotes.toscrape.com/page/1/'])
        requests = self.quotes_spider.start_requests()
        return_value = self.quotes_spider.create_requests(requests)
        self.assertTrue(return_value)
        quotes_1 = Path("data/quotes-1.html")
        quotes_2 = Path("data/quotes-2.html")
        self.assertTrue(quotes_1.is_file())
        self.assertTrue(quotes_2.is_file())

    def test_34(self):
        # test with no urls
        self.quotes_spider.update_urls([])
        requests = self.quotes_spider.start_requests()
        return_value = self.quotes_spider.create_requests(requests)
        self.assertFalse(return_value)

    # White box Testing __init__.py/start_requests, for a depreciated function
    def test_35(self):
        url = "http://quotes.toscrape.com/page/1/"
        request = self.html_spider.make_requests_from_url(url)
        self.quotes_spider.create_dep_requests(request)
        quotes_1 = Path("data/quotes-1.html")
        quotes_2 = Path("data/quotes-2.html")
        self.assertTrue(quotes_1.is_file())
        self.assertTrue(quotes_2.is_file())

    # White box Testing __init__.py/close
    def test_36(self):
        request = self.html_spider.close(self.html_spider, "close spider")
        self.assertEqual(request, "close spider")
        request = self.html_spider.close(self.quotes_spider, "close spider")
        self.assertNotEqual(request, "close spider")
        self.assertEqual(request, None)

        # Black box testing of sitemaps spiders.
    # All the tests are based on local files, to allow reproducibility.
    # The tests follow the examples available at the official sitemaps.org
    # website, respecting then the standard.

    def test_37(self):
        # Basic, useful data
        local_dir = self.sitemaps_spider.local_dir
        website_dir = self.sitemaps_spider.website_folder

        # Disable useless messages from the engine.
        # To be fair, they can be really useful in usual development context,
        # but here they fill up our tests output.
        # Based on: https://stackoverflow.com/a/33204694
        logging.getLogger('scrapy').setLevel(logging.WARNING)
        logging.getLogger('scrapy').propagate = False

        # Single element sitemap
        crawler_process = CrawlerProcess()
        crawler1 = CrawlerWithResults(self.sitemaps_spider)
        crawler_process.crawl(crawler1)
        crawler1.spider.sitemap_urls = [
            local_dir + website_dir + "/sitemap1.xml"]
        crawler1.spider.name += "1"
        # Multiple element sitemap
        crawler2 = CrawlerWithResults(self.sitemaps_spider)
        crawler_process.crawl(crawler2)
        crawler2.spider.sitemap_urls = [
            local_dir + website_dir + "/sitemap2.xml"]
        crawler2.spider.name += "2"
        # Multiple sitemaps within a sitemap
        crawler3 = CrawlerWithResults(sitemaps.LocalSitemapsSpider)
        crawler_process.crawl(crawler3)
        crawler3.spider.sitemap_urls = [
            local_dir + website_dir + "/sitemap3.xml"]
        crawler3.spider.name += "3"
        # Multiple sitemaps within a sitemap
        crawler4 = CrawlerWithResults(sitemaps.LocalSitemapsSpider)
        crawler_process.crawl(crawler4)
        crawler4.spider.sitemap_urls = [
            local_dir + website_dir + "/sitemap4.xml"]
        crawler4.spider.name += "4"

        # We can't run multiple processes in one script, due to the Twisted Reactor.
        # This is why we test everything in a single test unit.
        # Kind of bad, but it is the only way.
        crawler_process.start()

        # Check that all the tests are good
        # Single page sitemap
        self.assertEqual(crawler1.items, [{'1': '1'}])
        # Multiple page sitemap
        self.assertEqual(
            sorted((key, item[key])
                   for item in crawler2.items for key in item),
            [(str(x), str(x)) for x in range(2, 7)]
        )
        # Sitemaps within a sitemap
        self.assertEqual(
            sorted((key, item[key])
                   for item in crawler3.items for key in item),
            [(str(x), str(x)) for x in range(1, 7)]
        )
        # Compressed sitemaps within a sitemap
        self.assertEqual(
            sorted((key, item[key])
                   for item in crawler4.items for key in item),
            [(str(x), str(x)) for x in range(1, 7)]
        )

    # Whitebox testing for sitemap spiders.
    # The functions worthy to be tested are `_parse_sitemap` and `iterloc`; the
    # first one, although, has many nested conditionals and loops, up to 5
    # levels. `iterloc` has up to 3 levels, with only an intermixed loop with
    # a conditional (still within a loop, but better than the other).

    # Cover the loops 0 times
    def test_38(self):
        empty_iterator = []
        result1 = list(iterloc(empty_iterator))
        result2 = list(iterloc(empty_iterator, alt=True))
        self.assertEqual(result1, [])
        self.assertEqual(result2, [])

    def test_39(self):
        single_element_iterator = [
            {
                "loc": "location",
                "alternate": [
                    "alternate_location"
                ]
            }
        ]
        result1 = list(iterloc(single_element_iterator))
        result2 = list(iterloc(single_element_iterator, alt=True))
        self.assertEqual(result1, ["location"])
        self.assertEqual(sorted(result2),
            sorted(["location", "alternate_location"]))

    def test_40(self):
        good_characters = ''.join([
            x for x in string.printable
            if x not in string.punctuation and x not in string.whitespace
        ])
        oracle_iterator = [
            {
                "loc": sample(good_characters, randint(8,16)),
                "alternate": [
                    sample(good_characters, randint(8,16))
                    for _ in range(randint(0,10))
                ]
            } for _ in range(randint(0,100)) # Not too many tests
        ]
        # Let's build the correct results
        locations = sorted([x['loc'] for x in oracle_iterator])
        alternate = [l for x in oracle_iterator for l in x['alternate']]
        full = sorted(locations + alternate)
        # And get the iterloc ones
        result1 = sorted(list(iterloc(oracle_iterator)))
        result2 = sorted(list(iterloc(oracle_iterator, alt=True)))
        # Check the results
        self.assertEqual(result1, locations)
        self.assertEqual(result2, full)


if __name__ == "__main__":
    unittest.main()
