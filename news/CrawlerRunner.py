#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

参考资料:http://blog.leanote.com/post/dapingxia@163.com/Python%E7%88%AC%E8%99%AB%E8%BF%9B%E9%98%B63%E4%B9%8BScrapy%E8%BF%90%E8%A1%8C%E5%A4%9A%E4%B8%AASpiders-2

但是我没成功,不知道为什么。

"""


import os
# 必须先加载项目settings配置
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'news.settings')
import scrapy
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
runner = CrawlerRunner(get_project_settings())
# 运行单个时
d = runner.crawl("news")
# 运行多个时
#runner.crawl("board_spider")
#runner.crawl("favorite_spider")
#d = runner.join()
# 运行所有时
for spider_name in runner.spider_loader.list():
    runner.crawl(spider_name)
d = runner.join()
d.addBoth(lambda _: reactor.stop())
reactor.run()
