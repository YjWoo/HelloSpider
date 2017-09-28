# -*-coding=utf-8-*- #
import requests
import json
import os


# 利用Json返回单页图片地址
def WeiboAlbum(url, user_agent, cookies):
    headers = {"User-agent": user_agent, "Cookie": cookies}
    html = requests.get(url, headers=headers)
    dic = json.loads(html.text)
    dic = dic['data']['photo_list']
    images = []
    for i in range(len(dic)):
        pic_name = dic[i]['pic_name']
        pic_host = dic[i]['pic_host']
        pic_url = pic_host + '/large/' + pic_name
        images.append(pic_url)
    return images


# 返回图片总数
def WeiboPicSum(url, user_agent, cookies):
    headers = {"User-agent": user_agent, "Cookie": cookies}
    html = requests.get(url, headers=headers)
    dic = json.loads(html.text)
    return dic['data']['total']

# 获取指定用户的所有微博配图
if __name__ == "__main__":
    # 设置用户id
    uid = 0000000000
    # 设置user-agent
    user_agent = ''
    # 设置cookies
    cookies =''
    imagelist = []
    url = 'http://photo.weibo.com/photos/get_all?uid=%d&count=30&type=3&page=' % (uid)
    total = WeiboPicSum(url + '1', user_agent, cookies)

    #获取图片链接
    for i in range(1, total // 30 + 2):
        cur_url = url + '%d' % (i)
        imagelist.extend(WeiboAlbum(cur_url, user_agent, cookies))

    #保存本地文件
    filePath = 'E:\SpiderResource\WeiboPic\%d' % (uid)
    if not os.path.exists(filePath):
        os.makedirs(filePath)
    for i in range(len(imagelist)):
        pic = requests.get(imagelist[i])
        with open(filePath + '\%d.jpg' % (i), 'wb') as file:
            file.write(pic.content)
