# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 17:13:14 2018

@author: 01377931
"""
#import requests
import numpy as np
#import gevent
#import json
#import argparse
"""
algorithm_main方法为算法入口，请不要变更该方法名，返回方向字符串，例如“U”，方便我调用！！！
传入参数如下：
param:
    {
        'player1': { //玩家信息
            'name': 'p1', //玩家名
            'x': 8, //小哥所在位置X坐标
            'y': 4, //小哥所在位置Y坐标
            'home_x': 5, //小哥大本营所在位置X坐标
            'home_y': 5, //小哥大本营所在位置Y坐标
            'n_jobs': 10, //小哥背包包裹数
            'value': 99.0, //小哥背包包裹总价值
            'score': 0 //小哥得分
        },
        'player2': ..., // 同player1
        'walls': [ //障碍物所在位置
            {'x': 0, 'y': 1}, //障碍物X,Y坐标
            {'x': 0, 'y': 6},
        ...],
        'jobs': [
            {'x': 0, 'y': 2, 'value': 7.0}, //包裹所在位置，及其价值
            {'x': 0, 'y': 8, 'value': 9.0},
            ...
        ]
    }
user:代表我们处在当前的角色，如果user = "player1"，则对手是player2
"""
def algorithm_main(param, user):
    print(6666666)
    data_input = param
    return my_strategy(data_input)

def my_strategy(data_input) :
    return(np.random.choice(['U', 'D', 'L', 'R', 'S']))