import argparse

# get <trained_corpus_filename_prefix> <search_corpus_filename_prefix> from cli
def get_prefixes_for_index_build(args):
    
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "trained_corpus_filename_prefix", 
        help="prefix for corpus that index builder should be trained on"
    )
    parser.add_argument(
        "search_corpus_filename_prefix", 
        help="prefix for corpus that search index should be built from"
    )
    prms = parser.parse_args(args)
    
    return (prms.trained_corpus_filename_prefix, prms.search_corpus_filename_prefix)
    
# get <source_corpus_filename_prefix> <document_count1> <corpus_filename_prefix1> <document_count2> <corpus_filename_prefix2> from cli
def get_prefixes_for_split_corpus(args):
    
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "source_corpus_filename_prefix", 
        help="prefix for corpus to transfer documents from"
    )
    parser.add_argument(
        "document_count1", 
        help="number of documents from source corpus to save in corpus_filename_prefix1 file",
        type=int
    )
    parser.add_argument(
        "corpus_filename_prefix1", 
        help="prefix for corpus to get first <document_count1> documents from source corpus"
    )
    parser.add_argument(
        "document_count2", 
        help="number of documents from source corpus to save in corpus_filename_prefix2 file",
        type=int
    )
    parser.add_argument(
        "corpus_filename_prefix2", 
        help="prefix for corpus to get following <document_count2> documents from source corpus"
    )
    prms = parser.parse_args(args)
    
    return (prms.source_corpus_filename_prefix, prms.document_count1, prms.corpus_filename_prefix1, prms.document_count2, prms.corpus_filename_prefix2)

# get <start_url> <max_pages> <max_depth> <corpus_filename_prefix> from cli
def get_scraping_parameters(args):
    
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "corpus_filename_prefix", 
        help="prefix for downloaded corpus"
    )
    parser.add_argument(
        "start_url", 
        help="start url to crawl from"
    )
    parser.add_argument(
        "max_pages", 
        help="max pages to crawl",
        type=int
    )
    parser.add_argument(
        "max_depth", 
        help="max depth to crawl",
        type=int
    )
    prms = parser.parse_args(args)
    
    return (prms.corpus_filename_prefix, prms.start_url, prms.max_pages, prms.max_depth)
        

    