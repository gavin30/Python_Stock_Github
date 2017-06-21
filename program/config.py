# -*- coding: utf-8 -*-
"""
@author: davidfnck
date: 2017年05月17日
择时策略框架的主函数
"""

import os

# 获取当前程序的地址
current_file = __file__

# 程序根目录地址, os.pardir: 父目录
root_path = os.path.abspath(os.path.join(current_file, os.pardir, os.pardir))

# 输入数据根目录地址
input_data_path = os.path.abspath(os.path.join(root_path, 'data', 'input_data'))

# 输出数据根目录地址
output_data_path = os.path.abspath(os.path.join(root_path, 'data', 'output_data'))

# # 当前路径
print os.path.abspath('.')
# # 父辈路径
print os.path.abspath('..')
