from crawling import crawler
from documents import number_of_documents
from scrapy.crawler import CrawlerProcess
from fake_useragent import UserAgent
from pathlib import Path

# construct filepath from filename
def get_corpus_filepath(corpus_filename):
    return str(
        Path(__file__)
        .parent
        .with_name("corpus")
        .joinpath(corpus_filename)
    )


def scrape(corpus_filename, start_url, max_pages=100, max_depth=3, overwrite=True):
    
    print("scraping starting from", start_url, "...")
    print("max pages =", max_pages)
    print("max depth =", max_depth)
    print("overwrite =", overwrite)
    
    ua = UserAgent()
    
    process = CrawlerProcess(
        settings={
            'USER_AGENT': ua.random,
            'HTTPERROR_ALLOWED_CODES': [403, 404],
            
            # allow for more items in case filtering yields less
            
            'CLOSESPIDER_PAGECOUNT' : min(max_pages + 25, int(max_pages * 1.5)),
            'CLOSESPIDER_ITEMCOUNT' : min(max_pages + 25, int(max_pages * 1.5)),
            
            'DEPTH_LIMIT' : max_depth,
            'LOG_LEVEL': 'CRITICAL',#'DEBUG',
            'FEEDS': {
                get_corpus_filepath(corpus_filename): {
                    'format': 'jsonl',
                    'encoding': 'utf8',
                    'overwrite': overwrite,
                    'store_empty': True,
                    'fields': None, # all fields
                    'indent': 4,
                },
            },
            'max_pages' : max_pages,
            'ITEM_PIPELINES': {
                "crawling.pipelines.EmptyFilterPipeline": 100,
                "crawling.pipelines.MaxPagesPipeline": 200,
            },
        }
    )
    
    process.crawl(
        crawler.SearchSpider, 
        start_urls=[start_url],
        max_depth=max_depth
    )
    process.start()
    
    num_docs = number_of_documents(corpus_filename)
    
    print("downloaded", num_docs, "documents")