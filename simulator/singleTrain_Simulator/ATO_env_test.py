import random

import numpy as np
from running_parameter import *
import itertools
import matplotlib.pyplot as plt
import math



from train_simulator import TrainRun


# def descartes(x, y):
#     # return [(x[i], y[j]) for i in range(len(x)) for j in range(len(y))]
#     e = []
#     for item in itertools.product(x, y):
#         e.append(item)
#     return e


# dis = np.concatenate(
#     (np.arange(0, SPEED_LIMITATION_POINT[0], 2),
#      np.arange(155, SPEED_LIMITATION_POINT[1], 10),
#      np.arange(1120, DISTANCE, 2),
#      GRADIENT_CHANGE), axis=0)
#
# dis = np.unique(np.sort(dis))

# print(dis)
# print(len(dis))

# 生成2维度数组表示状态离散，维度1索引为离散距离，维度2为该距离上的速度离散
# reg = []
# for i in dis:
#     if i <= 155:
#         reg.append(descartes([i], np.arange(0, 16.7)))
#     elif i <= 1120:
#         reg.append(descartes([i], np.arange(0, 22.2)))
#     else:
#         reg.append(descartes([i], np.arange(0, 16.7)))
#
# print(reg[90])


# 生成1维度数组表示状态离散
# a = descartes(dis[:int(np.argwhere(dis==155)+1)], np.arange(0, 16.7))
# b = descartes(dis[int(np.argwhere(dis==155)+1): int(np.argwhere(dis==1120)+1)], np.arange(0, 22.2))
# c = descartes(dis[int(np.argwhere(dis==1120)+1):], np.arange(0, 16.7))
# print(a)
# print(b)
# print(c)

# 返回值对应的索引
# a = np.argwhere(dis==6)
# print(int(a))


a = TrainRun()


# 一组驾驶策略可行解，用于调试train_simulator
# running_loc, running_speed = [], []
# while a.state[0] < a.terminal:
#     if a.state[0] <= 155:
#         a.step(0)
#     elif a.state[0] <= 1148:
#         a.step(1)
#     else:
#         a.step(2)
#     running_loc.append(a.state[0])
#     running_speed.append(a.state[1])
# running_loc.insert(0, 0)
# running_speed.insert(0, 0)
# print(running_loc)
# print(running_speed)
# print('end')
#
# plt.figure()
# plt.plot(running_loc, running_speed)
# plt.show()

# 模拟人工驾驶策略输入
# for i in range(260):
#     m = int(input('执行操纵：'))
#     a.step(m)
#     print(a.state)
# print('end')

# 随机驾驶驾驶
running_loc, running_speed = [], []
while a.state[0] < a.terminal:
    m = random.randint(0, 2)
    a.step(m)
    running_loc.append(a.state[0])
    running_speed.append(a.state[1])
running_loc.insert(0, 0)
running_speed.insert(0, 0)
print(running_loc)
print(running_speed)
print(len(running_loc), len(running_speed))




# for i in range(len(a.space)):
#     plt.scatter(a.space[i][:, 0], a.space[i][:, 1])
#
# plt.show()

# a = 2.75 + 0.014 * 80 + 0.00075 * 80 * 80
# b = 280000 * a * 0.001
# c = b / 28000
#
# print(a)
# print(b)
# print(c)