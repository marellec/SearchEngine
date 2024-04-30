import sys
from crawling.scrape import scrape
from documents import check_if_0_documents, get_corpus_filename_from_prefix
from cli import get_scraping_parameters

def download_corpus(corpus_filename_prefix, start_url, max_pages, max_depth):
    
    overwrite = True
    
    # scraping = True
    # start_url = 'https://en.wikipedia.org/wiki/List_of_common_misconceptions'
    # max_pages = 100
    # max_depth = 3
    
    corpus_filename = get_corpus_filename_from_prefix(corpus_filename_prefix)

    scrape(corpus_filename, start_url, max_pages, max_depth, overwrite)

    if check_if_0_documents(corpus_filename):
        print("sorry, url yielded no documents, try another one!")
        return False
    
    return True
        

if __name__ == "__main__":
    
    prms = get_scraping_parameters(sys.argv[1:])
    if prms is not None:
        success = download_corpus(*prms)
        if success:
            print("crawl successful!")
        else:
            print("crawl unsuccessful.")