from scrapy.exceptions import DropItem

# filter out items with no text
class EmptyFilterPipeline:

    def __init__(self):
        return

    def process_item(self, item, spider):
        if ("text" in item and len(item["text"].strip()) > 0):
            return item
        else:
            raise DropItem(f"Empty item")

# filter out items that go over max pages
class MaxPagesPipeline:

    item_count = 0

    def __init__(self, max_pages):
        self.max_pages = max_pages

    def process_item(self, item, spider):
        if self.item_count < self.max_pages:
            self.item_count += 1
            return item
        else:
            raise DropItem(f"More than max pages")
        
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        max_pages = settings.get('max_pages')
        return cls(max_pages)