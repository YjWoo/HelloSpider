# -*-coding=utf-8-*- #

import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas


class DoubanBook:
    def page(self, url):
        list = []
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        for item in soup.select('ul li.store-item'):

            nameSelect = item.select('div.title a')
            authorSelect = item.select('span.labeled-text a')
            urlSelect = item.select('div.article-desc-brief a')

            if nameSelect:
                name = nameSelect[0].text
            else:
                name = None
            if authorSelect:
                author = authorSelect[0].text
            else:
                author = None

            if urlSelect:
                contextURL = 'https://read.douban.com' + urlSelect[0].attrs.get('href')
                context = BeautifulSoup(requests.get(contextURL).text, 'html.parser').select('div.info')[0].text
            else:
                context = item.select('div.info div.article-desc-brief')[0].text

            list.append([name, author, context])
        return list


i = 0
n = 0

category = ['小说', '文学', '人文社科', '经济管理', '科技科普', '计算机与互联网', '成功励志', '生活', '少儿', '艺术设计']
writer = pandas.ExcelWriter('DoubanBook.xlsx')

for n in range(category.__len__()):
    str = []
    for i in range(5):
        url = 'https://read.douban.com/kind/10{0}?start={1}'.format(n, i * 20)
        str.extend(DoubanBook().page(url))

    # 转多维数组
    str = np.array(str)
    result = pandas.DataFrame(str, columns=['书名', '作者', '简介'])
    result.to_excel(writer,sheet_name='{0}'.format(category[n]))
    writer.save()
    n += 1
