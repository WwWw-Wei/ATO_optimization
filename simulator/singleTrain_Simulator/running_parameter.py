"""
线路参数：站间距离、计划时间、坡道设置、限速设置等
车辆参数：列车质量、牵引制动性能、Davis系数等
"""

# 线路参数

DISTANCE = 1275  # 区间1距离
TRIP_TIME = 100  # 区间1计划时间
GRADIENT_CHANGE = [178, 200, 221, 507, 623, 1036, 1106, 1275]  # 区间1坡道变更点
SPEED_LIMITATION_POINT = [155, 1120]  # 区间1限速点
SPEED_LIMITATION = [16.7, 22.2]


# 列车参数
MASS = 280000  # Kg
TRACTION = 0.8  # m/s^2
BRAKE = -1  # m/s^2
DAVIS_A = 2.75  # 质量阻力系数
DAVIS_B = 0.014  # 机械阻力系数
DAVIS_C = 0.00075  # 空气阻力系数



def getGradient(x):  # 区间1坡度
    if x <= 178:
        gradient = 0
    elif x <= 200:
        gradient = -1
    elif x <= 221:
        gradient = -2
    elif x <= 507:
        gradient = -3
    elif x <= 623:
        gradient = 0
    elif x <= 1036:
        gradient = 2
    elif x <= 1106:
        gradient = 1
    else:
        gradient = 0
    return gradient

# def getGradient(i):  # 区间2坡度
#     if i <= 132:
#         gradient = 0
#     elif i <= 209:
#         gradient = 1
#     elif i <= 363:
#         gradient = 3
#     elif i <= 948:
#         gradient = 2
#     elif i <= 1005:
#         gradient = 1
#     elif i <= 1327:
#         gradient = 0
#     elif i <= 1367:
#         gradient = 2
#     elif i <= 1455:
#         gradient = 12
#     elif i <= 2013:
#         gradient = 22
#     elif i <= 2207:
#         gradient = 18
#     elif i <= 2265:
#         gradient = 15
#     elif i <= 2317:
#         gradient = 5
#     elif i <= 2368:
#         gradient = 1
#     else:
#         gradient = 0



