# -*- coding: utf-8 -*-
"""
@author: davidfnck
## the main idea:

1. 基于新闻内容,进行关键词匹配,找到最近的热点股票(需匹配股票的代码)
2.　对热点股票进行财务分析
3.　推荐股票并发送邮件或者短信


## python version:

>　开始使用的是 Python2.7, 为了结合 Scrapy, 修改成了 Python 3.5, 主要修改点包括:

1. Print()
2. reload 函数应该是跟编码有关,猜测。注释掉即可
3. 安装相关 Packages

## the　big　problems:

>　基本解决方案都在对应的函数下面,重点问题会拿到这里,保持代码的纯净

##　to　do　lists:　还要去实现的一些想法

1.　结合　Scrapy　爬虫,自动删除　Mongodb　中的数据,爬取新的数据进行分析
2.　


"""

import pandas as pd
from pymongo import MongoClient
import re
from datetime import datetime, timedelta
from dateutil.parser import parse
# import pandas as pd
import sys
# from sqlalchemy import create_engine, MetaData, Table, select


def _connect_mongo(host, port, username, password, db):
    """ A util for making a connection to mongo """

    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)


    return conn[db]


def read_mongo(db, collection, query={}, host='localhost', port=27017, username=None, password=None, no_id=True):
    """ Read from Mongo and Store into DataFrame """

    # Connect to MongoDB
    db = _connect_mongo(host=host, port=port, username=username, password=password, db=db)

    # Make a query to the specific DB and Collection
    cursor = db[collection].find(query)

    # Expand the cursor and construct the DataFrame
    df =  pd.DataFrame(list(cursor))

    # Delete the _id
    if no_id:
        del df['_id']

    return df

# 清空 MongoDB
def delete_mongo(db, collection, query={}, host='localhost', port=27017, username=None, password=None, no_id=True):

    # Connect to MongoDB
    db = _connect_mongo(host=host, port=port, username=username, password=password, db=db)

    # Make a query to the specific DB and Collection
    cursor = db[collection].drop()


delete_mongo('NewsDB','news',{},'127.0.0.1',27017)


# 运行爬虫 Scrapy news
# from news import ProcessRun
# ProcessRun

import os
# 必须先加载项目settings配置
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'news.settings')
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
process = CrawlerProcess(get_project_settings())
# 指定多个spider
process.crawl("news")
# process.crawl("favorite_spider")
# 执行所有 spider
for spider_name in process.spider_loader.list():
    # print spider_name
    process.crawl(spider_name)
process.start()


# 读取数据
df = read_mongo('NewsDB','news',{},'127.0.0.1',27017)
pd.set_option('expand_frame_repr', False)
pd.set_option('max_colwidth', 100)



# 正则提取时间,但是还是字符串
# pattern = re.compile(r"\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d")
# pattern = re.compile(r"^\d{4}(-\d\d){2}(-\d\d){2} \d\d(:\d\d){2}")
# pattern = re.compile(r"\d{4}(-\d\d){2}(-\d\d){2}  \d\d:\d\d:\d\d")
# df['news_time'] = df['news_time'].str[0]
# df['news_time'] = df['news_time'].str.split()
# df['news_time'] = df['news_time'].str[0]
# df['news_time'] = df['news_time'].str.findall(pattern)

# 老师提供方案
# df['news_time'] = df['news_time'].astype(str)
# df['news_time'] = df['news_time'].str[1:-1]
# df['news_time'] = df['news_time'].map(lambda x:eval(x))
# print df['news_time']

# 将时间字符串转换成时间格式
# df['news_time'] = pd.to_datetime(df['news_time'])

# 排序
# df.reset_index(inplace=True)
# df = df.sort_values(by=['news_time'], ascending=0)

# 将 index 设置成时间
# df.index = df['news_time']
# df.drop(['news_time'], axis=1, inplace=True)

# 除去包含空值的一条数据
df = df.dropna()

# 拼接新闻内容
for i in df.index:
    df['news_body'][i] = ''.join(df['news_body'][i])


# 以下出现编码问题。
# 操作 pandas,进行文本分析
import jieba
import jieba.analyse
#
# jieba.set_dictionary('/Users/davidfnck/Downloads/Python_Learning/jieba_python/dict.txt.big')
#
# content = open('/Users/davidfnck/Downloads/Python_Learning/jieba_python/lianghua_01.txt', 'rb').read()
# print("Input：", content)
# df['news_body'] = df['news_body'].astype(str)
# df['news_body'] = df['news_body']
try:
    df['news_body'] = [i.encode('utf8') for i in df['news_body']]
    # df['news_title'] = [i.encode('utf8') for i in df['news_title']]
except:
    # print 'Something Wrong'
    print('Something Wrong')  # Python3.5


import sys
from functools import wraps

# reload(sys)  # 仅限Python 2.7
# sys.setdefaultencoding("utf-8")  # 仅限Python 2.7

# setence=sys.argv[1]

# 基础词库以 Sogou 股票词为基础
stocks = ''
with open('/Users/davidfnck/Downloads/Python_Stock_Github/news_anlysis/stock_data/allstocks.txt','r') as f:
    for line in f:
        stocks += line
        # print(stocks)
        # continue

jieba.set_dictionary('/Users/davidfnck/Downloads/Python_Stock_Github/news_anlysis/dict.txt.big')

x = -1
while x < df.index[-1]:
    for content in df['news_body']:
        x = x + 1
        try:
            tags = jieba.analyse.extract_tags(content, 1)
            # print("Output：")
            # print(",".join(tags))
        except:
            # print 'Something Wrong'
            print('Something Wrong')  # Python3.5
        else:
            for i in tags:
                if i in stocks:
                    # print i,df['news_url'][x]
                    print(i,df['news_url'][x])
