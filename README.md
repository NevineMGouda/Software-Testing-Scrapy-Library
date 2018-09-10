# Useful information for running the tests

## Be inside this folder!
As the tests use paths to point to the proper files and were meant to be
executed within this folder, you should `cd` here!

## For running tests
In order to execute the tests, run:
```bash
$ python test_file.py
```
We support officially Python 2, but Python 3 should also work.
**Notice**: remember install the proper packages (such as *Scrapy*)! *pip* is
your friend.

## For checking code coverage
In order to evaluate code coverage, run in a shell, after installing *coverage*:
```bash
$ coverage run --source=scrapy.spiders,spiders,. test_file.py
$ coverage html
```
You can then check the generated HTML code.

## To use XPath expressions within the Scrapy shell
Inside the Scrapy shell:
```python
response.selector.register_namespace('sm', 'http://www.sitemaps.org/schemas/sitemap/0.9')
```