import sys
from pathlib import Path

path = str(Path(__file__).parent.parent)
sys.path.append(path)

from scrape import scrape
from documents import check_if_0_documents

from pathlib import Path
import linecache
import json


if __name__ == "__main__":
    
    # "https://www.w3schools.com/python/python_file_open.asp"
    # start_url = 'https://ebible.org/pdf/eng-kjv/eng-kjv_WIS.pdf'
    # start_url = 'https://investors.digitalocean.com/governance/executive-management/default.aspx'
    # start_url = 'https://www.digitalocean.com/community/tutorials/how-to-crawl-a-web-page-with-scrapy-and-python-3'
    start_url = 'https://en.wikipedia.org/wiki/List_of_common_misconceptions'
    max_pages = 100
    max_depth = 3
    overwrite = True
    
    corpus_filename = "emp.jsonl"
    
    corpus_filepath = str(
        Path(__file__)
        .parent
        .with_name("corpus")
        .joinpath(corpus_filename)
    )
    
    
    scrape(corpus_filepath, start_url, max_pages, max_depth, overwrite)
    
    
    print("\n\n", "continuing", "\n\n")
    
    
    no_docs = check_if_0_documents(corpus_filename)
    
    if not no_docs:
        particular_line = linecache.getline(corpus_filepath, 4)
        
        doc = json.loads(particular_line)
        print("url:\t", doc["url"])
        print("text:\t", doc["text"][:250] + "...")
        print()
    
    with open(corpus_filepath, "r") as f:
        print(0 if no_docs else (len(f.readlines()) - 1), "docs")