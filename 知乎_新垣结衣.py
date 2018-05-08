# 该程序只能爬去单页，不能爬去异步加载之后的，可改进
#!/usr/bin/python
# -*- coding:utf8 -*-
import urllib.request
import urllib.error
from lxml import etree
import os
import os.path


def geturlimg(url, path):
    response = urllib.request.urlopen(url).read()
    html = response.decode('utf-8')
    page = etree.HTML(html)
    imglist = page.xpath('//img/@src')
    if not os.path.isdir(path):
        os.makedirs(path)
    i = 0
    for img in imglist:
        if extension(img):
            filename = path + '//' + str(i) + extension(img)
            try:
                urllib.request.urlretrieve(img, filename)
                i += 1
            except urllib.error.URLError as e:
                print('照片%d下载失败:'%i + str(e))


def extension(img):
    ext = os.path.splitext(img)[1]
    Type = ['.jpg', '.png', '.gif', '.jpeg']
    if ext in Type:
        return ext
    else:
        return None


if __name__ == "__main__":
    url = 'https://www.zhihu.com/question/22070147'
    print('搜索的网址是%s' % url)
    path = input('请输入存放的路径：')
    geturlimg(url, path)
