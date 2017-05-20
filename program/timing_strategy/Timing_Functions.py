# -*- coding: utf-8 -*-
"""
@author: davidfnck
date: 2017年05月20日
汇总择时策略需要用到的一些常见函数
"""


# 根据交易信号,计算每天的仓位
def position(df):
    """
    根据交易信号, 计算每天的仓位
    :param df:
    :return:
    """
    # 由 signal 计算出实际每天持有的股票仓位
    df['pos'] = df['signal'].shift(1)
    df['pos'].fillna(method='ffill', inplace=True)

    # 将涨跌停时不得买卖股票考虑进来
    # 找出开盘涨停的日期
    cond_cannot_buy = df['开盘价'] > df['收盘价'].shift(1) * 1.097  # 今天的开盘价相对于昨天的收盘价上涨了 9.7%
    # 将开盘涨停日, 并且当天 position 为 1 时的 'pos' 设置为空值
    # ?? 问题:为什么是 1?
    df.loc[cond_cannot_buy & (df['pos'] == 1), 'pos'] = None

    # 找出开盘跌停的日期
    cond_cannot_buy = df['开盘价'] < df['收盘价'].shift(1) * 0.903  # 今天的开盘价相对于昨天的收盘价下跌了 9.7%
    # 将开盘跌停日, 并且当天 position 为 0 时的 'pos' 设置为空值
    # ?? 问题:为什么是 0?
    df.loc[cond_cannot_buy & (df['pos'] == 0), 'pos'] = None

    # position 为空的日期, 不能买卖。position 只能和前一个交易日保持一致。
    df['pos'].fillna(method='ffill', inplace=True)

    # 在 position 为空值的日期, 将 position 补全为 0
    df['pos'].fillna(value=0, inplace=True)

    return df

# 计算资金曲线, 简单版本
def equity_curve_simple(df):
    """
    最简单的计算资金曲线的方式, 与实际不符合
    :param df:
    :return:
    """

    # === 计算实际资金曲线
    # 当当天空仓时, pos 为 0, 资产涨幅为0
    # 当当天满仓时, pos 为 1, 资产涨幅为股票本身的涨跌幅
    df['equity_change'] = df['涨跌幅'] * df['pos']
    # 根据每天的涨跌幅计算资金曲线
    df['equity_curve'] = (df['equity_change'] +1).cumprod()

    return df

# 计算资金曲线, 稍复杂版本
def equity_curve(df, initial_money=1000000, slippage=0.01, c_rate=5.0/10000, t_rate=1.0/1000):
    """
    :param df:
    :param initial_money: 初始资金, 默认为 1,000,000元
    :param slippage: 滑点, 默认为 0.01 元
    :param c_rate: 手续费, commission fees, 默认为万分之 5
    :param t_rate: 印花税, tax, 默认为千分之 1
    :return:
    """

    # === 第一天的情况
    df.at[0, 'hold_num'] = 0  # 持有股票数量
    df.at[0, 'stock_value'] = 0  # 持仓股票市值
    df.at[0, 'actual_pos'] = 0  # 每日的实际仓位
    df.at[0, 'cash'] = initial_money  # 持有现金
    df.at[0, 'equity'] = initial_money # 总资产 = 持有股票市值 + 现金

    # === 第一天之后每天的情况
    for i in range(1, df.shape[0]):

        # 前一天只有的股票的数量
        hold_num = df.at[i -1, 'hold_num']

        # 若发生除权, 需要调整 hold_num
        if abs((df.at[i, '收盘价'] / df.at[i -1, '收盘价'] -1)- df.at[i, '涨跌幅']) > 0.001:
            stock_value = df.at[i-1, 'stock_value']
            last_price = df.at[i, '收盘价'] / (df.at[i, '涨跌幅'] + 1)
            hold_num = stock_value / last_price
            hold_num = int(hold_num)

        # 判断是否需要调整仓位
        # 需要调整仓位
        if df.at[i, 'pos'] != df.at[i-1, 'pos']:

            # 昨天的总资产 * 今天的仓位 / 今天的收盘价, 得到需要持有的股票数
            theory_num = df.at[i-1, 'equity'] * df.at[i, 'pos'] / df.at[i, '开盘价']
            # 对需要持有的股票数取整
            theory_num = int(theory_num)  # 向下取整

            # 判断加仓还是减仓
            # 加仓
            if theory_num >= hold_num:
                # 计算实际需要买入的股票数量
                buy_num = theory_num - hold_num
                # 买入股票只能整百, 对 buy_num 进行向下取整百
                buy_num = int(buy_num / 100) * 100

                # 计算买入股票花去的现金
                buy_cash = buy_num * (df.at[i, '开盘价'] + slippage)
                # 计算买入股票花去的手续费, 并保留 2 位小数
                commission = round(buy_cash * c_rate, 2)
                # 不足 5 元按 5 元收
                if commission < 5 and commission != 0:
                    commission = 5
                df.at[i, '手续费'] = commission

                # 计算当天收盘时持有股票的数量和现金
                df.at[i, 'hold_num'] = hold_num + buy_num  # 持有股票
                df.at[i, 'cash'] = df.at[i-1, 'cash'] - buy_cash - commission

            # 减仓
            else:
                # 计算卖出股票数量, 卖出股票可以不是整数, 不需要取整百。
                sell_num = hold_num - theory_num

                # 计算卖出股票得到的现金
                sell_cash = sell_num * (df.at[i, '开盘价'] - slippage)
                # 计算手续费, 不足 5 元按 5 元收并保留 2 位小数
                commission = round(max(sell_cash * c_rate, 5), 2)
                df.at[i, '手续费'] = commission
                # 计算印花税, 保留 2 位小数。历史上有段时间, 买入也会收取印花税
                tax = round(sell_cash * t_rate, 2)
                df.at[i, '印花税'] = tax

                # 计算当天收盘时持有股票的数量和现金
                df.at[i, 'hold_num'] = hold_num - sell_num  # 持有股票
                df.at[i, 'cash'] = df.at[i - 1, 'cash'] + sell_cash - commission - tax  # 剩余现金

        # 不需要调仓
        else:
            # 计算当天收盘时持有股票的数量和现金
            df.at[i, 'hold_num'] = hold_num  # 持有股票
            df.at[i, 'cash'] = df.at[i - 1, 'cash']  # 剩余现金


        # 计算当天的各种数据
        df.at[i, 'stock_value'] = df.at[i, 'hold_num'] * df.at[i, '收盘价']  # 剩余现金
        df.at[i, 'equity'] = df.at[i, 'cash'] + df.at[i, 'stock_value']  # 总资产
        df.at[i, 'actual_pos'] = df.at[i, 'stock_value'] / df.at[i, 'equity']  # 实际仓位

    return df