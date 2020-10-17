# -*- coding: utf-8 -*-
# @Time    : 2020/9/15 19:52
# @Author  : jiashu.zhong
# @Site    : 
# @File    : test_create_data.py
"""

INSERT INTO hsdc.us_branch_detail_holding
 (ID,ACCOUNT_OWNER_ID,ACCOUNT_OWNER_CODE,ASSET_ACCOUNT_ID,ASSET_ACCOUNT_CODE,HOLDER_ID,HOLDER_CODE,MARKET,SECURITY_ID,SYMBOL,SECURITY_NAME,CUSTODIAN_ID,CUSTODIAN_NAME,BRANCH_ID,BRANCH_NAME,REGISTER_TYPE,SETTLE_QUANTITY,SETTLE_T1_QUANTITY,SETTLE_T2_QUANTITY,SETTLE_TN_QUANTITY,SETTLE_OVERDUE_QUANTITY,VERIFY_MD5,CREATE_TIME_UTC,UPDATE_TIME_UTC)
 values (999999999,110012278,0, 2800004626,0,2800004626,0, 2, 60409,'IBM   210115C00080000', 'IBM   210115C00080000',39,'IB',33,'Margin Long',1,1, 9,2,3,0,'dasdas321321asdasd','2020-08-05 14:05:18:500000','2020-08-05 14:05:18:500000'
);
"""
import random
import string
import time

import yaml
from Utils.connect_oracle import ConnectOracle
from Utils.us_holding import test_us_holding

connect = ConnectOracle()
with open("../datas/stock_share.yaml") as f:
    data = yaml.safe_load(f)
    asset_account_id =  tuple([i['ASSET_ACCOUNT_ID']for i in data.values()])
    select_us_branch_detail_holding_sql = f'select * from hsdc.us_branch_detail_holding a where a.asset_account_id in {asset_account_id} and id >900000000'
    del_us_branch_detail_holding_sql = f'delete from hsdc.us_branch_detail_holding a where a.asset_account_id in {asset_account_id} and id >900000000'
    symbol = tuple(set(([i['SYMBOL']for i in data.values()])))
    select_us_branch_total_holding_sql = f'select * from hsdc.us_branch_total_holding a where a.symbol in {symbol}'
    del_us_branch_total_holding_sql = f'delete from hsdc.us_branch_total_holding a where a.symbol in {symbol}'
    select_us_holding_sql = f'select * from hsdc.us_holding a where a.asset_account_id in {asset_account_id} and id >900000000'
    del_us_holding_sql = f'delete from hsdc.us_holding a where a.asset_account_id in {asset_account_id} and id >900000000'
