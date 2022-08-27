import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import xlrd
# 创建图
G = nx.Graph()

# 增加节点
G.add_nodes_from(
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29])
data = xlrd.open_workbook('fujian3.xls')
table = data.sheet_by_name(u'Sheet1')  # 通过名称获取
# step2:给上述空图加边
start = []
to = []
value = []
e=[]
for qidian in range(0, 29):
    for zhongdian in range(qidian, 29):
        if table.cell(qidian, zhongdian).value != 'inf' and table.cell(qidian, zhongdian).value !=0.0:
            start.append(qidian+1)
            to.append(zhongdian+1)
            value.append(table.cell(qidian, zhongdian).value)
            # e.append((G.nodes[qidian], G.nodes[zhongdian], table.cell(qidian, zhongdian).value * 10))
            e.append((qidian+1,zhongdian+1,table.cell(qidian, zhongdian).value))
print(e)
# 增加权重，数据格式（节点1，节点2，权重）
# e = [(1, 2, 6), (2, 3, 2), (1, 3, 1), (3, 4, 7), (4, 5, 9), (5, 6, 3), (4, 6, 3)]
for k in e:
    G.add_edge(k[0], k[1], weight=k[2])

# 普通的画图方式
# nx.draw(G, with_labels=True)

# 生成节点位置序列
pos = nx.spring_layout(G)

# 重新获取权重序列
weights = nx.get_edge_attributes(G, "weight")
node_color=[]
for i in range(0,29):
    if i in {4,13,18,26}:
        node_color.append('red')
    elif i in {5,12,17,21}:
        node_color.append('yellow')
    else:
        node_color.append('lightblue')
# 画节点图
nx.draw_networkx(G, pos, with_labels=True,node_size = 200,font_size=12,node_color=node_color)
# 画权重图
nx.draw_networkx_edge_labels(G, pos, edge_labels=weights)

# 展示
plt.show()
