import requests
import json
import time
import pandas as pd


def __str2json(response):
    content = response.text[7:-1]
    result = '[' + content + ']'
    result = json.loads(result)
    return result


def __get_param(url, size):
    url = url % (1, size)
    res = requests.get(url)
    res.encoding = 'gbk'
    content = __str2json(res)
    param = {}
    param['TotalPage'] = content[0]['TotalPage']
    param['TotalCount'] = content[0]['TotalCount']
    param['PageSize'] = content[0]['PageSize']
    series = pd.Series(content[0]['Data'][0])
    df = pd.DataFrame(columns=series.index)
    return df, param


if __name__ == '__main__':
    url = 'http://data.eastmoney.com/gstc/search.ashx?&PageIndex=%s&PageSize=%s'
    size = 100
    df, param = __get_param(url, size)
    print(param)
    for i in range(1, param['TotalPage'] + 1):
        time.sleep(0.5)
        res = requests.get(url % (i, size))
        res.encoding = 'gbk'
        content = __str2json(res)
        data_length = len(content[0]['Data'])
        for j in range(data_length):
            print((i - 1) * size + j + 1, ' Done!')
            df.loc[df.shape[0]] = pd.Series(content[0]['Data'][j])
    df.to_csv('data.csv')
