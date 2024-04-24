from documents import check_if_0_documents, get_build_from_prefix
from indexer.index_utils import valid_index

# get <start_url> <max_pages> <max_depth> [<save_filename_prefix>] from cli
def get_build_cli_options(argv):
    scraping = False
    
    start_url = None
    max_pages = None
    max_depth = None
    
    save_filename_prefix = None
    
    valid = True
    
    if len(argv) < 4:
        print("less than 3 arguments passed, try again!")
        valid = False
    elif len(argv) > 5:
        print("more than 4 arguments passed, try again!")
        valid = False
    else:
        
        # check arguments
        
        if len(argv) >= 4:
            
            scraping = True
            start_url = argv[1]
            
            try: 
                max_pages = int(argv[2])
            except ValueError:
                print("invalid value for max_pages:", argv[2], sep="")
                valid = False
            try: 
                max_depth = int(argv[3])
            except ValueError:
                print("invalid value for max_depth:", argv[3], sep="")
                valid = False
                
        if len(argv) == 5:
            save_filename_prefix = argv[4]
            
        
        if valid:
            return (scraping, start_url, max_pages, max_depth, save_filename_prefix)
        
# get filename for corpus and filename for index with [<save_filename_prefix>] from cli
def get_run_cli_build(argv):
    
    save_filename_prefix = None
    
    corpus_filename = "items.jsonl"
    index_filename = "index.pkl"
    
    valid = True
    
    if len(argv) > 2:
        print("more than 1 argument passed, try again!")
        valid = False
    else:
        
        if len(argv) == 2:
            save_filename_prefix = argv[1]
            
        
    (corpus_filename, index_filename) = get_build_from_prefix(save_filename_prefix)
            
    if check_if_0_documents(corpus_filename):
        print("empty or missing corpus corpus/'", corpus_filename, "', try again!", sep="")
        
    if valid_index(corpus_filename):
        print("invalid or missing index index/'", index_filename, "', try again!", sep="")
        
            
    if valid:
        return (corpus_filename, index_filename)
    