# -*- coding: utf-8 -*-
# @Time    : 2020/8/25 16:52
# @Author  : jiashu.zhong
# @Site    : 
# @File    : test_cx.py
import cx_Oracle
import yaml

with open('./config/db_config.yaml', encoding='utf-8') as f:
    db_config = yaml.safe_load(f)['db_config']

con = cx_Oracle.connect(db_config['user'], db_config['passwd'], db_config['host'] + ":" + db_config['port'] + "/" +  db_config['sid'])
cursor = con.cursor()
sql = "select * from hsdc.us_holding where asset_account_id=2800002860"
cursor.execute(sql)
data = cursor.fetchall()
print(type(data))
[print(type(i),i) for i in data]


