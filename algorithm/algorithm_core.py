#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 09:39:56 2018

@author: liting
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 17:13:14 2018

@author: 01377931
"""
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 17:13:14 2018

@author: 01377931
"""
#import requests
import numpy as np
#import gevent
import json
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
curStep:表示当前步数
totalStep:表示总步数
"""
def algorithm_main(param, user,curStep, totalStep):
    text = json.dumps(param)
    input_data = json.loads(text)
    return my_strategy(input_data, user=user, curStep = curStep, totalStep = totalStep)

def my_strategy(input_data, user, curStep, totalStep):
    gamma = 0.8
    cur_step = int(curStep)
    total_step = int(totalStep)
    dic_walls=input_data['walls']
    dic_jobs=input_data['jobs']
    walls=np.ones((12,12)) #可走的路是1， 不能走的障碍是0
    jobs=np.zeros((12,12))
    
    for num_walls in range(len(dic_walls)):
        x_inc=dic_walls[num_walls]['x']
        y_inc=dic_walls[num_walls]['y']
        walls[int(x_inc),int(y_inc)]=0
    
    for num_jobs in range(len(dic_jobs)):
        x_inc=dic_jobs[num_jobs]['x']
        y_inc=dic_jobs[num_jobs]['y']
        jobs[int(x_inc),int(y_inc)]=dic_jobs[num_jobs]['value']
    
    my_state = input_data[user]
    if user=='player1':
        enemy = 'player2'
    else:
        enemy='player1'
        
    enemy_state = input_data[enemy]
    walls[enemy_state['home_x'],enemy_state['home_y']] = 0 # 敌人的大本营是我们墙
    
    # 计算上下左右的坐标
    loc_value = {'U':0,'D':0,'L':0,'R':0,'S':0}
    loc_coord,loc_value,backup1 = udlrs({'x':my_state['x'],'y':my_state['y']}, jobs, walls)
    #print('loc_coord:',loc_coord)
    # 如果上下左右有路障给、或者是-1 那么value就判断为-1
    # 用回家需要的步子来算，是不是要回家了
    #coord = {}
    # go_home(x,y,home_x,home_y,walls): 回家对路
    step_num,act_list,step_coord=go_home(my_state['x'],my_state['y'],my_state['home_x'],my_state['home_y'],walls)
    # 背上对包裹
    print("step_num,act_list,step_coord:",step_num,act_list,step_coord)
    n_jobs = my_state['n_jobs']
    print('total_step,cur_step,step_num,n_jobs:',total_step,cur_step,step_num,n_jobs)
    #print('step_num:',step_num,'act_list:',act_list)
    if (total_step - cur_step) > int(step_num) or n_jobs < 9:
        
        # 先判断是不是墙
        loc_value2={'U':0,'D':0,'L':0,'R':0,'S':0}
        for loc in list(['U','D','L','R','S']):
            if loc_value[loc] == -100:
                loc_value2[loc] = -100
            else:
                #coord={'x':loc_coord[loc]['x'],'y':loc_coord[loc]['y']}
                value_now = loc_value[loc]
                backup2,backup3,max_value_next = udlrs(loc_coord[loc],jobs,walls)
                value = value_now + gamma * max_value_next
                loc_value2[loc] = value
        #print('loc_value2:',loc_value)
        act1 = max(loc_value2, key=loc_value2.get)
        print('act1:',act1)
        return(act1)
    else:
        act2 = act_list[0]
        print('act2:',act2)
        return(act2)
      #return(np.random.choice(['U', 'D', 'L', 'R', 'S']))  
    #return(max(loc_value2, key=loc_value2.get))
                
      
    # 计算回家的步长
    #return(np.random.choice(['U', 'D', 'L', 'R', 'S']))
    
# 计算上下左右，有的话就返回坐标，没有的话返回-1 
# now_coord 坐标字典 {'x':1,'y':2}
def udlrs(now_coord,jobs,walls):
    loc_value = {'U':0,'D':0,'L':0,'R':0,'S':0}
    loc_coord = {'S':{'x':int(now_coord['x']),'y':int(now_coord['y'])},
                     'U':{'x':int(now_coord['x']),'y':int(now_coord['y'])-1},
                     'D':{'x':int(now_coord['x']),'y':int(now_coord['y'])+1},
                     'L':{'x':int(now_coord['x'])-1,'y':int(now_coord['y'])},
                     'R':{'x':int(now_coord['x'])+1,'y':int(now_coord['y'])}}
    for loc in list(['U','D','L','R','S']):
        if int(loc_coord[loc]['x']) > 11 or int(loc_coord[loc]['x']) < 0 or int(loc_coord[loc]['y']) > 11 or int(loc_coord[loc]['y']) < 0:
            loc_value[loc] = -100
        elif walls[int(loc_coord[loc]['x']),int(loc_coord[loc]['y'])]==0: #
            loc_value[loc] = -100
    i=0
    value_list=[0,0,0,0,0]
    for loc in list(['U','D','L','R','S']):
        if loc_value[loc]!=-100:
            value_list[i]=jobs[int(loc_coord[loc]['x']), int(loc_coord[loc]['y'])]
            i=i+1
    max_value = max(value_list)
    return loc_coord, loc_value, max_value
 

 
def direction_set(data):
    """
        函数功能，找到data中未被走过的地方，并同时记录该地方能够走的地方
    """
    dir_set = {}
    col_num = np.size(data,0)
    data1= np.zeros((col_num+2,col_num+2))
    #data2 = data

    for i in range(col_num):
        for j in range(col_num):
            data1[i+1,j+1] = data[i,j]
    data = data1
    
    v, h = np.where(data > 0)
    for i,j in zip(v, h):
        key = 'y'+str(i)+'x' + str(j)
        if data[i, j+1] > 0:            #该地方东邻块是否能走
            dir_set[key] = ['y'+str(i)+'x'+str(j+1)]
        if data[i+1, j] > 0:            #该地方南邻块是否能走
            if key in dir_set:
                dir_set[key] += ['y'+str(i+1)+'x'+str(j)]
            else:
                dir_set[key] = ['y'+str(i+1)+'x'+str(j)]
        #data[i, j-1]
        if data[i, j-1] > 0:            #该地方西邻块是否能走
            if key in dir_set:
                dir_set[key] += ['y'+str(i)+'x'+ str(j-1)]
            else:
                dir_set[key] = ['y'+str(i)+ 'x'+str(j-1)]
        #data[i-1, j]
        if data[i-1, j] > 0:            #该地方北邻块是否能走
            if key in dir_set:
                dir_set[key] += ['y'+str(i-1)+'x'+str(j)]
            else:
                dir_set[key] = ['y'+str(i-1) +'x'+str(j)]
    return dir_set,data
    #print(dir_set,data)
 
def get_forward_step(exit_index, start_index,direction):
    layer_ori = start_index  #存放第一层信息 
    while True:     
        layer_sec = []      #存放第二层信息
        for key in layer_ori: #将layer_ori里面所能达到的位置，存放在layer_sec中
            #print(key)
            layer_sec += direction[key]
            if exit_index in direction[key]:
                forward_step = key
        if exit_index in layer_sec: break
        layer_ori = layer_sec
    return forward_step

def go_home(x,y,home_x,home_y,walls):
    direction,data = direction_set(walls)
    
    exit_index = ['y'+str(home_y+1)+'x'+str(home_x+1)]
    start_index = ['y'+str(y+1)+'x'+str(x+1)]
    while True:
        forward_step = get_forward_step(exit_index[-1], start_index,direction)
        exit_index += [forward_step]
        if forward_step == 'y'+str(y+1)+'x'+str(x+1):
            break
    step = exit_index[::-1][:-1]
    for ind in step:
        #print(ind)
        y_inc = ind[1:ind.find('x')]
        #print(x_inc)
        x_inc = ind[ind.find('x')+1:]
        #print(y_inc)
        data[int(y_inc), int(x_inc)] = -8
    step_num = len(step)
    step.append('y'+str(home_y+1)+'x'+str(home_x+1))
    act_list = list()
    for i in range(step_num):
        x_now = int(step[i][step[i].find('x')+1:])
        y_now = int(step[i][1:step[i].find('x')])
        x_next = int(step[i+1][step[i+1].find('x')+1:])
        y_next = int(step[i+1][1:step[i+1].find('x')])   
        if x_now==x_next:
            if y_now > y_next:
                act_list.append('D')
            else:
                act_list.append('U')
        else:
            if x_now>x_next:
                act_list.append('L')
            else:
                act_list.append('R')
    step_coord = []
    for ind in step:
        y_inc = int(ind[1:ind.find('x')])-1
        x_inc = int(ind[ind.find('x')+1:])-1
        step_coord.append('y'+str(y_inc)+'x'+str(x_inc))
    return(step_num,act_list,step_coord)
"""

