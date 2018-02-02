# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs

class JsonWriterPipeline(object):

    def __init__(self):
        self.file = codecs.open('items.json', 'wb', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"  # python3解决scrapy中文编码存储问题
        # print line
        self.file.write(line)
        return item
