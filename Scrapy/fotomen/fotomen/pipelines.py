# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import requests
import os

class FotomenPipeline(object):
    def process_item(self, item, spider):
        filepath = 'D:\\My Python\\爬虫\\爬虫数据\\fotomen_scrapy\\'+ item['keyword']
        if not os.path.isdir(filepath):
            os.mkdir(filepath)
        filename = filepath + '\\' + item['desc']
        response = requests.get(item['link'])
        with open(filename+'.jpg', 'wb') as f:
            f.write(response.content)