param = {
        'player1':{'name': 'p1', 'x': 5, 'y': 5, 'home_x': 5, 'home_y': 5, 'n_jobs': 0, 'value': 0, 'score': 0},
        'player2':{'name': 'p2', 'x': 10, 'y': 11, 'home_x': 6, 'home_y': 6, 'n_jobs': 0, 'value': 0, 'score': 0},
        'walls':[{'x': 0, 'y': 3}, {'x': 0, 'y': 5}, {'x': 0, 'y': 9}, {'x': 0, 'y': 11}, {'x': 1, 'y': 5}, 
               {'x': 1, 'y': 7}, {'x': 3, 'y': 1}, {'x': 3, 'y': 8}, {'x': 3, 'y': 10}, {'x': 4, 'y': 4},
               {'x': 4, 'y': 7}, {'x': 5, 'y': 4}, {'x': 5, 'y': 7}, {'x': 6, 'y': 2}, {'x': 6, 'y': 9}, 
               {'x': 6, 'y': 11}, {'x': 7, 'y': 5}, {'x': 7, 'y': 10}, {'x': 8, 'y': 9}, {'x': 9, 'y': 1}, 
               {'x': 9, 'y': 8}, {'x': 10, 'y': 0}, {'x': 10, 'y': 1}, {'x': 10, 'y': 7}],
        'jobs':[{'x': 0, 'y': 7, 'value': 11.0}, {'x': 1, 'y': 0, 'value': 10.0}, {'x': 1, 'y': 3, 'value': 12.0}, 
              {'x': 2, 'y': 5, 'value': 6.0}, {'x': 3, 'y': 5, 'value': 6.0}, {'x': 3, 'y': 6, 'value': 8.0}, 
              {'x': 3, 'y': 9, 'value': 10.0}, {'x': 4, 'y': 6, 'value': 11.0}, {'x': 5, 'y': 0, 'value': 6.0}, 
              {'x': 5, 'y': 11, 'value': 9.0}, {'x': 6, 'y': 1, 'value': 10.0}, {'x': 6, 'y': 3, 'value': 7.0}, 
              {'x': 6, 'y': 4, 'value': 6.0}, {'x': 7, 'y': 0, 'value': 10.0}, {'x': 7, 'y': 6, 'value': 9.0}, 
              {'x': 7, 'y': 11, 'value': 12.0}, {'x': 8, 'y': 2, 'value': 7.0}, {'x': 9, 'y': 0, 'value': 9.0}, 
              {'x': 9, 'y': 4, 'value': 9.0}, {'x': 9, 'y': 5, 'value': 10.0}, {'x': 9, 'y': 7, 'value': 11.0}, 
              {'x': 9, 'y': 9, 'value': 10.0}, {'x': 10, 'y': 8, 'value': 11.0}, {'x': 11, 'y': 10, 'value': 6.0}],
        'curStep':0,
        'totalStep':200
        }
user = 'player1'
curStep = cur_step = 0
totalStep = total_step = 200        
print(algorithm_main(param, user,curStep, totalStep))
"""
