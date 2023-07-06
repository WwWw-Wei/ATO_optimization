import math

import numpy as np
import copy
import itertools

from running_parameter import *


class TrainRun:
    def __init__(self):
        super(TrainRun, self).__init__()

        self.terminal = DISTANCE
        self.tripTime = TRIP_TIME
        self.gradientChange = GRADIENT_CHANGE
        self.speedLimPoint = SPEED_LIMITATION_POINT

        self.mass = MASS
        self.mo = TRACTION
        self.co = 0
        self.br = BRAKE

        self.action = ['mo', 'co', 'br']  # 牵引、(巡航、)惰行、制动
        self.n_actions = len(self.action)
        self.n_features = 2  # 状态维度包括距离、速度（运行时间、能耗、舒适度）

        self.origin = [0, 0]
        self.state = copy.deepcopy(self.origin)
        self.distance = self._build_line()[1]  # 位置离散信息，用于定位列车运行过程索引下一个步进点

        self.energy = 0
        self.time = 0

        self.space = self._build_line()[0]  # 离散后生成的解空间

    def _build_line(self):  # 根据线路环境参数生成路径规划的离散模型
        # 位置离散，出站与进站离散步进为2，其余为10，且包括限速（此处集成在出/进站）与坡道变更点
        location_des = np.concatenate(
            (
                np.arange(0, self.speedLimPoint[0], 2),
                np.arange(155, self.speedLimPoint[1], 10),
                np.arange(1120, DISTANCE, 2),
                GRADIENT_CHANGE),
            axis=0)

        location_des = np.unique(np.sort(location_des))

        # 离散状态生成，表示为3维度数组，维度1索引任意距离处所有可行状态集合，维度2索引距离离散，维度3索引该点的速度离散
        # 速度取均匀离散，此处取步进1，离散上下界为0和该点限速
        reg = []
        for i in location_des:
            if i <= self.speedLimPoint[0]:
                reg.append(np.array(descartes([i], np.arange(0, 16.7))))
            elif i <= self.speedLimPoint[1]:
                reg.append(np.array(descartes([i], np.arange(0, 22.2))))
            else:
                reg.append(np.array(descartes([i], np.arange(0, 16.7))))

        return reg, location_des

    def reset(self):  # 重置列车运行状态
        self.state = copy.deepcopy(self.origin)
        self.energy = 0
        self.time = 0
        return self.state

    def _getGradient(self):  # 计算坡道信息
        pass

    def _getTraction(self):  # 计算牵引力输出
        pass

    def _getBrake(self):  # 计算制动力输出
        pass

    def step(self, action):  # 列车智能体与运行环境交互
        # 获取当前状态与下一状态，按距离步进
        state_now = copy.deepcopy(self.state)  # 当前状态
        state_next_index = int(np.argwhere(self.distance == state_now[0]))+1  # 根据当前位置索引下一状态对应的距离
        distance_next = self.distance[state_next_index]

        # 计算阻力
        gradient_i = getGradient(distance_next)
        # 坡道阻力, 列车质量M单位为t时计算公式为W=mgi，质量m为Kg时有m=1000M，因此最后计算时除去倍率关系1000
        resistance_g = self.mass * 9.8 * gradient_i * 0.001

        # 基本阻力，列车质量M为t，速度为Km/h时计算公式为W_0 = a + b*v + c*v^2, 计算量单位为N/KN,因此除去倍率关系1000把m（Kg）转换为M（t）
        resistance_v = self.mass * 0.001 * \
                       (DAVIS_A + DAVIS_B * 3.6 * state_now[1] + DAVIS_C * 3.6 * 3.6 * state_now[1] * state_now[1]) if self.state[1] else 0

        # 根据所选工况计算状态转移用时、能耗、转移后速度
        print('坡道阻力', resistance_g/self.mass, '基本阻力', resistance_v/self.mass)
        print('阻力', ((resistance_g + resistance_v) / self.mass))
        if action == 0:  # 牵引
            acc = self.mo - ((resistance_g + resistance_v) / self.mass)
        elif action == 1:  # 惰行
            acc = -((resistance_g + resistance_v) / self.mass)
        else:  # 制动
            if self.state[1] > 0:
                acc = self.br - ((resistance_g + resistance_v) / self.mass)
            else:
                acc = 0

        print(action, acc)

        if acc != 0 or self.state[1] != 0:


            # 计算列车该步工况用时、能耗及转移后速度
            reg = 2 * acc * (distance_next - state_now[0]) + math.pow(state_now[1], 2)
            speed_next = math.sqrt(reg) if reg >= 0 else 0  # 某次状态步进中列车可能提前减速为0
            # 转移耗时
            time_used = (speed_next - state_now[1]) / acc
            # 转移能耗
            energy_used = 0.5 * self.mass * (speed_next + state_now[0]) * (speed_next - state_now[1]) if action == 0 else 0

            # 状态更新
            self.time += time_used
            self.energy += energy_used

            print('start at: ', self.state)
            # print('using time: ', time_used, ', energy: ', energy_used)
            self.state[0] = copy.deepcopy(distance_next)
            self.state[1] = copy.deepcopy(speed_next)
            print('using time {0:.2f}, and energy {1:.2f}, terminate at [{2}, {3:.2f}], total time {4:.2f} and energy {5:.2f}'.format(time_used, energy_used, self.state[0], self.state[1], self.time, self.energy))
            # print('terminate at: ', self.state, )

        else:
            print('stop', self.state)
            time_used = 0
            energy_used = 0
            print('using time {0:.2f}, and energy {1:.2f}, terminate at [{2}, {3:.2f}], total time {4:.2f} and energy {5:.2f}'.format(time_used, energy_used, self.state[0], self.state[1], self.time, self.energy))

        # 生成奖励信号及判断终止
        if self.state[0] == self.terminal:
            done = True
            if self.state[1] == 0:
                reward = 100
            else:
                reward = -100
        else:
            done = False
            reward = energy_used / 3600000  # 待完善

        return self.state, reward, done














    def render(self):  # 刷新函数，用于GUI显示
        pass


"""
自定义支持函数
"""
def descartes(x, y):  # 计算笛卡尔积
    # return [(x[i], y[j]) for i in range(len(x)) for j in range(len(y))]
    e = []
    for item in itertools.product(x, y):
        e.append(item)
    return e