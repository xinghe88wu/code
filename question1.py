import math

import numpy as np
import xlrd


def read_xls(hang, lie, name, sheet_name):
    data = xlrd.open_workbook(name)
    table = data.sheet_by_name(sheet_name)  # 通过名称获取
    need = np.zeros((hang[1] - hang[0] + 1, lie[1] - lie[0] + 1))
    for i in range(hang[0], hang[1] + 1):
        for j in range(lie[0], lie[1] + 1):
            need[i - hang[0]][j - lie[0]] = table.cell(i, j).value
    return need


# 读取最短路径表distance
distance = read_xls([0, 28], [0, 28], 'distance.xls', '最短距离')
# print(distance)
che_distance = [3.7, 13.6, 11.7, 11.2]
che_chongdian = [2.1, 3.6, 2.3, 2.4]
chongdian_1 = [5.8, 12.4, 9.4, 13.6]
# 读取负荷需求表need
need = read_xls([0, 10], [1, 4], 'need.xls', 'Sheet1')
# print(need)

price = read_xls([0, 10], [6, 6], 'need.xls', 'Sheet1')

# 读取车辆数目表che
che = read_xls([0, 6404], [0, 7], 'excel_test.xls', 'Test')
# print(che)
# for i in range(0, 6405):
i = 0
# print(che[0])
# time_all=[]
p = 512
for i in range(0, 6404):
    time = []  # 记录派车时间
    for j in range(0, 8):
        if j % 2 == 1:
            continue
        if che[i][j] == 0:
            time1 = 0
            for m in range(0, math.floor(che[i][j + 1])):
                # 没有小车，只有大车,不用判断功率，直接算
                c = 0  # 初始化车用电量为0
                for k in range(time1, 11):  # 遍历need，不能继续供电为止
                    if c + need[k][math.floor(j / 2)] > 400:
                        time.append((k, math.floor(j / 2), 1))  # 第math.floor(j / 2)个台区变需要在k点之前有车来,1表示大车
                        time1 = k
                        break
                    if k == 5 and need[5][math.floor(j / 2)] == 0 and math.floor(che[i][j + 1]) > 1:
                        time.append((k + 1, math.floor(j / 2), 1))
                        time1 = k + 1
                        break
                    if k == 6 and need[6][math.floor(j / 2)] == 0 and math.floor(che[i][j + 1]) > 1:
                        time.append((k + 1, math.floor(j / 2), 1))
                        time1 = k + 1
                        break

                    c = c + need[k][math.floor(j / 2)]
                    need[k][math.floor(j / 2)] = 0
                    # if k==10:
                    #     # 1台区变的完成了
                    #     time_all.append(time)
        elif che[i][j + 1] == 0:
            time1 = 0
            for m in range(0, math.floor(che[i][j])):
                # 没有小车，只有大车，不用判断功率，直接算
                c = 0  # 初始化车用电量为0
                for k in range(time1, 11):  # 遍历need，不能继续供电为止
                    if c + need[k][math.floor(j / 2)] > 200:
                        time.append((k, math.floor(j / 2), 0))  # 第math.floor(j / 2)个台区变需要在k点之前有车来,0表示小车
                        time1 = k
                        break
                    if k == 5 and need[5][math.floor(j / 2)] == 0 and math.floor(che[i][j]) > 1:
                        time.append((k + 1, math.floor(j / 2), 0))
                        time1 = k + 1
                        break
                    c = c + need[k][math.floor(j / 2)]
                    need[k][math.floor(j / 2)] = 0
                    # if k==10:
                    #     # 1台区变的完成了
                    #     time_all.append(time)
        else:
            big_car = che[i][j + 1]
            small_car = che[i][j]
            time1 = 0
            for m in range(0, math.floor(che[i][j + 1])):
                # 优先派大车
                c = 0  # 初始化车用电量为0
                for k in range(time1, 11):  # 遍历need，不能继续供电为止
                    if c + need[k][math.floor(j / 2)] > 400:
                        time.append((k, math.floor(j / 2), 1))  # 第math.floor(j / 2)个台区变需要在k点之前有车来,0表示小车
                        time1 = k
                        break
                    if k == 5 and need[5][math.floor(j / 2)] == 0 and math.floor(che[i][j]) > 1:
                        time.append((k + 1, math.floor(j / 2), 0))
                        time1 = k + 1
                        break
                    c = c + need[k][math.floor(j / 2)]
                    need[k][math.floor(j / 2)] = 0
                    if k == 10:
                        # 1台区变的完成了
                        time1 = 11
                        # time_all.append(time)

            for n in range(0, math.floor(che[i][j])):
                # 大车派完派小车
                c = 0  # 初始化车用电量为0
                for k in range(time1, 11):  # 遍历need，不能继续供电为止
                    if need[k][math.floor(j / 2)] > 50:
                        break
                    if c + need[k][math.floor(j / 2)] > 200:
                        time.append((k, math.floor(j / 2), 0))  # 第math.floor(j / 2)个台区变需要在k点之前有车来,0表示小车
                        time1 = k
                        break
                    if k == 5 and need[5][math.floor(j / 2)] == 0 and math.floor(che[i][j]) > 1:
                        time.append((k + 1, math.floor(j / 2), 0))
                        time1 = k + 1
                        break
                    c = c + need[k][math.floor(j / 2)]
                    need[k][math.floor(j / 2)] = 0
                    # if k == 10:
                    #     # 1台区变的完成了
                    #     time_all.append(time)
    money = 0
    if np.all(need == 0) and time != []:
        # 调度可行，输出费用
        num_che = np.zeros((4, 2))
        for num in time:
            if num[1] == 0:
                if num[2] == 0:
                    num_che[0][0] = num_che[0][0] + 1
                else:
                    num_che[0][1] = num_che[0][1] + 1
            elif num[1] == 1:
                if num[2] == 0:
                    num_che[1][0] = num_che[1][0] + 1
                else:
                    num_che[1][1] = num_che[1][1] + 1
            elif num[1] == 2:
                if num[2] == 0:
                    num_che[2][0] = num_che[2][0] + 1
                else:
                    num_che[2][1] = num_che[2][1] + 1
            else:
                if num[2] == 0:
                    num_che[3][0] = num_che[3][0] + 1
                else:
                    num_che[3][1] = num_che[3][1] + 1

        for mo in range(len(num_che)):
            # 去各个台区变的路费
            money = money - num_che[mo][0] * (che_distance[mo] + che_chongdian[mo] + chongdian_1[mo]) - num_che[mo][
                1] * 2 * (che_distance[mo] + che_chongdian[mo] + chongdian_1[mo])
        need = read_xls([0, 10], [1, 4], 'need.xls', 'Sheet1')

        time_0_shijian = []
        time_1_shijian = []
        time_2_shijian = []
        time_3_shijian = []
        for num in time:
            if num[1] == 0:
                time_0_shijian.append(num)
            elif num[1] == 1:
                time_1_shijian.append(num)
            elif num[1] == 2:
                time_2_shijian.append(num)
            elif num[1] == 3:
                time_3_shijian.append(num)

        for num in time:
            kuai = 0
            kuai0 = 0
            time_p = num[0]
            for yuan in range(0, math.floor(time_p)):
                kuai = need[yuan][math.floor(num[1])] + kuai
            money = money - price[math.floor(time_p)] * kuai
            if num[1] == 0:
                kuai0 = 557.3 - kuai
            elif num[1] == 1:
                kuai0 = 500 - kuai
            elif num[1] == 2:
                kuai0 = 276 - kuai
            else:
                kuai0 = 403 - kuai

            money = money - kuai0 * 0.8

            # print(kuai)
            # print(need)
        money = money + 1750.222

        time.append((0, 0, 1))
        time.append((3, 1, 0))
        time.append((3, 2, 0))
        time.append((3, 3, 1))
        print("调度策略如下")
        print(time)

        # print(time_all)
        # print(need)
        print("最佳收益为")
        print(money)
        print('\n')
