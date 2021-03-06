import datetime
import csv
import functools
import logging as log
import json

from scrapy.exceptions import DropItem

from core.settings import DATA_DIRECTORY, ARTICLE_DIRECTORY, \
    ARTICLE_JSON_DIRECTORY


def check_spider_process_item(process_item_method):
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
        now = datetime.datetime.now()
        now_str = now.strftime(self.time_format)
        target_dir = DATA_DIRECTORY + "/" + spider.name + "/"
        if spider.colnames is not None:
            self.filename = target_dir + spider.name + "_" + now_str + ".csv"
            self.file = open(self.filename, 'w')
            self.writer = csv.DictWriter(
                self.file,
                fieldnames=spider.colnames,
                lineterminator='\n'
            )
            self.writer.writeheader()

    @check_spider_process_item
    def process_item(self, item, spider):
        item = dict(item)
        row = {col: item[col] for col in spider.colnames}
        dupe_check = row['section'] + '_' + row['url']
        if dupe_check in self.seen:
            raise DropItem("Dupe found: " + dupe_check)
        else:
            self.writer.writerow(row)
            self.seen.add(dupe_check)

    def close_spider(self, spider):
        print("Finished processing file: " + self.filename)
        self.file.close()


class ArticlePipeline(object):

    def __init__(self):
        self.time_format = "%Y-%m-%d_%H%M%S"
        self.seen = set()
        self.file = None
        self.writer = None
        self.filename = "default"

    def open_spider(self, spider):
        self.json_data = {}

    @check_spider_process_item
    def process_item(self, item, spider):
        target_dir = ARTICLE_DIRECTORY + "/" + spider.name + "/"
        filename = target_dir + item["url_hash"] + ".txt"
        self.file = open(filename, "w")
        article = " ".join(item["paragraphs"])
        self.file.write(article)
        self.file.close()
        self.json_data[item["url_hash"]] = item

    def close_spider(self, spider):
        now = datetime.datetime.now()
        now_str = now.strftime(self.time_format)
        json_dir = ARTICLE_JSON_DIRECTORY + "/" + spider.name + "/"
        filename = json_dir + spider.name + "_" + now_str + ".json"
        self.json_file = open(filename, "w")
        json.dump(self.json_data, self.json_file, indent=2, ensure_ascii=False)
        self.json_file.close()
