import sys
from indexer.index_utils import build_inverted_index
from crawling.scrape import scrape
from documents import check_if_0_documents, get_build_from_prefix
from cli import get_build_cli_options

def build_search_engine(scraping, start_url, max_pages, max_depth, save_filename_prefix=None):
    
    overwrite = True
    
    # scraping = True
    # start_url = 'https://en.wikipedia.org/wiki/List_of_common_misconceptions'
    # max_pages = 100
    # max_depth = 3
    
    (corpus_filename, index_filename) = get_build_from_prefix(save_filename_prefix)

    if scraping:
        scrape(corpus_filename, start_url, max_pages, max_depth, overwrite)

        if check_if_0_documents(corpus_filename):
            print("sorry, invalid url, try another one!")
            return
    
    build_inverted_index(corpus_filename, index_filename)
    
    return (corpus_filename, index_filename)


if __name__ == "__main__":
    
    options = get_build_cli_options(sys.argv)
    
    if options is not None:
        build = build_search_engine(*options)
        if build is not None:
            print("build successful!")
        else:
            print("build unsuccessful.")