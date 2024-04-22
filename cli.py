

def get_cli_options(argv):
    scraping = False
    
    start_url = None
    max_pages = None
    max_depth = None
    
    save_filename_prefix = None
    
    valid = True
    
    if 1 < len(argv) < 4:
        print("between 0 and 3 arguments passed, try again!")
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