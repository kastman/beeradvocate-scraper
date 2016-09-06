# Scrapy settings for beeradvocate project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'beeradvocate'

SPIDER_MODULES = ['beeradvocate.spiders']
NEWSPIDER_MODULE = 'beeradvocate.spiders'
LOG_FILE = 'beeradvocate.log'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'beeradvocate (+http://www.yourdomain.com)'
ROBOTSTXT_OBEY = True
BASE_URL = 'https://www.beeradvocate.com'

AUTOTHROTTLE_ENABLED = True
TELNETCONSOLE_ENABLED = False
