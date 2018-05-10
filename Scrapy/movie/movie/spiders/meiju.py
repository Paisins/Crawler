# -*- coding: utf-8 -*-
import scrapy
from movie.items import MovieItem


class MeijuSpider(scrapy.Spider):
    name = 'meiju'
    allowed_domains = ['meijutt.com']
    start_urls = ['http://www.meijutt.com/new100.html']  

    def parse(self, response):
        movies = response.xpath('//ul[contains(@class,"top-list") and contains(@class,"fn-clear")]/li') # ul[@class=" fn-clear"]/li

        for each_movie in movies:
            item = MovieItem()
            item['name'] = each_movie.xpath('./h5/a/@title').extract()[0]
            yield item
