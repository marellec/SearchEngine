
import scrapy
from scrapy import Request
import re
from random import shuffle

import justext



class SearchSpider(scrapy.Spider):
    name = 'search-spider'
    start_urls = []
    DOWNLOAD_DELAY = 1    # delay between requests in seconds
    
    urls_to_visit = set()
    
    #####   STOLEN FROM https://stackoverflow.com/questions/48042872/python-scrapy-creating-a-crawler-that-gets-a-list-of-urls-and-crawls-them
    def __init__(self, *args, **kwargs):
        super(SearchSpider, self).__init__(*args, **kwargs)
        self.start_urls = kwargs.get("start_urls")
        self.urls_to_visit = set(self.start_urls)
        
    def parse(self, response):
        
        # print("\n\n", response.status, "\n\n")
        
        if (response.status == 404):
            return
        
        url = response.url

        paragraphs = justext.justext(response.text, justext.get_stoplist("English"))
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
        # get rid of non-ascii chars
        
        # print("\n\n")
        # print(text[0:500])
        # print()
        # print(text[-500:])
        # print("\n\n")
        
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
        
        # find all <a> links that are website links
        
        # print("\n\n")
        # print(links[:8])
        # print()
        # print(links[-8:])
        # print("\n\n")
        
        yield {
            "url": url, 
            "text" : text,#text[:100],
        }
        
        # follow links in random order
        shuffle(links)
        for link in links:
            link_url = response.urljoin(link)
            
            if link_url not in self.urls_to_visit:
                self.urls_to_visit.add(link_url)
                yield Request(
                    link_url,
                    callback=self.parse
                )
            
        
            

