# 第一句话一定要讲：今日头条上我老婆的图片真的不好看，简直不能忍，要不是为了爬虫，我怎么能忍你们这样侮辱她，哼！
# 改进1：我只能爬搜索出来的封面上的几张图片，但是图集内部的还无法爬取，好在所有的图集貌似有一样的格式，应该可以做到
# 改进2：主函数写得太丑了，以后有时间改一下
# 改进3：这次感觉到变量名称有些不够用了，乱用会导致全局变量和局部变量冲突，要注意
# 提示1：将keyword的参数换为其他的参数，都可以使用，相当于搜索时输入的关键词
# 提示2：这里下载的图片都是jpg格式的，这是因为我得到了URL中没有文件后缀，在保存的时候看到默认格式为jpg，所以全部用这个格式，如果搜索到其他格式的图片
#       文件，保存时可能会出现问题
# 提示3：仍然会有部分图片重复，但是已经筛选过图片的下载链接了，尽管链接不重复，可是下载的图片仍是同一张，这个暂时没办法处理
import os
import requests
from urllib.parse import urlencode


def get_page(base_url, offset):
    params = {'offset': str(offset),
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
            return True, response.json()
        else:
            return False, 'response.status_code： %d' % (response.status_code)
    except requests.ConnectionError as e:
        return False, e


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


def save_image(title, links, save_path):
    # 此处为文件保存的位置，可以自定义
    path = save_path + title
    if not os.path.exists(path):
        os.makedirs(path)
    # 记录每个文件夹下载的图片数目
    number = 0
    for img in set(links):
        try:
            response = requests.get('http:' + img)
            if response:
                with open(path+'\\'+str(number)+'.jpg', 'wb') as f:
                    f.write(response.content)
                number += 1
            else:
                print('%s下载失败' % img)
        except Exception as e:
            pass
    print('文件夹 %s 已下载%d张图片' % (title, number))


    
def run(save_path, page):
    base_url = 'https://www.toutiao.com/search_content/?'
    offset=0
    for i in range(page):
        offset += i * 20
        page_json = get_page(base_url, offset)
        if page_json[0]:
            for title,links in parse_page(page_json[1]):
                save_image(title, links, save_path)
        else:
            print(page_json[1])
            
            
if __name__ == '__main__':
    # run函数一般需要两个参数，第一个是保存路径，第二个是下载图片轮数，每轮下载20条头条数，注意这与图片数量无关，每个头条中一般会包含不定的多张图片
    # 文件路径请以'/'作为文件名间隔符，如'folder1/folder2/'
    run('', 1)
