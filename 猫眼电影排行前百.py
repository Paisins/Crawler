#实现的功能
#1、爬取前百的电影信息
#2、避免被封IP，控制爬虫速度
#3、设置各种异常的处理情况
#4、保存为txt文件

import requests
import re
import json
import time

def get_page(urls):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
        response = requests.get(urls, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except requests.exception.RequestException:
        return None
    

def find_info(response):    
    pattern = re.compile('board-index-(\d+).*?title="(.*?)".*?data-src="(.*?)".*?主演：(.*?)</p>.*?上映时间(.*?)</p>.*?class="integer">(.*?)</i>.*?class="fraction">(.*?)</i>', re.S)
    m = pattern.findall(response)
    for i in m:
        yield {
        'index': i[0],
        'name' : i[1],
        'picture' : i[2],
        'actors' : i[3].strip(),
        'time' : i[4],
        'score' : i[5]+i[6]
        }

    
def save_file(content):
    with open('C:\\Users\\dell\\Desktop\\猫眼排行榜.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')

if __name__ == '__main__':
    base_url = 'http://maoyan.com/board/4'
    for i in range(10):
        urls = base_url + '?offset=' + str(i*10)
        response = get_page(urls)
        for i in find_info(response):
            save_file(i)
    time.sleep(1)
