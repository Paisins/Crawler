# 第一句话一定要讲：今日头条上我老婆的图片真的不好看，简直不能忍，要不是为了爬虫，我怎么能忍你们这样侮辱她，哼！
# 改进1：我只能爬搜索出来的封面上的几张图片，但是图集内部的还无法爬取，好在所有的图集貌似有一样的格式，应该可以做到
# 提示1：将keyword的参数换为其他的参数，都可以使用，相当于搜索时输入的关键词
import requests
from urllib.parse import urlencode
import os


def get_page(offset):
    params = {'offset': offset,
              'format': 'json',
              'keyword': '新垣结衣',
              'autoload': 'true',
              'count': '20',
              'cur_tab': '3',
              'from': 'gallery'}
    url = base_url + urlencode(params)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.ConnectionError as e:
        print(e)
        return None


def parse_page(page_json):
    # 图片主要在img_list和img_url中，其中前者有多个，后者只有一个，然后后者可能与前者重复
    for term in page_json.get('data'):
        # 建立空列表用来存储图片链接和标题
        links = []
        # 先得到标题和只有一个链接的img_url
        title = term.get('title')
        img_url = term.get('image_url')
        links.append(img_url)
        # 循环得到img_list中的所有图片链接
        for img in term.get('image_list'):
            # 判断是否与img_url相同
            if img_url != img.get('url'):
                links.append(img.get('url'))
        yield [title, links]


def save_image(info):
    # 此处为文件保存的位置，可以自定义
    path = 'D:\\My Python\\爬虫\\爬虫数据\\新垣结衣_今日头条\\' + info[0]
    if not os.path.exists(path):
        os.makedirs(path)
    # 记录每个文件夹下载的图片数目
    number = 0
    for item in info[1]:
        try:
            response = requests.get('http:'+item)
            if response:
                with open(path+'\\'+str(number)+'.jpg', 'wb') as f:
                    f.write(response.content)
                number += 1
            else:
                print('下载失败')
        except requests.ConnectionError as e:
            print(e)
    print('文件夹《%s》已下载%d张图片' % (info[0], number-1))


if __name__ == '__main__':
    base_url = 'https://www.toutiao.com/search_content/?'
    offset = 0
    for i in range(2):
        offset += i * 20
        page_json = get_page(str(offset))
        if page_json:
            for info in parse_page(page_json):
                save_image(info)
