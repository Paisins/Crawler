# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MoviePipeline(object):
    def process_item(self, item, spider):
        with open('C:\\Users\\dell\\Desktop\\test.txt', 'a' ) as f:
            f.write(item['name'] + '\n')
