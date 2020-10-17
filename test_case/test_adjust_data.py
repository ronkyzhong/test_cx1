# -*- coding: utf-8 -*-
# @Time    : 2020/9/22 15:32
# @Author  : jiashu.zhong
# @Site    : 
# @File    : test_adjust_data.py
import logging

import yaml

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s  %(message)s ')
# 声明了一个 Log 对象
log = logging.getLogger(__name__)
adjust_data = {}
positions = []

with open("../datas/stock_share.yaml", encoding='utf-8') as f:
    datas = yaml.safe_load(f)
for key, data in datas.items():
    share_dict = dict()
    share_dict[data['SYMBOL']] = {
        key: data['SETTLE_QUANTITY'] + data['SETTLE_T1_QUANTITY'] + data['SETTLE_T2_QUANTITY'] + data[
            'SETTLE_TN_QUANTITY']}
    positions.append(share_dict)
for index, value in enumerate(positions):
    for k, v in value.items():
        positions[index - 1].get(k)
        adjust_data[k] = [v, positions[index - 1].get(k)]


def test_adjust_customer():
    data = adjust_data
    num = 1
    for key, value in data.items():
        marginShort = value[0][f'marginShortPositive{num}']
        marginLong = value[1][f'marginLongPositive{num}']
        margin = marginLong + marginShort
        if marginLong > 0 and marginShort > 0:
            # todo 搬仓
            log.info(f"stock:{key} 属于搬仓场景1:{num}，'marginLong()':{marginLong},'marginShort()':{marginShort},搬仓方向：marginShort==>marginLong")
            log.info(f"stock:{key},from_branch_id:{datas[f'marginShortPositive{num}']['BRANCH_ID']}, to_branch_id:{datas[f'marginLongPositive{num}']['BRANCH_ID']},transfer_amount:{abs(marginShort)}，LONG_TOTAL_QTY_BEFORE:{marginLong},SHORT_TOTAL_QTY_BEFORE:{marginShort},LONG_TOTAL_QTY_AFTER:{margin},SHORT_TOTAL_QTY_AFTER:0,\
            LONG_SETTLE_QTY_BEFORE:{datas[f'marginLongPositive{num}']['SETTLE_QUANTITY']},LONG_T1_QTY_BEFORE:{datas[f'marginLongPositive{num}']['SETTLE_T1_QUANTITY']},LONG_T2_QTY_BEFORE:{datas[f'marginLongPositive{num}']['SETTLE_T2_QUANTITY']},Short_SETTLE_QTY_BEFORE:{datas[f'marginShortPositive{num}']['SETTLE_QUANTITY']},Short_T1_QTY_BEFORE:{datas[f'marginShortPositive{num}']['SETTLE_T1_QUANTITY']},Short_T2_QTY_BEFORE:{datas[f'marginShortPositive{num}']['SETTLE_T2_QUANTITY']} \n")
            pass
        if marginLong > 0 and marginShort == 0:
            # 不需要搬仓
            pass
        if marginLong > 0 and marginShort < 0:
            if abs(marginLong) > abs(marginShort):
                # todo 搬仓
                log.info(
                    f"stock:{key} 属于搬仓场景2:{num}，'marginLong()':{marginLong},'marginShort()':{marginShort},搬仓方向：marginLong==>marginShort")
                log.info(f"stock:{key},from_branch_id:{datas[f'marginLongPositive{num}']['BRANCH_ID']}, to_branch_id:{datas[f'marginShortPositive{num}']['BRANCH_ID']},transfer_amount:{abs(marginShort)}，LONG_TOTAL_QTY_BEFORE:{marginLong},SHORT_TOTAL_QTY_BEFORE:{marginShort},LONG_TOTAL_QTY_AFTER:{margin},SHORT_TOTAL_QTY_AFTER:0,\
                LONG_SETTLE_QTY_BEFORE:{datas[f'marginLongPositive{num}']['SETTLE_QUANTITY']},LONG_T1_QTY_BEFORE:{datas[f'marginLongPositive{num}']['SETTLE_T1_QUANTITY']},LONG_T2_QTY_BEFORE:{datas[f'marginLongPositive{num}']['SETTLE_T2_QUANTITY']},Short_SETTLE_QTY_BEFORE:{datas[f'marginShortPositive{num}']['SETTLE_QUANTITY']},Short_T1_QTY_BEFORE:{datas[f'marginShortPositive{num}']['SETTLE_T1_QUANTITY']},Short_T2_QTY_BEFORE:{datas[f'marginShortPositive{num}']['SETTLE_T2_QUANTITY']}  \n")

                pass
            elif abs(marginLong) == abs(marginShort):
                # todo 搬仓
                log.info(
                    f"stock:{key} 属于搬仓场景3:{num}，'marginLong()':{marginLong},'marginShort()':{marginShort},搬仓方向：marginLong==>marginShort")
                log.info(f"stock:{key},from_branch_id:{datas[f'marginLongPositive{num}']['BRANCH_ID']}, to_branch_id:{datas[f'marginShortPositive{num}']['BRANCH_ID']},transfer_amount:{abs(marginShort)}，LONG_TOTAL_QTY_BEFORE:{marginLong},SHORT_TOTAL_QTY_BEFORE:{marginShort},LONG_TOTAL_QTY_AFTER:{margin},SHORT_TOTAL_QTY_AFTER:0,\
                LONG_SETTLE_QTY_BEFORE:{datas[f'marginLongPositive{num}']['SETTLE_QUANTITY']},LONG_T1_QTY_BEFORE:{datas[f'marginLongPositive{num}']['SETTLE_T1_QUANTITY']},LONG_T2_QTY_BEFORE:{datas[f'marginLongPositive{num}']['SETTLE_T2_QUANTITY']},Short_SETTLE_QTY_BEFORE:{datas[f'marginShortPositive{num}']['SETTLE_QUANTITY']},Short_T1_QTY_BEFORE:{datas[f'marginShortPositive{num}']['SETTLE_T1_QUANTITY']},Short_T2_QTY_BEFORE:{datas[f'marginShortPositive{num}']['SETTLE_T2_QUANTITY']}  \n")

                pass
            else:
                # todo 搬仓
                log.info(
                    f"stock:{key} 属于搬仓场景4:{num}，'marginLong()':{marginLong},'marginShort()':{marginShort},搬仓方向：marginLong==>marginShort")
                log.info(f"stock:{key},from_branch_id:{datas[f'marginLongPositive{num}']['BRANCH_ID']}, to_branch_id:{datas[f'marginShortPositive{num}']['BRANCH_ID']},transfer_amount:{abs(marginLong)}，LONG_TOTAL_QTY_BEFORE:{marginLong},SHORT_TOTAL_QTY_BEFORE:{marginShort},LONG_TOTAL_QTY_AFTER:0,SHORT_TOTAL_QTY_AFTER:{margin},\
                LONG_SETTLE_QTY_BEFORE:{datas[f'marginLongPositive{num}']['SETTLE_QUANTITY']},LONG_T1_QTY_BEFORE:{datas[f'marginLongPositive{num}']['SETTLE_T1_QUANTITY']},LONG_T2_QTY_BEFORE:{datas[f'marginLongPositive{num}']['SETTLE_T2_QUANTITY']},Short_SETTLE_QTY_BEFORE:{datas[f'marginShortPositive{num}']['SETTLE_QUANTITY']},Short_T1_QTY_BEFORE:{datas[f'marginShortPositive{num}']['SETTLE_T1_QUANTITY']},Short_T2_QTY_BEFORE:{datas[f'marginShortPositive{num}']['SETTLE_T2_QUANTITY']}  \n")

                pass
        if marginLong == 0 and marginShort > 0:
            # todo 搬仓
            log.info(
                f"stock:{key} 属于搬仓场景5:{num}，'marginLong()':{marginLong},'marginShort()':{marginShort},搬仓方向：marginShort==>marginLong")
            log.info(f"stock:{key},from_branch_id:{datas[f'marginShortPositive{num}']['BRANCH_ID']}, to_branch_id:{datas[f'marginLongPositive{num}']['BRANCH_ID']},transfer_amount:{abs(marginShort)}，LONG_TOTAL_QTY_BEFORE:{marginLong},SHORT_TOTAL_QTY_BEFORE:{marginShort},LONG_TOTAL_QTY_AFTER:{margin},SHORT_TOTAL_QTY_AFTER:0,\
            LONG_SETTLE_QTY_BEFORE:{datas[f'marginLongPositive{num}']['SETTLE_QUANTITY']},LONG_T1_QTY_BEFORE:{datas[f'marginLongPositive{num}']['SETTLE_T1_QUANTITY']},LONG_T2_QTY_BEFORE:{datas[f'marginLongPositive{num}']['SETTLE_T2_QUANTITY']},Short_SETTLE_QTY_BEFORE:{datas[f'marginShortPositive{num}']['SETTLE_QUANTITY']},Short_T1_QTY_BEFORE:{datas[f'marginShortPositive{num}']['SETTLE_T1_QUANTITY']},Short_T2_QTY_BEFORE:{datas[f'marginShortPositive{num}']['SETTLE_T2_QUANTITY']}  \n")

            pass
        if marginLong == 0 and marginShort == 0:
            # 不需要搬仓
            pass
        if marginLong == 0 and marginShort < 0:
            # 不需要搬仓
            pass
        if marginLong < 0 and marginShort > 0:
            if abs(marginLong) > abs(marginShort):
                # todo 搬仓
                log.info(
                    f"stock:{key} 属于搬仓场景6:{num}，'marginLong()':{marginLong},'marginShort()':{marginShort},搬仓方向：marginShort==>marginLong")
                log.info(f"stock:{key},from_branch_id:{datas[f'marginShortPositive{num}']['BRANCH_ID']}, to_branch_id:{datas[f'marginLongPositive{num}']['BRANCH_ID']},transfer_amount:{abs(marginLong)}，LONG_TOTAL_QTY_BEFORE:{marginLong},SHORT_TOTAL_QTY_BEFORE:{marginShort},LONG_TOTAL_QTY_AFTER:0,SHORT_TOTAL_QTY_AFTER:{margin},\
                LONG_SETTLE_QTY_BEFORE:{datas[f'marginLongPositive{num}']['SETTLE_QUANTITY']},LONG_T1_QTY_BEFORE:{datas[f'marginLongPositive{num}']['SETTLE_T1_QUANTITY']},LONG_T2_QTY_BEFORE:{datas[f'marginLongPositive{num}']['SETTLE_T2_QUANTITY']},Short_SETTLE_QTY_BEFORE:{datas[f'marginShortPositive{num}']['SETTLE_QUANTITY']},Short_T1_QTY_BEFORE:{datas[f'marginShortPositive{num}']['SETTLE_T1_QUANTITY']},Short_T2_QTY_BEFORE:{datas[f'marginShortPositive{num}']['SETTLE_T2_QUANTITY']}  \n")

                pass
            elif abs(marginLong) == abs(marginShort):
                # todo 搬仓
                log.info(
                    f"stock:{key} 属于搬仓场景7:{num}，'marginLong()':{marginLong},'marginShort()':{marginShort},搬仓方向：marginShort==>marginLong")
                log.info(f"stock:{key},from_branch_id:{datas[f'marginShortPositive{num}']['BRANCH_ID']}, to_branch_id:{datas[f'marginLongPositive{num}']['BRANCH_ID']},transfer_amount:{abs(marginShort)}，LONG_TOTAL_QTY_BEFORE:{marginLong},SHORT_TOTAL_QTY_BEFORE:{marginShort},LONG_TOTAL_QTY_AFTER:{margin},SHORT_TOTAL_QTY_AFTER:0,\
                LONG_SETTLE_QTY_BEFORE:{datas[f'marginLongPositive{num}']['SETTLE_QUANTITY']},LONG_T1_QTY_BEFORE:{datas[f'marginLongPositive{num}']['SETTLE_T1_QUANTITY']},LONG_T2_QTY_BEFORE:{datas[f'marginLongPositive{num}']['SETTLE_T2_QUANTITY']},Short_SETTLE_QTY_BEFORE:{datas[f'marginShortPositive{num}']['SETTLE_QUANTITY']},Short_T1_QTY_BEFORE:{datas[f'marginShortPositive{num}']['SETTLE_T1_QUANTITY']},Short_T2_QTY_BEFORE:{datas[f'marginShortPositive{num}']['SETTLE_T2_QUANTITY']}  \n")

                pass
            else:
                # todo 搬仓
                log.info(
                    f"stock:{key} 属于搬仓场景8:{num}，'marginLong()':{marginLong},'marginShort()':{marginShort},搬仓方向：marginShort==>marginLong")
                log.info(f"stock:{key},from_branch_id:{datas[f'marginShortPositive{num}']['BRANCH_ID']}, to_branch_id:{datas[f'marginLongPositive{num}']['BRANCH_ID']},transfer_amount:{abs(marginShort)}，LONG_TOTAL_QTY_BEFORE:{marginLong},SHORT_TOTAL_QTY_BEFORE:{marginShort},LONG_TOTAL_QTY_AFTER:{margin},SHORT_TOTAL_QTY_AFTER:0,\
                LONG_SETTLE_QTY_BEFORE:{datas[f'marginLongPositive{num}']['SETTLE_QUANTITY']},LONG_T1_QTY_BEFORE:{datas[f'marginLongPositive{num}']['SETTLE_T1_QUANTITY']},LONG_T2_QTY_BEFORE:{datas[f'marginLongPositive{num}']['SETTLE_T2_QUANTITY']},Short_SETTLE_QTY_BEFORE:{datas[f'marginShortPositive{num}']['SETTLE_QUANTITY']},Short_T1_QTY_BEFORE:{datas[f'marginShortPositive{num}']['SETTLE_T1_QUANTITY']},Short_T2_QTY_BEFORE:{datas[f'marginShortPositive{num}']['SETTLE_T2_QUANTITY']} \n")

                pass
        if marginLong < 0 and marginShort == 0:
            # todo 搬仓
            log.info(
                f"stock:{key} 属于搬仓场景9:{num}，'marginLong()':{marginLong},'marginShort()':{marginShort},搬仓方向：marginShort==>marginLong")
            log.info(f"stock:{key},from_branch_id:{datas[f'marginShortPositive{num}']['BRANCH_ID']}, to_branch_id:{datas[f'marginLongPositive{num}']['BRANCH_ID']},transfer_amount:{abs(marginLong)}，LONG_TOTAL_QTY_BEFORE:{marginLong},SHORT_TOTAL_QTY_BEFORE:{marginShort},LONG_TOTAL_QTY_AFTER:0,SHORT_TOTAL_QTY_AFTER:{margin},\
            LONG_SETTLE_QTY_BEFORE:{datas[f'marginLongPositive{num}']['SETTLE_QUANTITY']},LONG_T1_QTY_BEFORE:{datas[f'marginLongPositive{num}']['SETTLE_T1_QUANTITY']},LONG_T2_QTY_BEFORE:{datas[f'marginLongPositive{num}']['SETTLE_T2_QUANTITY']},Short_SETTLE_QTY_BEFORE:{datas[f'marginShortPositive{num}']['SETTLE_QUANTITY']},Short_T1_QTY_BEFORE:{datas[f'marginShortPositive{num}']['SETTLE_T1_QUANTITY']},Short_T2_QTY_BEFORE:{datas[f'marginShortPositive{num}']['SETTLE_T2_QUANTITY']}  \n")
            pass
        if marginLong < 0 and marginShort < 0:
            # todo 搬仓
            log.info(
                f"stock:{key} 属于搬仓场景10:{num}，'marginLong()':{marginLong},'marginShort()':{marginShort},搬仓方向：marginShort==>marginLong")
            log.info(f"stock:{key},from_branch_id:{datas[f'marginShortPositive{num}']['BRANCH_ID']}, to_branch_id:{datas[f'marginLongPositive{num}']['BRANCH_ID']},transfer_amount:{abs(marginLong)}，LONG_TOTAL_QTY_BEFORE:{marginLong},SHORT_TOTAL_QTY_BEFORE:{marginShort},LONG_TOTAL_QTY_AFTER:0,SHORT_TOTAL_QTY_AFTER:{margin},\
            LONG_SETTLE_QTY_BEFORE:{datas[f'marginLongPositive{num}']['SETTLE_QUANTITY']},LONG_T1_QTY_BEFORE:{datas[f'marginLongPositive{num}']['SETTLE_T1_QUANTITY']},LONG_T2_QTY_BEFORE:{datas[f'marginLongPositive{num}']['SETTLE_T2_QUANTITY']},Short_SETTLE_QTY_BEFORE:{datas[f'marginShortPositive{num}']['SETTLE_QUANTITY']},Short_T1_QTY_BEFORE:{datas[f'marginShortPositive{num}']['SETTLE_T1_QUANTITY']},Short_T2_QTY_BEFORE:{datas[f'marginShortPositive{num}']['SETTLE_T2_QUANTITY']}  \n")
            pass

        num += 1
