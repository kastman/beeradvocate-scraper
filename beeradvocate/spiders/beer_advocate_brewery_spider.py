import logging
from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector

from beeradvocate.settings import BASE_URL
from beeradvocate.spiders.mixins import BeerDetailPageParserMixin


class BeerAdvocateBrewerySpider(Spider, BeerDetailPageParserMixin):
    name = "beeradvocate_brewery"
    allowed_domains = ["beeradvocate.com", "www.beeradvocate.com"]
    start_urls = [
        BASE_URL + "/place/directory/?show=all"
    ]

    def parse(self, response):
        return self.parse_country_list(response)

    def parse_country_list(self, response):
        logging.info("Got country list %s" % response.url)
        hxs = Selector(response)
        countries = hxs.xpath('//*[@id="ba-content"]/table/tr[2]/td/table')
        country_urls = countries.xpath('tr/td[2]/li/a/@href').extract()
        for country_url in country_urls:
            url = (BASE_URL + "/place/list/?c_id=%s"
                   "&s_id=0&brewery=Y") % country_url.strip('/').split('/')[-1]
            yield Request(url=url, callback=self.parse_country_details)

    def parse_country_details(self, response):
        logging.info("Got country details %s" % response.url)
        hxs = Selector(response)
        brewery_table = hxs.xpath('//*[@id="ba-content"]/table')

        breweries = brewery_table.xpath(
            'tr/td/a[contains(@href, "/beer/profile")]')
        for brewery in breweries:
            url = BASE_URL + brewery.xpath('@href').extract()[0]
            url += "?view=beers&show=all"
            yield Request(url=url, callback=self.parse_beer_list)

        next_links = brewery_table.xpath('.//a[text()="next"]/@href')
        if len(next_links):
            next_url = BASE_URL + next_links[0].extract()
            yield Request(url=next_url, callback=self.parse_country_details)

    def parse_beer_list(self, response):
        logging.info("Got beer list %s" % response.url)
        hxs = Selector(response)
        beer_table = hxs.xpath('//*[@id="ba-content"]/div/table')
        beer_urls = beer_table.xpath(
            'tr/td/a[contains(@href, "/beer/profile/") and not(contains(@href, "sort")) and not(contains(@href, "bros"))]')
        for beer_url in beer_urls:
            url = BASE_URL + beer_url.xpath('@href').extract()[0]
            yield Request(url=url, callback=self.parse_beer_detail)
