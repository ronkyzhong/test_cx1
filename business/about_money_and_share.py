# -*- coding: utf-8 -*-
# @Time    : 2020/8/25 17:37
# @Author  : jiashu.zhong
# @Site    : 
# @File    : about_money_and_share.py
import json
import os

from Utils.connect_oracle import ConnectOracle
import logging
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s  %(message)s :\n')
# 声明了一个 Log 对象
log = logging.getLogger(__name__)


def get_root_dir():
    return os.path.dirname(os.path.dirname(__file__))

def get_dir():
    return os.path.dirname(__file__)

class GetMoneyAndShare:
    def __init__(self):
        self.connect = ConnectOracle()

    def get_book_balance(self, asset_account_id):
        """
        获取账面余额
        :return:
        """
        money_balance_sql = 'select a.money_current_balance,a.money_in_today,a.money_out_today,a.cost_fee_today,a.penalty,a.short_penalty from HSdc.MONEY_ACCOUNT_BALANCE a where asset_account_id = {} and money_type = 4'.format(
            asset_account_id)
        money_balance = self.connect.get_fetchone(money_balance_sql)
        money_current_balance = money_balance[0]
        money_in_today = money_balance[1]
        money_out_today = money_balance[2]
        cost_fee_today = money_balance[3]
        penalty = money_balance[4]
        short_penalty = money_balance[5]
        book_balance = money_current_balance + money_in_today - money_out_today - cost_fee_today - penalty - short_penalty
        return book_balance

    def get_account_holding(self, asset_account_id):
        """
        获取客户持仓情况：期权持仓：可用数量(可平仓数量)，账面数量，其他证券持仓可用数量，账面数量
        :param asset_account_id:
        :return: option_holding_dict,stock_holding_dict
        """
        holding_sql = 'select a.current_share,a.today_trade_buy_share,a.today_trade_sell_share,a.trade_freeze_balance_share,a.law_freeze_balance_share,a.other_freeze_balance_share,a.short_pre_close_share,a.asset_account_id,a.symbol,a.security_type,a.position_status from hsdc.us_holding a where a.asset_account_id= {} and a.position_status<>0'.format(
            asset_account_id)
        holding_dict = dict()  # {symbol:[可用数量，账面数量]}
        stock_holding_dict = dict()
        option_holding_dict = dict()
        account_holding_data = self.connect.get_fetchall(holding_sql)
        for data in account_holding_data:
            current_share = data[0]
            today_trade_buy_share = data[1]
            today_trade_sell_share = data[2]
            trade_freeze_balance_share = data[3]
            law_freeze_balance_share = data[4]
            other_freeze_balance_share = data[5]
            short_pre_close_share = data[6]
            symbol = data[8]
            security_type = data[-2]
            # 总冻结数量 = 【交易冻结】+【司法冻结】+【其他冻结】
            freeze_share = trade_freeze_balance_share + law_freeze_balance_share + other_freeze_balance_share
            # 账面数量 = 【期初数量】-【当日卖出】+【当日买入】
            book_balance = current_share - today_trade_sell_share + today_trade_buy_share
            if data[-1] == 1:
                # 头寸状态为1，做多时可用数量=账面数量 - 总冻结数
                available_share = book_balance - freeze_share
            elif data[-1] == 2:
                # 头寸状态为2，做空时可用数量= - 账面数量 - 【做空预平仓】
                available_share = - book_balance - short_pre_close_share
            if data[-2] == 8192:
                option_holding_dict[symbol] = {"available_share": available_share, "book_balance": book_balance,
                                               "position_status": data[-1]}
            else:
                stock_holding_dict[symbol] = {"available_share": available_share, "book_balance": book_balance,
                                              "position_status": data[-1]}
            holding_dict[symbol] = {"available_share": available_share, "book_balance": book_balance}
        return option_holding_dict, stock_holding_dict, holding_dict

    def get_stock_margin_ratio(self, asset_account_id):
        """
        获取客户持仓证券的孖展初始保证金比率
        :param asset_account_id:
        :return:
        """
        margin_ratio_dict = dict()
        short_ratio_dict = dict()
        stock_names = self.get_account_holding(asset_account_id)[1].keys()
        for stock_name in stock_names:
            stock_margin_ratio_sql = """select a.stock_code,a.margin_switch,a.init_margin_ratio,a.keep_margin_ratio,a.short_switch,a.init_short_margin_ratio,a.keep_short_margin_ratio from hsdc.margin_ratio a where stock_code='{}'""".format(
                stock_name)
            stock_margin_ratio = self.connect.get_fetchone(stock_margin_ratio_sql)

            if stock_margin_ratio is None:
                margin_ratio_dict[stock_name] = {"init_margin_ratio": 1,
                                                 "keep_margin_ratio": 1}
                log.info("\n {} 在孖展比率表没有记录".format(stock_name))
            else:
                margin_switch = stock_margin_ratio[1]
                init_margin_ratio = stock_margin_ratio[2]
                keep_margin_ratio = stock_margin_ratio[3]
                short_switch = stock_margin_ratio[4]
                init_short_margin_ratio = stock_margin_ratio[5]
                keep_short_margin_ratio = stock_margin_ratio[6]
                if margin_switch == 1:
                    margin_ratio_dict[stock_name] = {"init_margin_ratio": init_margin_ratio,
                                                     "keep_margin_ratio": keep_margin_ratio}
                else:
                    margin_ratio_dict[stock_name] = {"init_margin_ratio": 1,
                                                     "keep_margin_ratio": 1}
                if short_switch == 1:
                    short_ratio_dict[stock_name] = {"init_short_margin_ratio": init_short_margin_ratio,
                                                    "keep_short_margin_ratio": keep_short_margin_ratio}
                else:
                    short_ratio_dict[stock_name] = {"init_short_margin_ratio": 1,
                                                    "keep_short_margin_ratio": 1}
        return margin_ratio_dict, short_ratio_dict

    def get_option_params(self):
        """
        获取期权卖空参数
        :return:
        """
        stock_option_params = dict()
        index_option_params = dict()
        option_params_sql = 'select a.option_product_type,a.content from hsdc.formula_configure a where a.status=0 and a.market=2'
        option_params_data = self.connect.get_fetchall(option_params_sql)
        for data in option_params_data:
            # data[0]==1 为股票期权
            if data[0] == 1:
                stock_option_params = json.loads(data[1])
            # data[0]==2 为系数行期权
            elif data[0] == 2:
                index_option_params = json.loads(data[1])
        return stock_option_params, index_option_params


if __name__ == '__main__':
    print(get_root_dir(), get_dir())
    get = GetMoneyAndShare()
    get_book_balance = get.get_book_balance(2800004626)
    log.info("\n asset_account_id:2800004626:账面余额:{}".format(get_book_balance))
    get_account_holding = GetMoneyAndShare().get_account_holding(2800004626)
    log.info("\n asset_account_id:2800004626:\n 期权持仓情况:{},\n 其他证券持仓情况:{}".format(get_account_holding[0],
                                                                                 get_account_holding[1]))
    get_stock_margin_ratio = get.get_stock_margin_ratio(2800004626)
    log.info("\n asset_account_id:2800004626:\n 证券持仓的margin_ratio 信息:{}".format(get_stock_margin_ratio[0]))
    get_option_params = get.get_option_params()
    log.info("\n 股票型期权参数信息:{}，\n 指数型期权参数信息:{}".format(get_option_params[0], get_option_params[1]))
