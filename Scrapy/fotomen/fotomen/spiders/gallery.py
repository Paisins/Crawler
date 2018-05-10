# -*- coding: utf-8 -*-
import scrapy
from fotomen.items import FotomenItem

class GallerySpider(scrapy.Spider):
    name = 'gallery'
    allowed_domains = ['fotomen.cn']
    task = 10
    start_urls = ['https://fotomen.cn/category/gallery/nature-gallery/page/'+str(i+1)+'/' for i in range(task)]

    def parse(self, response):
        imgs = response.css('.archive-main article')
        for img in imgs:
            item = FotomenItem()
            item['link'] = img.css('img::attr(src)').extract()[0].replace('/.','').replace('20x15','560x420')
            '''
            if 'IMG' not in item['link']:
                item['link'] = item['link'].replace('20x15','560x420')
            '''
            item['desc'] = img.css('.entry-title a::text').extract()[0]
            yield item
