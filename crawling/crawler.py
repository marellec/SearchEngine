
import scrapy
from scrapy import Request
import re
from random import shuffle

import justext



class SearchSpider(scrapy.Spider):
    name = 'search-spider'
    start_urls = []
    
     # delay between requests in seconds
    DOWNLOAD_DELAY = 1   
    
    # urls that have been found so far in crawling (prevent re-crawling urls)
    urls_to_visit = set()
    
    ####    https://stackoverflow.com/questions/48042872/python-scrapy-creating-a-crawler-that-gets-a-list-of-urls-and-crawls-them
    def __init__(self, *args, **kwargs):
        super(SearchSpider, self).__init__(*args, **kwargs)
        self.start_urls = kwargs.get("start_urls")
        self.urls_to_visit = set(self.start_urls)
        
    # parse response, yield item data (json), and request to scrape further links
    def parse(self, response):
        
        # print("\n\n", response.status, "\n\n")
        
        # do not crawl 404
        if (response.status == 404):
            return
        
        url = response.url

        # use justext to extract relevent text data from webpage
        paragraphs = justext.justext(
            response.text, 
            justext.get_stoplist("English"),
            # max_heading_distance=500,
            # length_low=10
        )
        paragraphs = [p.text for p in paragraphs if not p.is_boilerplate]
        
        # paragraphs = response.xpath(
        #     '//body/descendant-or-self::*[not(ancestor-or-self::header) and not(ancestor-or-self::nav) and not(ancestor-or-self::button) and not(ancestor-or-self::script) and not(ancestor-or-self::style)]/text()'
        #     # "//p/text()"
        # ).getall()
        
        # NO:
        # <header>
        # <nav>
        # <button>
        # <script>
        # <style>
        
        # normalize space
        text = re.sub(r'[\s\n\t]+', ' ', ' '.join(paragraphs))
        # separate numbers inside words
        text = re.sub(r'(?<=[a-zA-Z])([\d]+([^a-zA-Z\s]*[\d]+)*)(?=[a-zA-Z])', r' \1 ', text)
        # get rid of non-ascii chars
        text = "".join(ch for ch in text if ord(ch) <= 127) 
    
        # print("\n\n")
        # print(text[0:500])
        # print()
        # print(text[-500:])
        # print("\n\n")
        
        # find all <a> links that are website links
        links = response.xpath(
            "//a["
                "not(starts-with(@href, '#')) and "
                "not(starts-with(@href, 'javascript:')) and "
                "not(contains(@href, '@')) and "
                "not(starts-with(@href, 'tel:')) and "
                "not(starts-with(@href, 'mailto:')) and "
                "(substring(@href, string-length(@href) - string-length('.pdf') + 1) != '.pdf') and"
                "(substring(@href, string-length(@href) - string-length('.zip') + 1) != '.zip') and"
                "(substring(@href, string-length(@href) - string-length('.zip') + 1) != '.xls')"
            "]/@href"
        ).getall()
        
        # print("\n\n")
        # print(links[:8])
        # print()
        # print(links[-8:])
        # print("\n\n")
        
        # item data
        yield {
            "url": url, 
            "text" : text, #text[:100],
        }
        
        # follow links in random order (prevent re-crawling urls)
        shuffle(links)
        for link in links:
            link_url = response.urljoin(link)
            
            if link_url not in self.urls_to_visit:
                self.urls_to_visit.add(link_url)
                yield Request(
                    link_url,
                    callback=self.parse
                )
            
        
            

