import argparse
import configparser
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
import scrapy
from utils import *
from spiders import Crowler
from pipelines import CrowlPipeline

def get_settings():
    """
    Define settings here.
    """
    settings = Settings({
        # User agent & headers
        'USER_AGENT': 'Crowl (+https://www.crowl.tech/)',
        'DEFAULT_REQUEST_HEADERS' : {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'fr'
        },        

        # Respect robots.txt
        'ROBOTSTXT_OBEY': True,

        # Crawl speed
        'DOWNLOAD_DELAY': 0.5, # Seconds between each request
        'CONCURRENT_REQUESTS': 5, # Number of concurrent spiders  

        # Crawling URLs from the same level before going deeper
        'DEPTH_PRIORITY': 1, # Don't touch
        'SCHEDULER_DISK_QUEUE': 'scrapy.squeues.PickleFifoDiskQueue', # Don't touch
        'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue', # Don't touch

        # Internal Scrapy stuff
        'HTTPERROR_ALLOW_ALL': True, # Allows to store results for non-200 URLs
        'RETRY_ENABLED': False,
        'MEDIA_ALLOW_REDIRECTS' : True,
        'LOG_LEVEL': 'INFO',
        'ITEM_PIPELINES': {
            'crowl.CrowlPipeline': 101
        }
    })

    return settings

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="SEO crawler")
    parser.add_argument('-u','--url',help="Start URL (required)",
        required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-b','--database',help="Project basename (new crawl)",
        type=str)
    group.add_argument('-r','--resume',help="Database (resume crawl)")
    parser.add_argument('-l','--links',help="Store links (default: False)",
        action='store_true',default=False)
    parser.add_argument('-c','--content',help="Store page content (default: False)",
        action='store_true',default=False)
    parser.add_argument('-d','--depth',help="Maximum crawl depth (default: 5)",
        default=5,type=int)
    parser.add_argument('--conf_file',help="Config file (default: config.ini)",
        default='config.ini',type=str)
    args = parser.parse_args()

    # Check if start URL is valid
    if not validate_url(args.url):
        print("Start URL not valid, please enter a valid HTTP or HTTPS URL.")
        exit(1)

    conf = {
        'url': args.url, 
        'links': args.links,
        'content': args.content,
        'depth': args.depth
    }

    settings = get_settings()

    config = configparser.ConfigParser()
    config.read(args.conf_file)
    settings.set('MYSQL_HOST',config['MYSQL']['MYSQL_HOST'])
    settings.set('MYSQL_PORT',config['MYSQL']['MYSQL_PORT'])
    settings.set('MYSQL_USER',config['MYSQL']['MYSQL_USER'])
    settings.set('MYSQL_PASSWORD',config['MYSQL']['MYSQL_PASSWORD'])

    # New crawl
    if(args.database):
        dbname = get_dbname(args.database)
        settings.set('MYSQL_DB',dbname)
        create_database(
            dbname,
            config['MYSQL']['MYSQL_HOST'],
            config['MYSQL']['MYSQL_PORT'],
            config['MYSQL']['MYSQL_USER'],
            config['MYSQL']['MYSQL_PASSWORD'])
        create_urls_table(
            dbname,
            config['MYSQL']['MYSQL_HOST'],
            config['MYSQL']['MYSQL_PORT'],
            config['MYSQL']['MYSQL_USER'],
            config['MYSQL']['MYSQL_PASSWORD'])
        if args.links:
            create_links_table(
                dbname,
                config['MYSQL']['MYSQL_HOST'],
                config['MYSQL']['MYSQL_PORT'],
                config['MYSQL']['MYSQL_USER'],
                config['MYSQL']['MYSQL_PASSWORD'])

    # Resume crawl
    else:
        dbname = args.resume
        settings.set('MYSQL_DB',dbname)

    # Set JOBDIR to pause/resume crawls 
    settings.set('JOBDIR','crawls/{}'.format(dbname))

    process = CrawlerProcess(settings)
    process.crawl(Crowler, **conf)
    process.start()
