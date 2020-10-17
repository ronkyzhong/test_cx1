# -*- coding: utf-8 -*-
# @Time    : 2020/9/2 14:25
# @Author  : jiashu.zhong
# @Site    : 
# @File    : test_option.py
import re

import yaml

from business.about_money_and_share import GetMoneyAndShare

asset_account_id = 2800004626
moneyAndShare = GetMoneyAndShare()

with open("../datas/stock_price.yaml") as f:
    datas = yaml.safe_load(f)

def test_option_share():
    """
    返回期权持仓数据
    {'IBM   210115C00080000': {'available_share': 2, 'book_balance': -2, 'position_status': 2, 'stock_code': 'IBM', 'strike_price': 80.0}}
    :return:
    """
    ## 获取期权持仓信息
    option_shares = moneyAndShare.get_account_holding(asset_account_id)[0]
    for key, option_share in option_shares.items():
        stock_code = re.match(r'\w+\w', key).group(0)
        strike_price = int(re.search('\d{8}$', key).group(0)) / 1000
        option_share['stock_code'] = stock_code
        option_share['strike_price'] = strike_price
    print(datas)
    print('\n', option_shares)
    return option_shares