def test_insert_into_us_branch_detail_holding():
    branch_detail_sql_list = []
    branch_total_sql_list = []
    us_holding_sql_list = test_us_holding()
    for key, value in data.items():
        create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        update_time = create_time
        id = random.randint(900000000, 999999999)
        VERIFY_MD5 = ''.join(random.sample(string.ascii_letters + string.digits, 32))
        branch_detail_sql = f"INSERT INTO hsdc.us_branch_detail_holding " \
            f"(ID,ACCOUNT_OWNER_ID,ACCOUNT_OWNER_CODE,ASSET_ACCOUNT_ID,ASSET_ACCOUNT_CODE,HOLDER_ID,HOLDER_CODE,MARKET,SECURITY_ID,SYMBOL,SECURITY_NAME,CUSTODIAN_ID,CUSTODIAN_NAME,BRANCH_ID,BRANCH_NAME,REGISTER_TYPE,SETTLE_QUANTITY,SETTLE_T1_QUANTITY,SETTLE_T2_QUANTITY,SETTLE_TN_QUANTITY,SETTLE_OVERDUE_QUANTITY,VERIFY_MD5,CREATE_TIME_UTC,UPDATE_TIME_UTC)" \
            f" values ({id},{value['ACCOUNT_OWNER_ID']},0, {value['ASSET_ACCOUNT_ID']},0,{value['HOLDER_ID']},0, 2, {value['SECURITY_ID']},'{value['SYMBOL']}', '{value['SECURITY_NAME']}',39,'IB',{value['BRANCH_ID']},'{value['BRANCH_NAME']}',{value['REGISTER_TYPE']},{value['SETTLE_QUANTITY']}, {value['SETTLE_T1_QUANTITY']}, {value['SETTLE_T2_QUANTITY']},{value['SETTLE_TN_QUANTITY']},0,'{VERIFY_MD5}','{create_time}','{update_time}')"
        branch_detail_sql_list.append(branch_detail_sql)

        branch_total_sql = f"INSERT INTO hsdc.us_branch_total_holding (ID,MARKET,SECURITY_ID,SYMBOL,SECURITY_NAME,CUSTODIAN_ID,CUSTODIAN_NAME,BRANCH_ID,BRANCH_NAME,SETTLE_QUANTITY,SETTLE_T1_QUANTITY,SETTLE_T2_QUANTITY,SETTLE_TN_QUANTITY,SETTLE_OVERDUE_QUANTITY,VERIFY_MD5,FLAG_BIT,FEATURES,CREATE_TIME_UTC,UPDATE_TIME_UTC)" \
            f" values ({id},2, {value['SECURITY_ID']},'{value['SYMBOL']}', '{value['SECURITY_NAME']}',39,'IB',{value['BRANCH_ID']},'{value['BRANCH_NAME']}',{value['SETTLE_QUANTITY']},{value['SETTLE_T1_QUANTITY']}, {value['SETTLE_T2_QUANTITY']},{value['SETTLE_TN_QUANTITY']},0,'{VERIFY_MD5}',0,'{{}}','{create_time}','{update_time}')"
        branch_total_sql_list.append(branch_total_sql)
    connect.commit_data("alter session set NLS_TIMESTAMP_FORMAT='yyyy-mm-dd hh24:mi:ss:ff'")
    if connect.get_fetchone(select_us_branch_detail_holding_sql) is not None:
        print(f"开始执行删除子仓明细表数据：执行sql：{del_us_branch_detail_holding_sql}")
        connect.commit_data(del_us_branch_detail_holding_sql)
    for insert_sql in branch_detail_sql_list:
        connect.commit_data(insert_sql)
    if connect.get_fetchone(select_us_branch_detail_holding_sql) is not None:
        print(f"{len(branch_detail_sql_list)}条子仓明细表数据插入成功")

    if connect.get_fetchone(select_us_holding_sql) is not None:
        print(f"开始执行删除持仓表数据：执行sql：{del_us_holding_sql}")
        connect.commit_data(del_us_holding_sql)
    for insert_sql in us_holding_sql_list:
        connect.commit_data(insert_sql)
    if connect.get_fetchone(select_us_holding_sql) is not None:
        print(f"{len(us_holding_sql_list)}条持仓表数据插入成功")

    # done us_branch_total_holding insert
    if connect.get_fetchone(select_us_branch_total_holding_sql) is not None:
        print("开始执行delete子仓汇总表数据")
        connect.commit_data(del_us_branch_total_holding_sql)
    for insert_sql in branch_total_sql_list:
        connect.commit_data(insert_sql)
    if connect.get_fetchone(select_us_branch_total_holding_sql) is not None:
        print(f"{len(branch_total_sql_list)}条子仓汇总表数据插入成功")

def test_delete_data():
    if connect.get_fetchone(select_us_branch_detail_holding_sql) is not None:
        print(f"开始执行删除子仓明细表数据：执行sql：{del_us_branch_detail_holding_sql}")
        connect.commit_data(del_us_branch_detail_holding_sql)
    if connect.get_fetchone(select_us_branch_detail_holding_sql) is None:
        print("子仓明细表测试数据清理成功")
    if connect.get_fetchone(select_us_branch_total_holding_sql) is not None:
        print(f"开始执行删除子仓汇总表数据：执行sql：{del_us_branch_total_holding_sql}")
        connect.commit_data(del_us_branch_total_holding_sql)
    if connect.get_fetchone(select_us_branch_total_holding_sql) is None:
        print("子仓汇总表测试数据清理成功")
    if connect.get_fetchone(select_us_holding_sql) is not None:
        print(f"开始执行删除持仓表数据：执行sql：{del_us_holding_sql}")
        connect.commit_data(del_us_holding_sql)
    if connect.get_fetchone(select_us_holding_sql) is None:
        print("持仓表测试数据清理成功")

