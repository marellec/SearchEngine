from indexer.index_utils import build_inverted_index
from crawling.scrape import scrape
from documents import check_if_0_documents

def build_search_engine(scraping, start_url, max_pages, max_depth, overwrite=None):
    
    if overwrite is None:
        overwrite = True
    
    # scraping = True
    # start_url = 'https://en.wikipedia.org/wiki/List_of_common_misconceptions'
    # max_pages = 100
    # max_depth = 3
    
    corpus_filename = "items.jsonl"
    index_filename = "index.pkl"
    

    if scraping:
        scrape(corpus_filename, start_url, max_pages, max_depth, overwrite)

        if check_if_0_documents(corpus_filename):
            print("sorry, invalid url, try another one!")
            return
    
    build_inverted_index(corpus_filename, index_filename)
    
    return (corpus_filename, index_filename)