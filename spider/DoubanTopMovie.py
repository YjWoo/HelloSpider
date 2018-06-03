# -*-coding=utf-8-*- #

import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas
import os


class DoubanTopMovie:
    # 根据url获取文件名
    def getName(url):
        if url == None: return None
        if url == "": return ""
        arr = url.split("/")
        return arr[len(arr) - 1]

    def page(self, url):
        if not os.path.exists('DoubanTopMovie'): os.makedirs('DoubanTopMovie')
        list = []
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        for tar in soup.select('ol li'):
            rank = tar.select('div.item div.pic em')[0].text
            name = tar.select('div.item div.info div.hd a span')[0].text
            director = tar.select('div.item div.info div.bd p')[0].text.strip().split(' ')[1]
            score = tar.select('div.item div.info div.bd div span.rating_num')[0].text
            image = tar.select('div.item div.pic a img')[0].attrs.get('src')
            people = tar.select('div.item div.info div.bd div span')[3].text.rsplit('人评价')[0]
            # 保存图片到本地
            pic = requests.get(image)
            with open('DoubanTopMovie/' + DoubanTopMovie.getName(image), 'wb') as file:
                file.write(pic.content)

            list.append([rank, name, director, score, people])
            # print(rank, name, director)
        return list


i = 0
str = []
for i in range(10):
    url = 'https://movie.douban.com/top250?start={0}&filter='.format(i * 25)
    str.extend(DoubanTopMovie().page(url))

# 转多维数组
str = np.array(str)
result = pandas.DataFrame(str, columns=['排名', '片名', '导演', '评分', '评价人数'])
writer = pandas.ExcelWriter('DoubanTopMovie.xlsx')
result.to_excel(writer, 'sheet1')
writer.save()
