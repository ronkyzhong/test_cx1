# -*- coding: utf-8 -*-
# @Time    : 2020/8/28 17:23
# @Author  : jiashu.zhong
# @Site    : 
# @File    : test.py


import pytest


@pytest.fixture
def test_print():
    print("\n this is a fixture==>先调用")


def test_ehlo(test_print):
    print("准备开始测试")
    print(test_ehlo.__name__)
    assert 1  # for demo purposes


def test_get_a():
    """
      a = ['T1', 'T2', 'T3,T4', 'T5']
      转 为 ['T1', 'T2', 'T3', 'T4', 'T5']
    :return:
    """
    a = ['T1', 'T2', 'T3,T4', 'T5']
    for index, value in enumerate(a):
        if ',' in value:
            new_value = value.split(',', 1)
            a[index] = new_value[0]
            a.insert(index + 1, new_value[1])

    print(a)


