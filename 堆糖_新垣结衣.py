import requests
from pyquery import PyQuery as pq


def open_url(url):
    response = requests.get(url)
    try:
        if response.status_code == 200:
            return response.text
        else:
            return None
    except requests.RequestException as e:
        print(e)
        return None


def find_img(html):
    doc = pq(html)
    img = doc.find('img[alt=新垣结衣]').items()
    for i in img:
        yield i.attr.src


def get_extension(link):
    (a, b) = link.rsplit('.', 1)
    return '.' + b


def download(link, file_name):
    try:
        img = requests.get(link)
        path = 'D:\\My Python\\爬虫\\爬虫数据\\新垣结衣_堆糖\\' + file_name
        with open(path, 'wb') as f:
            f.write(img.content)
    except requests.RequestException as e:
        print(e)
    except IOError as e:
        print(e)


if __name__ == '__main__':
    #  此处应该修改
    url = 'https://www.duitang.com/search/?kw=%E6%96%B0%E5%9E%A3%E7%BB%93%E8%A1%A3&type=feed'
    html = open_url(url)
    if html:
        i = 1
        for link in find_img(html):
            extension = get_extension(link)
            file_name = str(i) + extension
            download(link, file_name)
            i += 1
        print('下载了%d张图片' % (i-1))
    else:
        print('网页未回复请求')
