#!/usr/bin/python
# -*- coding:utf8 -*-
import urllib.request
from lxml import etree

url = 'http://tieba.baidu.com/p/5104807868#!/l/p1'
file_path = 'D:\\My Python\\爬虫\\爬虫数据\\新垣结衣\\'
response = urllib.request.urlopen(url)
html = response.read().decode('utf-8')  # 解码有必要吗？
page = etree.HTML(html)
img_tag = page.xpath('//*[@class="BDE_Image"]/@src')
x = 0
for i in img_tag:
    file_name = file_path + '%d.jpg' % x
    urllib.request.urlretrieve(i, file_name)
    x += 1
print('共下载了%d张图片' % x)

#这是爬取单页帖子的代码，下次可以改进，爬完整个帖子。
