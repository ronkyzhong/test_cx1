# -*- coding: utf-8 -*-
# @Time    : 2020/8/25 17:28
# @Author  : jiashu.zhong
# @Site    : 
# @File    : connect_oracle.py
import cx_Oracle

import yaml

with open('../config/db_config.yaml', encoding='utf-8') as f:
    db_config = yaml.safe_load(f)['db_config']


class ConnectOracle:
    def __init__(self):
        """
        创建 oracle 链接，并建立游标
        """
        self.con = cx_Oracle.connect(db_config['user'], db_config['passwd'],
                                     db_config['host'] + ":" + db_config['port'] + "/" + db_config['sid'])
        self.cursor = self.con.cursor()

    def get_fetchone(self, sql):
        """
        查询 sql 只返回一条 tuple 记录
        :param sql:
        :return: ("ssss") 一条 tuple 记录
        """
        self.cursor.execute(sql)
        data = self.cursor.fetchone()
        return data

    def get_fetchall(self,sql):
        """
        查询 sql 只返回多条记录，[("aaa"),("bbbb")]
        :param sql:
        :return: [("aaa"),("bbbb")]
        """
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data

    def commit_data(self, sql):
        self.cursor.execute(sql)
        self.con.commit()

if __name__ == '__main__':
    asset_account_id = "2800004626"
    sql =  'select a.money_current_balance,a.money_in_today,a.money_out_today,a.cost_fee_today,a.penalty,a.short_penalty from HSdc.MONEY_ACCOUNT_BALANCE a where asset_account_id = {} and money_type = 4'.format(asset_account_id)
    data = ConnectOracle().get_fetchone(sql)
    money_current_balance = data[0]
    money_in_today = data[1]
    money_out_today = data[2]
    cost_fee_today = data[3]
    penalty = data[4]
    short_penalty = data[5]
    book_balance = money_current_balance+money_in_today-money_out_today-cost_fee_today-penalty-short_penalty
    print(book_balance)