from datetime import datetime
from decimal import Decimal
import logging
import re

from scrapy.selector import Selector

from beeradvocate.items import BeerAdvocateItem


class BeerDetailPageParserMixin(object):
    def parse_beer_detail(self, response):
        logging.info("Got beer detail for %s" % response.url)
        hxs = Selector(response)
        item = BeerAdvocateItem()

        ids = re.findall(r'profile/(?P<brewery_id>\d+)/(?P<beer_id>\d+)',
                         response.url)[0]
        item['brewery_id'] = ids[0]
        item['beer_id'] = ids[1]

        beer_name = hxs.xpath('//*[@id="content"]//h1/text()').extract()[0]
        item['name'] = beer_name

        details = hxs.xpath('//*[@id="ba-content"]/div[4]').extract()[0]
        brewery = re.findall(r'href="/beer/profile/%s/?"><b>([^<]+)' %
                             item['brewery_id'], details)[0]
        item['brewery'] = brewery
        style = re.findall(r'href="/beer/style/(\d+)/?"><b>([^<]+)',
                           details)[0]
        item['style_id'] = style[0]
        item['style'] = style[1]
        abv = re.findall(r'([0-9.]+)% <a href="/articles/518">ABV</a>',
                         details)
        if abv:
            item['abv'] = Decimal(abv[0].strip().strip('%'))

        notes = re.findall(
            r'Commercial Description:.*\n.*\n([\s\S]+)<br><br>Added',
            details)[0].strip()

        ibu_match = re.findall(r'(\d+) IBU', details, flags=re.IGNORECASE)
        if ibu_match:
            ibu = Decimal(ibu_match.groups()[0])
        else:
            ibu = None

        item['notes'] = notes
        item['ibu'] = ibu

        ba_score = hxs.xpath(
            '//*[contains(@class, "ba-score")]/text()').extract()[0]
        ba_bro_score = hxs.xpath(
            '//*[contains(@class, "ba-bro_score")]/text()').extract()[0]
        item['ba_score'] = ba_score
        item['ba_bro_score'] = ba_bro_score

        num_reviews = hxs.xpath(
            '//*[contains(@class, "ba-reviews")]/text()').extract()[0]
        num_ratings = hxs.xpath(
            '//*[contains(@class, "ba-ratings")]/text()').extract()[0]
        rAvg = hxs.xpath('//*[contains(@class, "ba-ravg")]/text()').extract()[
            0]
        pDev = hxs.xpath('//*[contains(@class, "ba-pdev")]/text()').extract()[
            0].strip().strip('%')
        wants = hxs.xpath('//*[contains(@class, "ba-wants")]/text()').extract(
        )[0]
        gots = hxs.xpath('//*[contains(@class, "ba-gots")]/text()').extract()[
            0]

        item['rAvg'] = Decimal(rAvg.strip())
        item['pDev'] = Decimal(pDev.strip())
        item['num_reviews'] = int(num_reviews.strip())
        item['num_ratings'] = int(num_ratings.strip())
        item['wants'] = int(wants.strip())
        item['gots'] = int(gots.strip())

        item['timestamp'] = datetime.utcnow()

        return item
