import sys
from cli import get_prefixes_for_index_build
from build_index import build_if_missing_index
from processor.query_processor import get_top_k_inds_by_score
from documents import load_document, get_corpus_filename_from_prefix
    
def run(trained_corpus_filename_prefix, search_corpus_filename_prefix):
    
    search_corpus_filename = get_corpus_filename_from_prefix(search_corpus_filename_prefix)
    
    cont = True
    
    while cont:
    
        # get input from user
        
        query_str = input("\nEnter query: ")
        
        valid_k = False
        while not valid_k:
            k = input("Number of results: ")
            
            try: 
                k = int(k)
                valid_k = k > 0
            except ValueError: print("\nsorry, invalid number of results, try again!\n")
        
            
        # query_str = "Jesus"
        # k = 5
        
            
        top_k_inds_by_score = get_top_k_inds_by_score(trained_corpus_filename_prefix, search_corpus_filename_prefix, query_str, k)
        
        if top_k_inds_by_score is None: # invalid query
            print("\nsorry, invalid query could not be searched. try again!")
        else:
            if len(top_k_inds_by_score) < k:
                print(
                    "\nSorry, no results found. Try another query!" 
                    if len(top_k_inds_by_score) == 0 else 
                    (f"\nLess than k={k} results found. Showing " +
                    str(len(top_k_inds_by_score)) +
                    " results.")
                )
        
            for n, i in enumerate(top_k_inds_by_score, 1):
                doc = load_document(search_corpus_filename, i)
                print("\nresult ", n, ":", "\t", doc["url"], " [", i+1, "]", sep="")
                print("\n", doc["text"][:500], "...", sep="")
                
            cont = input("\nTo continue, enter 'y': ").lower() == 'y'
    
        
        
if __name__ == "__main__":
    
    prms = get_prefixes_for_index_build(sys.argv[1:])
    if prms is not None:
        (trained_corpus_filename_prefix, search_corpus_filename_prefix) = prms
        
        success = build_if_missing_index(*prms)
        if success:
            print("build successful!")
        else:
            print("build unsuccessful.")
        
        if success:
            run(trained_corpus_filename_prefix, search_corpus_filename_prefix)