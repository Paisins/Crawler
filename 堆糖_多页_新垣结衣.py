# 问题1：效率过低，下载48张图片，竟然等了十几秒钟，改进yield为list看有没有效果，另外尝试学习判断程序运行时间的工具 | 原因应该是gif过大（9M），导致下载速度较慢，至于效率不清楚。
# 问题2：gif还是不能正确下载，虽然没有报错，但是下载的gif文件不能动态演示 | 已解决
# 问题3：不使用headers也可以完成下载，难道不是Ajax加载吗？或者只是不需要审核headers中的信息？|
# 问题4：num参数的意义，以及如何得到，总不能老从浏览器上看到吧
# 这代码居然还能用！其实可以不用加num，照样可以下载图片，但是第一还是很好奇num的作用，另外似乎每次下载的图片都不相同，这种随机有没有办法控制，不然我就要创建一个txt文件来存储
# 已下载的图片链接，避免重复下载。
# 其他记录
# python可以合成gif图，这个挺感兴趣的
# Docstring的正确格式是什么？如何使用？
import os
import pickle
import requests
from urllib.parse import urlencode


def open_url(base_url, start, num=0):
    params = {'include_fields': 'top_comments%2Cis_root%2Csource_link%2Citem%2Cbuyable%2Croot_id%2Cstatus%2Clike_count%2Csender%2Calbum',
              '_type': ''}
    params['start'] = str(start)
    #　params['_'] = str(num)
    url = base_url + urlencode(params)
    # 刚开始忘记使用headers，结果一样可以得到数据，难道堆糖的不是异步加载吗？不然怎么可能呢？
    headers = {'Host': 'www.duitang.com',
               'Referer': 'https://www.duitang.com/search/?kw=%E6%96%B0%E5%9E%A3%E7%BB%93%E8%A1%A3&type=feed',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
               'X-Requested-With': 'XMLHttpRequest'}
    try:
        response = requests.get(url, headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.RequestException as e:
        print('打开网址时出现错误！')
        return None


# 这个函数是创建一个list好呢？还是直接用yield好呢？
# 爬虫速度变得特别慢，是否是因为yield呢？改进效率问题！
def get_img(response_json):
    for item in response_json.get('data').get('object_list'):
        link = item['photo']['path']
        yield link


# 后缀名中已包含'.'
def link_extension(link):
    (a, b) = link.rsplit('.', 1)
    if 'gif' in b:
        b = '.' + 'gif'
        return (a+b, b)
    else:
        b = '.' + b
        return (link, b)


def save_img(link, file_name, t):
    try:
        response = requests.get(link)
        with open(file_name, 'wb') as f:
            f.write(response.content)
        print(link)
        print('下载第%d张图片成功！' % t)
        return True
    except Exception as e:
        print('下载第%d张图片失败！' % t)
        return False


def run(save_path, page):
    base_url = 'https://www.duitang.com/napi/blog/list/by_search/?kw=%E6%96%B0%E5%9E%A3%E7%BB%93%E8%A1%A3&type=feed'
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    records_file = save_path+"/records.pk"
    if os.path.exists(records_file):
        with open(records_file, 'rb') as f:
            old_links = pickle.load(records_file)
    else:
        old_links = []
    start = 24
    # num参数需要人为获取，因为我不知道怎么获取
    num = 1525482336186
    t = 1
    links = []
    for i in range(page):
        start += 24*i
        # num += 1
        response_json = (open_url(base_url, start))
        if response_json:
            for link in get_img(response_json):
                if link in old_links:
                    continue
                else:
                    old_links.append(link)
                (link, extension) = link_extension(link)
                img_name = str(t) + extension
                if save_img(link, save_path + img_name, t):
                    t += 1
    with open(records_file, 'wb') as f:
        pickle.dump(old_links, f)
    print('共下载了%d张图片' % (t-1))
    
    
if __name__ == '__main__':
    # run函数一般需要两个参数，第一个是保存路径，第二个是下载图片轮数，每轮下载24张
    # 文件路径请以'/'作为文件名间隔符，如'folder1/folder2/'
    run('/home/jcj/Pictures/新垣结衣/', 1)
