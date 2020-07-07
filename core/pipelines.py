import datetime
import csv
import functools
import logging as log

from scrapy.exceptions import DropItem

from core.settings import OUTPUT_DIRECTORY


def check_spider_pipeline(process_item_method):
    @functools.wraps(process_item_method)
    def wrapper(self, item, spider):
        msg = '%%s %s pipeline step' % (self.__class__.__name__,)
        if self.__class__ in spider.pipeline:
            spider.log(msg % 'executing', level=log.DEBUG)
            return process_item_method(self, item, spider)
        else:
            spider.log(msg % 'skipping', level=log.DEBUG)
            return item

    return wrapper


class CSVPipeline(object):

    def __init__(self):
        self.time_format = "%Y-%m-%d_%H%M%S"
        self.seen = set()
        self.file = None
        self.writer = None
        self.filename = "default"

    def open_spider(self, spider):
        spider_name = spider.name
        now = datetime.datetime.now()
        now_str = now.strftime(self.time_format)
        target_dir = OUTPUT_DIRECTORY + "/" + spider_name + "/"
        self.filename = target_dir + spider_name + "_" + now_str + ".csv"
        self.file = open(self.filename, 'w')
        self.writer = csv.DictWriter(
            self.file,
            fieldnames=spider.colnames,
            lineterminator='\n'
        )
        self.writer.writeheader()

    @check_spider_pipeline
    def process_item(self, item, spider):
        item = dict(item)
        row = {col: item[col] for col in spider.colnames}
        dupe_check = row['section'] + '_' + row['url']
        if dupe_check in self.seen:
            raise DropItem("Dupe found: " + dupe_check)
        else:
            self.writer.writerow(row)
            self.seen.add(dupe_check)

    def close_spider(self):
        print("Finished processing file: " + self.filename)
        self.file.close()
