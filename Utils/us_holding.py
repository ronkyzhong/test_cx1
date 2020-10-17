# -*- coding: utf-8 -*-
# @Time    : 2020/9/28 18:41
# @Author  : jiashu.zhong
# @Site    : 
# @File    : us_holding.py
import logging
import random
import string
import time

import yaml
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s  %(message)s ')
# 声明了一个 Log 对象
log = logging.getLogger(__name__)
us_holding_sql_list = []
adjust_data = {}
positions = []

with open("../datas/stock_share.yaml", encoding='utf-8') as f:
    datas = yaml.safe_load(f)
for key, data in datas.items():
    share_dict = dict()
    share_dict[data['SYMBOL']] = {
        key: data['SETTLE_QUANTITY'] + data['SETTLE_T1_QUANTITY'] + data['SETTLE_T2_QUANTITY'] + data[
            'SETTLE_TN_QUANTITY'],
        'BRANCH_ID': data['BRANCH_ID'],
        'ACCOUNT_OWNER_ID': data['ACCOUNT_OWNER_ID'],
        'ASSET_ACCOUNT_ID': data['ASSET_ACCOUNT_ID'],
        'HOLDER_ID': data['HOLDER_ID'],
        'SYMBOL': data['SYMBOL'],
        'SECURITY_ID': data['SECURITY_ID'],
        'SECURITY_NAME': data['SECURITY_NAME'],
        'SETTLE_QUANTITY': data['SETTLE_QUANTITY'],
        'SETTLE_T1_QUANTITY': data['SETTLE_T1_QUANTITY'],
        'SETTLE_T2_QUANTITY': data['SETTLE_T2_QUANTITY'],
        'SETTLE_TN_QUANTITY': data['SETTLE_TN_QUANTITY'],
        'price': data['price']}
    positions.append(share_dict)
for index, value in enumerate(positions):
    for k, v in value.items():
        positions[index - 1].get(k)
        adjust_data[k] = [v, positions[index - 1].get(k)]

