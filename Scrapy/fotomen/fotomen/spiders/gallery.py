# -*- coding: utf-8 -*-
# 在命令行启动时，按照‘scrapy crawl gallery -a keyword = keyword’这样的格式。其中keyword代表可选的种类，[portrait(人像),documentary(纪实),
# nature-gallery(风光) life-gallery(生活),art(艺术),film(胶片),still-life(静物),black-and-white-gallery(黑白),mobile-phone-photography
# (手机摄影)]，中文为注释，请输入其中一项英文,例如‘scrapy crawl gallery -a keyword = nature-gallery’
import scrapy
from fotomen.items import FotomenItem

class GallerySpider(scrapy.Spider):
    name = 'gallery'
    allowed_domains = ['fotomen.cn']
    
    def __init__(self, keyword=None, *args, **kwargs):
        super(GallerySpider, self).__init__(*args, **kwargs)
        self.keyword = keyword
        # 这里的数字10为页数，可以自由设置（上限？）
        self.start_urls = ['https://fotomen.cn/category/gallery/%s/page/'% keyword + str(i+1) + '/' for i in range(10)]

        
    def parse(self, response):
        imgs = response.css('.archive-main article')
        for img in imgs:
            item = FotomenItem()
            item['keyword'] = self.keyword
            item['link'] = img.css('img::attr(src)').extract()[0].replace('/.','').replace('20x15','560x420')
            item['desc'] = img.css('.entry-title a::text').extract()[0]
            yield item

