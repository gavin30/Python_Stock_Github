# -*- coding: utf-8 -*-
"""
@author: davidfnck
date: 2017年05月17日
择时策略框架的主函数
"""

import config  # 导入 config, 在同一级目录下,直接 import
import pandas as pd  # 导入 pandas, 我们一般为 pandas 取一个别名叫做 pd


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

