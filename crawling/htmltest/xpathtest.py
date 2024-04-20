
import scrapy
import re


print("scraping module")


def parse_text(txt):
    response = scrapy.Selector(text=txt, type="html")
    
    text = response.xpath(
        '//body/descendant-or-self::*[not(ancestor-or-self::header) and not(ancestor-or-self::nav) and not(ancestor-or-self::button) and not(ancestor-or-self::script) and not(ancestor-or-self::style)]/text()'
        # '//body/descendant-or-self::*[not(ancestor-or-self::header)]/text()'
        # '//body//*[not(ancestor-or-self::header)]/text()'
        # '//*[not(ancestor-or-self::header)]/text()'
    ).getall()
        
    # NO:
    # <header>
    # <nav>
    # <button>
    # <script>
    # <style>
    
    print("\n\n")
    print(text[:100])
    print()
    print(text[-100:])
    # print(type(text[0]))
    print("\n\n")
    
    

def parse_links(txt):
    response = scrapy.Selector(text=txt, type="html")
    
    links = response.xpath(
        "//a[not(starts-with(@href, '#'))]/@href"
    ).getall()
    
    # find all <a> links that are website links
    
    print("\n\n")
    print(links[:8])
    print()
    print(links[-8:])
    # print(type(text[0]))
    print("\n\n")
    
    
txt = """
<body>
<div>
not header text 1
<header>
some header text
<nav>
<ul>
<li>smore header text in nav in list</li>
</ul>
</nav>
</header>
not header text 2
</div>
</body>"""


with open("test.html", "r") as f:
    txt = f.read()
    
    
# parse_text(txt)
parse_links(txt)