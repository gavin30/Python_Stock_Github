#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.cmdline import execute

def GOGO():
    execute(['scrapy', 'crawl', 'news'])

if __name__ == "__main__":
    GOGO()


"""
# main 函数的学习:

def main():
    print "we are in %s"%__name__

if __name__ == '__main__':
    main()
"""
