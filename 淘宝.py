# 根据崔庆才的博客写的
# 思考1：我以为每次打开URL却又不关闭，会有太多界面的问题，但是把它放在函数里面之后，因为局部变量的缘故吧，就不会有问题。
# 思考2：我的CSS基础太差了，原本以为够用了，现在觉得还是太嫩了，要多看
# 改进1：比如搜索MacBook就不行，页面稍微一改变，就会出错
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote
from pyquery import PyQuery as pq
import json
keyword = '零食'
browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)


def to_page(page):
    base_url = 'https://s.taobao.com/search?q='
    url = base_url + quote(keyword)
    browser.get(url)
    print('这是第%d页' % page)
    try:
        if page > 1:
            input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager .form input')))
            submit = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager span.btn.J_Submit')))
            input.clear()
            input.send_keys(page)
            submit.click()
        # 确定跳转到了正确的页面
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active span'), str(page)))
        # 确保所需的信息都已加载完全
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .item')))
        get_info(browser.page_source)
    except TimeoutException:
        print('%d页加载失败' % page)


def get_info(page):
    if page:
        doc = pq(page)
        dict = {}
        for item in doc('#mainsrp-itemlist .item.J_MouserOnverReq').items():
            # print(item('.pic').children().attr('trace-price'))  # 这是为什么？
            dict['价格'] = item('.pic').children().attr('trace-price')
            dict['图片'] = 'http:' + item('.J_ItemPic').attr('data-src')
            dict['购买人数'] = item('.deal-cnt').text()
            dict['介绍'] = item('.row-2 ').children().text()
            dict['地点'] = item('.location').text()
            dict['商店'] = item('.shop').text()
            print(dict)
            save_info(dict)
    else:
        print('出错了')


def save_info(dict):
    path = 'C:\\Users\\dell\\Desktop\\taobao.txt'
    with open(path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(dict, ensure_ascii=False))


if __name__ == '__main__':
    Page = 4
    for i in range(Page):
        i += 1
        to_page(i)
    print('程序已结束，共搜索了%d页' % i)
