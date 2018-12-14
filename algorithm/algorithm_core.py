#import requests
import numpy as np
import pandas as pd
#import gevent
#import json
import argparse
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
curStep:表示当前步数
totalStep:表示总步数
"""

def algorithm_main(param, user, curStep, totalStep):
    return my_strategy(param,user, curStep, totalStep)

def my_strategy(data_input,user, curStep, totalStep) :
    walls_df = pd.DataFrame(data_input['walls'])
    remain_step = totalStep - curStep
    # print(walls_df)
    # 计算包裹距离，按照从近到远排序
    job_df = pd.DataFrame(data_input['jobs'])
    j = 0
    for ind in job_df.index:
        i = job_df.loc[ind, 'x']
        dis = -1 * (abs(i - data_input['player1']['x']) + abs(job_df.loc[j, 'y'] - data_input['player1']['y']))
        j += 1
        job_df.loc[ind, 'dis'] = dis
        job_df = job_df.sort_values(by=['dis', 'value'], ascending=False)

    act = data_input['player1']
    h_position = data_input['player1']

    if data_input['n_jobs'] == 10 | remain_step <= 30:
        while (int(h_position['home_x']) != act['x'] | int(h_position['home_y']) != act['y']):
            if (int(h_position['home_x']) < act['x']) & ((act['x'] - 1 & act['y']) not in walls_df):
                act['x'] = act['x'] - 1
                print('U')
            elif (int(h_position['home_y']) < act['y']) & ((act['x'] & act['y'] - 1) not in walls_df):
                act['y'] = act['y'] - 1
                print('L')
            elif (int(h_position['home_x']) > act['y']) & ((act['x'] + 1 & act['y']) not in walls_df):
                act['x'] = act['x'] + 1
                print('D')
            elif (int(h_position['home_y']) > act['y']) & ((act['x'] & act['y'] + 1) not in walls_df):
                act['y'] = act['y'] + 1
                print('R')
    else:
        b_position = job_df.iloc[0, :]
        act = data_input['player1']
        while (int(b_position['x']) != act['x'] | int(b_position['y']) != act['y']):
            if (int(b_position['x']) < act['x']) & ((act['x'] - 1 & act['y']) not in walls_df):
                act['x'] = act['x'] - 1
                print('U')
            elif (int(b_position['y']) < act['y']) & ((act['x'] & act['y'] - 1) not in walls_df):
                act['y'] = act['y'] - 1
                print('L')
            elif (int(b_position['y']) > act['y']) & ((act['x'] + 1 & act['y']) not in walls_df):
                act['x'] = act['x'] + 1
                print('D')
            elif (int(b_position['y']) > act['y']) & ((act['x'] & act['y'] + 1) not in walls_df):
                act['y'] = act['y'] + 1
                print('R')
    return act
    # return(np.random.choice(['U', 'D', 'L', 'R', 'S']))
