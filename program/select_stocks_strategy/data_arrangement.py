# -*- coding: utf-8

"""
@author: davidfnck
date: 2017年6月20日
本段程序用于生成选股策略所需要的数据
"""

import pandas as pd
from program import config
from program import Functions
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行

# ==读取所有股票代码的列表
stock_code_list = Functions.get_stock_code_list_in_one_dir(config.input_data_path+'/stock_data')
stock_code_list = stock_code_list[:20]
print stock_code_list
exit()




