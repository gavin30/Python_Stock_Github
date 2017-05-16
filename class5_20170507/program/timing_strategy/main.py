# -*- coding: utf-8 -*-
"""
@author: davidfnck
date: 2017年05月17日
择时策略框架的主函数
"""

import pandas as pd
# import Signals

#　目前遇到的问题就是导入自己的文件夹的时候不正确

from program import Functions  # 或者 import program.Functions

pd.set_option('expand_frame_repr', False)　# 当列太多时不换行


# ===== 第一个模块: 数据准备
# === 读入数据
code = 'sz300001'
df = Functions.import_stock_data(code)
# 判断股票上市是否满一定时间,如果不满足,则不运行策略
if df.shape[0] < 250:
    print '股票上市未满一年,不运行策略'
    exit()


# === 计算复权价
fuquan_type = '后复权'
df[[i + '_' + fuquan_type for i in '开盘价', '最高价', '最低价', '', '', '', '', '']]