def test_us_holding():
    num = 1
    for key,value in adjust_data.items():
        create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        update_time = create_time
        id = random.randint(900000000, 999999999)
        VERIFY_MD5 = ''.join(random.sample(string.ascii_letters + string.digits, 32))
        # done current_share,settle_t1_share,settle_t2_share,holding_balance_share,need_settle_in_from_party
        current_share = value[0][f'marginShortPositive{num}'] + value[1][f'marginLongPositive{num}']
        holding_balance_share = value[0]['SETTLE_QUANTITY'] + value[1]['SETTLE_QUANTITY']
        need_settle_in_from_party = value[0]['SETTLE_T1_QUANTITY'] + value[1]['SETTLE_T1_QUANTITY'] + value[0]['SETTLE_T2_QUANTITY'] + value[1]['SETTLE_T2_QUANTITY'] + value[0]['SETTLE_TN_QUANTITY'] + value[1]['SETTLE_TN_QUANTITY']
        settle_t1_share = value[0]['SETTLE_T1_QUANTITY'] + value[1]['SETTLE_T1_QUANTITY']
        settle_t2_share =  value[0]['SETTLE_T2_QUANTITY'] + value[1]['SETTLE_T2_QUANTITY']
        if value[1]['BRANCH_ID']==33:
        # todo us_holding total_buy_amount,total_buy_qty,total_sell_amount,total_sell_qty
            if value[1]['SETTLE_QUANTITY']>=0 and value[1]['SETTLE_T1_QUANTITY']>=0 and value[1]['SETTLE_T2_QUANTITY']>=0:
                total_buy_qty = value[1]['SETTLE_QUANTITY'] + value[1]['SETTLE_T1_QUANTITY'] + value[1]['SETTLE_T2_QUANTITY']
                total_sell_qty = 0
                total_buy_amount = total_buy_qty * value[1]['price']
                total_sell_amount = 0
            elif value[1]['SETTLE_QUANTITY']>=0 and value[1]['SETTLE_T1_QUANTITY']>=0 and value[1]['SETTLE_T2_QUANTITY']<0:
                total_buy_qty = value[1]['SETTLE_QUANTITY'] + value[1]['SETTLE_T1_QUANTITY']
                total_sell_qty = abs(value[1]['SETTLE_T2_QUANTITY'])
                total_buy_amount = total_buy_qty * value[1]['price']
                total_sell_amount = total_sell_qty * value[1]['price']
            elif value[1]['SETTLE_QUANTITY']>=0 and value[1]['SETTLE_T1_QUANTITY']<0 and value[1]['SETTLE_T2_QUANTITY']<0:
                total_buy_qty = value[1]['SETTLE_QUANTITY']
                total_sell_qty =  abs(value[1]['SETTLE_T1_QUANTITY'] + value[1]['SETTLE_T2_QUANTITY'])
                total_buy_amount = total_buy_qty * value[1]['price']
                total_sell_amount = total_sell_qty * value[1]['price']
            elif value[1]['SETTLE_QUANTITY'] >= 0 and value[1]['SETTLE_T1_QUANTITY'] < 0 and value[1]['SETTLE_T2_QUANTITY'] >= 0:
                total_buy_qty = value[1]['SETTLE_QUANTITY'] + value[1]['SETTLE_T2_QUANTITY']
                total_sell_qty = abs(value[1]['SETTLE_T1_QUANTITY'])
                total_buy_amount = total_buy_qty * value[1]['price']
                total_sell_amount = total_sell_qty * value[1]['price']
            elif value[1]['SETTLE_QUANTITY'] < 0 and value[1]['SETTLE_T1_QUANTITY'] < 0 and value[1]['SETTLE_T2_QUANTITY'] >= 0:
                total_buy_qty =  value[1]['SETTLE_T2_QUANTITY']
                total_sell_qty = abs(value[1]['SETTLE_QUANTITY'] + value[1]['SETTLE_T1_QUANTITY'])
                total_buy_amount = total_buy_qty * value[1]['price']
                total_sell_amount = total_sell_qty * value[1]['price']
            elif value[1]['SETTLE_QUANTITY'] < 0 and value[1]['SETTLE_T1_QUANTITY'] >= 0 and value[1]['SETTLE_T2_QUANTITY'] >= 0:
                total_buy_qty =  value[1]['SETTLE_T1_QUANTITY'] + value[1]['SETTLE_T2_QUANTITY']
                total_sell_qty = abs(value[1]['SETTLE_QUANTITY'])
                total_buy_amount = total_buy_qty * value[1]['price']
                total_sell_amount = total_sell_qty * value[1]['price']
            elif value[1]['SETTLE_QUANTITY'] < 0 and value[1]['SETTLE_T1_QUANTITY'] >= 0 and value[1]['SETTLE_T2_QUANTITY'] < 0:
                total_buy_qty = value[1]['SETTLE_T1_QUANTITY']
                total_sell_qty = abs(value[1]['SETTLE_QUANTITY'] + value[1]['SETTLE_T2_QUANTITY'])
                total_buy_amount = total_buy_qty * value[1]['price']
                total_sell_amount = total_sell_qty * value[1]['price']
            else:
                total_buy_qty = 0
                total_sell_qty = abs(value[1]['SETTLE_QUANTITY'] + value[1]['SETTLE_T1_QUANTITY'] + value[1]['SETTLE_T2_QUANTITY'])
                total_buy_amount = 0
                total_sell_amount = total_sell_qty * value[1]['price']
        if value[0]['BRANCH_ID']==34:
            # todo us_holding short_total_buy_amount,short_total_buy_qty,short_total_sell_amount,short_total_sell_qty
            if value[0]['SETTLE_QUANTITY']>=0 and value[0]['SETTLE_T1_QUANTITY']>=0 and value[0]['SETTLE_T2_QUANTITY']>=0:
                short_total_buy_qty = value[0]['SETTLE_QUANTITY'] + value[0]['SETTLE_T1_QUANTITY'] + value[0]['SETTLE_T2_QUANTITY']
                short_total_sell_qty = 0
                short_total_buy_amount = short_total_buy_qty * value[0]['price']
                short_total_sell_amount = 0
            elif value[0]['SETTLE_QUANTITY']>=0 and value[0]['SETTLE_T1_QUANTITY']>=0 and value[0]['SETTLE_T2_QUANTITY']<0:
                short_total_buy_qty = value[0]['SETTLE_QUANTITY'] + value[0]['SETTLE_T1_QUANTITY']
                short_total_sell_qty = abs(value[0]['SETTLE_T2_QUANTITY'])
                short_total_buy_amount = short_total_buy_qty * value[0]['price']
                short_total_sell_amount = short_total_sell_qty * value[0]['price']
            elif value[0]['SETTLE_QUANTITY']>=0 and value[0]['SETTLE_T1_QUANTITY']<0 and value[0]['SETTLE_T2_QUANTITY']<0:
                short_total_buy_qty = value[0]['SETTLE_QUANTITY']
                short_total_sell_qty =  abs(value[0]['SETTLE_T1_QUANTITY'] + value[0]['SETTLE_T2_QUANTITY'])
                short_total_buy_amount = short_total_buy_qty * value[0]['price']
                short_total_sell_amount = short_total_sell_qty * value[0]['price']
            elif value[0]['SETTLE_QUANTITY'] >= 0 and value[0]['SETTLE_T1_QUANTITY'] < 0 and value[0]['SETTLE_T2_QUANTITY'] >= 0:
                short_total_buy_qty = value[0]['SETTLE_QUANTITY'] + value[0]['SETTLE_T2_QUANTITY']
                short_total_sell_qty = abs(value[0]['SETTLE_T1_QUANTITY'])
                short_total_buy_amount = short_total_buy_qty * value[0]['price']
                short_total_sell_amount = short_total_sell_qty * value[0]['price']
            elif value[0]['SETTLE_QUANTITY'] < 0 and value[0]['SETTLE_T1_QUANTITY'] < 0 and value[0]['SETTLE_T2_QUANTITY'] >= 0:
                short_total_buy_qty =  value[0]['SETTLE_T2_QUANTITY']
                short_total_sell_qty = abs(value[0]['SETTLE_QUANTITY'] + value[0]['SETTLE_T1_QUANTITY'])
                short_total_buy_amount = short_total_buy_qty * value[0]['price']
                short_total_sell_amount = short_total_sell_qty * value[0]['price']
            elif value[0]['SETTLE_QUANTITY'] < 0 and value[0]['SETTLE_T1_QUANTITY'] >= 0 and value[0]['SETTLE_T2_QUANTITY'] >= 0:
                short_total_buy_qty =  value[0]['SETTLE_T1_QUANTITY'] + value[0]['SETTLE_T2_QUANTITY']
                short_total_sell_qty = abs(value[0]['SETTLE_QUANTITY'])
                short_total_buy_amount = short_total_buy_qty * value[0]['price']
                short_total_sell_amount = short_total_sell_qty * value[0]['price']
            elif value[0]['SETTLE_QUANTITY'] < 0 and value[0]['SETTLE_T1_QUANTITY'] >= 0 and value[0]['SETTLE_T2_QUANTITY'] < 0:
                short_total_buy_qty = value[0]['SETTLE_T1_QUANTITY']
                short_total_sell_qty = abs(value[0]['SETTLE_QUANTITY'] + value[0]['SETTLE_T2_QUANTITY'])
                short_total_buy_amount = short_total_buy_qty * value[0]['price']
                short_total_sell_amount = short_total_sell_qty * value[0]['price']
            else:
                short_total_buy_qty = 0
                short_total_sell_qty = abs(value[0]['SETTLE_QUANTITY'] + value[0]['SETTLE_T1_QUANTITY'] + value[0]['SETTLE_T2_QUANTITY'])
                short_total_buy_amount = 0
                short_total_sell_amount = short_total_sell_qty * value[0]['price']

        us_holding_sql = f"INSERT INTO hsdc.us_holding (id, account_owner_id, account_owner_code, asset_account_id, asset_account_code, holder_id, holder_code, symbol, security_id, security_name, currency, holding_balance_share, inflated_share, trade_freeze_balance_share, today_trade_buy_share, today_trade_sell_share, other_freeze_balance_share, law_freeze_balance_share, balance_share_cost_price, status, verify_md5, flag_bit, features, create_time_utc, update_time_utc, need_settle_in_from_party, current_share, total_sell_amount, total_buy_amount, total_sell_qty, total_buy_qty, version, break_even_price, total_sell_fee, total_buy_fee, break_even_price_from_settle, view_status_bit, short_total_buy_amount, short_total_sell_amount, short_total_sell_qty, short_total_buy_qty, short_total_sell_fee, short_total_buy_fee, security_type, trade_platform, settle_t1_share, settle_t2_share, long_pre_open_share, short_pre_open_share, short_pre_close_share, position_status, custodian_id) " \
            f"values ({id},{value[0]['ACCOUNT_OWNER_ID']},0, {value[0]['ASSET_ACCOUNT_ID']},0,{value[0]['HOLDER_ID']},0,'{value[0]['SYMBOL']}',{value[0]['SECURITY_ID']},'{value[0]['SECURITY_NAME']}',4,{holding_balance_share},0,0,0,0,0,0,{value[0]['price']},0,'{VERIFY_MD5}',0,'{{}}','{create_time}','{update_time}','{need_settle_in_from_party}', '{current_share}', {total_sell_amount},{total_buy_amount}, {total_sell_qty}, {total_buy_qty}, 1, {value[0]['price']}, 0, 0, {value[0]['price']}, 0, '{short_total_buy_amount}', {short_total_sell_amount}, {short_total_sell_qty}, {short_total_buy_qty},0, 0, 32, 5, {settle_t1_share}, {settle_t2_share}, 0, 0, 0, 1, 39)"
        us_holding_sql_list.append(us_holding_sql)
        num += 1
    log.info(f"=================:{us_holding_sql_list}")
    return us_holding_sql_list
