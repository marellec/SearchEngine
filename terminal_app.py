import sys
from cli import get_run_cli_build
from processor.query_processor import get_top_k_inds_by_score
from documents import load_document
    
def run(corpus_filename, index_filename):
    
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
        
            
        top_k_inds_by_score = get_top_k_inds_by_score(index_filename, query_str, k)
        
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
                doc = load_document(corpus_filename, i)
                print("\nresult ", n, ":", "\t", doc["url"], " [", i+1, "]", sep="")
                print("\n", doc["text"][:500], "...", sep="")
                
            cont = input("\nTo continue, enter 'y': ").lower() == 'y'
    
        
        
if __name__ == "__main__":
    
    build = get_run_cli_build(sys.argv)
    if build is not None:
        (corpus_filename, index_filename) = build
        run(corpus_filename, index_filename)