# -*- coding: utf-8 -*-
"""
@author: davidfnck
date: 2017年05月17日
择时策略框架的主函数
"""

import pandas as pd  # 导入 pandas, 我们一般为 pandas 取一个别名叫做 pd
import config  # 导入 config, 在同一级目录下,直接 import
import os
import urllib2
import time
import datetime


# 导入数据
def import_stock_data(stock_code):
    """
    只导入如下字段: '交易日期', '股票代码', '开盘价', '最高价', '最低价', '收盘价', '涨跌幅'
    最终输出结果按照日期排序
    :param stock_code:
    :return:
    """
    df = pd.read_csv(config.input_data_path + '/stock_data/' + stock_code + '.csv', encoding='gbk')
    df.columns = [i.encode('utf8') for i in df.columns]
    df = df[['交易日期', '股票代码', '开盘价', '最高价', '最低价', '收盘价', '涨跌幅']]
    df.sort_values(by=['交易日期'], inplace=True)
    df['交易日期'] = pd.to_datetime(df['交易日期'])
    df.reset_index(inplace=True, drop=True)

    return df

# 计算复权价
# 在课程 4 月 23 日下午(2) 里面有
def cal_fuquan_price(input_stock_data, fuquan_type='后复权'):
    """
    计算复权价
    :param input_stock_data:
    :param fuquan_type:复权类型, 可以是'后复权'或者'前复权'
    :return:
    """

    # 创建空的df
    df = pd.DataFrame()

    # 计算复权收盘价
    num = {'后复权': 0, '前复权': -1}
    price1 = input_stock_data['收盘价'].iloc[num[fuquan_type]]
    df['复权因子'] = (1.0 + input_stock_data['涨跌幅']).cumprod()
    price2 = df['复权因子'].iloc[num[fuquan_type]]
    df['收盘价_' + fuquan_type] = df['复权因子'] *(price1 / price2)

    # 计算复权的开盘价、最高价、最低价
    df['开盘价_' + fuquan_type] = input_stock_data['开盘价'] / input_stock_data['收盘价'] * df['收盘价_' + fuquan_type]
    df['最高价_' + fuquan_type] = input_stock_data['最高价'] / input_stock_data['收盘价'] * df['收盘价_' + fuquan_type]
    df['最低价_' + fuquan_type] = input_stock_data['最低价'] / input_stock_data['收盘价'] * df['收盘价_' + fuquan_type]

    return df[[i + '_' + fuquan_type for i in '开盘价','最高价','最低价','收盘价']]

# 导入某文件夹下的所有股票代码
def get_stock_code_list_in_one_dir(path):
    """
    从指定文件夹下,导入所有 csv 文件的文件名
    :param path:
    :return:
    """

    stock_list = []

    #系统自带函数 os.walk, 用于遍历文件夹中的所有文件
    for root, dirs, files in os.walk(path):
        if files:  # 当 files 不为空的时候
            for f in files:
                if f.endswith('.csv'):
                    stock_list.append(f[:8])

    return stock_list
