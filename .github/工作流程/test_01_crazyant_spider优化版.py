import requests
import random
from lxml import etree
import pprint
import simplejson


def get_UA():
    '''
    获取随机User-agent
    :return:
    '''
    ua_lists = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36 QIHU 360SE/12.1.2528.0',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
        'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    ]
    this_ua = random.choice(ua_lists)
    headers = {'User-agent': this_ua}
    print('当前使用的headers：' + str(headers))

    
# 一、分析目标网站并准备目标url
    
def get_url(i):
    '''
    获取目标网站url
    :param i: 你想获取多少页的url
    :return: 返回url_list
    '''
    url_list = []
    for idx in range(i):
        url = f"http://www.crazyant.net/page/{idx + 1}"
        url_list.append(url)
    return url_list


# 二、下载单个页面的HTML

def download_single_html(url):
    '''
    下载html页面
    :param url: 下载单个html页面的url
    :return: 返回html数据
    '''
    headers = get_UA()
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    response.encoding = response.apparent_encoding
    html = response.text
    return html


# 三、解析单个页面的HTML

def parse_single_html(html):
    '''
    :param html:解析单个html
    :return:
    '''
    data = []
    selector = etree.HTML(html)
    articles = selector.xpath('//article')
    for article in articles:
        # 获取title
        title = article.xpath('.//h2[@class="entry-title"]/a/text()')
        # 获取标签
        tags_list = article.xpath('.//footer/span[4]')
        tags = [tags.xpath('./a/text()') for tags in tags_list]
        # 获取超链接
        link = article.xpath('./header/h2/a/@href')
        # 添加到data
        data.append({"title": title, "tags": tags, "link": link})
    return data


# 四、保存数据到本地

def save_simplejson(data):
    '''
    将数据保存到本地
    :param data:
    :return:
    '''
    print("保存中...")
    with open("all_article_links优化版.json", "a") as f:
        for dat in data:
            f.write(simplejson.dumps(dat, ensure_ascii=False) + "\n")
        print("保存成功！")


def run():
    for url in url_list:
        print(url)
        html = download_single_html(url)
        data = parse_single_html(html)
        pprint.pprint(data)
        save_simplejson(data)


if __name__ == '__main__':
    url_list = get_url(27)
    run()
