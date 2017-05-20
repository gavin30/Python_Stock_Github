# -*- coding: utf-8 -*-
"""
@author: davidfnck
date: 2017年05月17日
择时策略框架的主函数
"""

import pandas as pd
import Signals
import Timing_Functions
#　目前遇到的问题就是导入自己的文件夹的时候不正确
from program import Functions  # 或者 import program.Functions
# import program.Functions as Functions
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行


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
df[[i + '_' + fuquan_type for i in '开盘价', '最高价', '最低价', '收盘价']] = Functions.cal_fuquan_price(df, fuquan_type)

# ===== 第二个模块:产生交易信号
# === 根据均线策略产生交易信号
df = Signals.signal_ma(df, ma_short=5, ma_long=50)


# =====  第三个模块: 根据交易信号计算每天的仓位
# ===计算仓位
df = Timing_Functions.position(df)

# == 截取上市一年之后的交易日
df = df.iloc[250-1:]  # 为什么是250-1?
# 将第一天的仓位设置为 0
df.iloc[0, -1] = 0

# ===== 第四个模块: 根据仓位计算资金曲线
# === 简单方式
print Timing_Functions.equity_curve_simple(df)

# === 实际方式
df = df[['交易日期','股票代码','开盘价','最高价','最低价','收盘价','涨跌幅','pos']]
df.reset_index(inplace=True, drop=True)
df = Timing_Functions.equity_curve(df, initial_money=1000000, slippage=0.01, c_rate=5.0/10000, t_rate=1.0/1000)

print df
exit()