from scrapy.exceptions import DropItem

class EmptyFilterPipeline:

    def __init__(self):
        return

    def process_item(self, item, spider):
        if ("text" in item and len(item["text"].strip()) > 0):
            # print("not empty item")
            return item
        else:
            # print("empty item")
            raise DropItem(f"More than max pages")

class MaxPagesPipeline:

    item_count = 0

    def __init__(self, max_pages):
        self.max_pages = max_pages

    def process_item(self, item, spider):
        if self.item_count < self.max_pages:
            self.item_count += 1
            # print(self.item_count, "items")
            return item
        else:
            # print("max", self.item_count, "items")
            raise DropItem(f"More than max pages")
        
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        max_pages = settings.get('max_pages')
        return cls(max_pages)