import heapq
import sys
import pandas as pd
from collections import defaultdict

import pandas as pd
import numpy as np


class Graph:

    def __init__(self):
        self.vertices = {}

    def add_vertex(self, name, edges):
        self.vertices[name] = edges

    def shortest_path(self, start, finish):
        distances = {}  # Distance from start to node 从开始到节点的距离
        previous = {}  # Previous node in optimal path from source 最佳路径的前一个节点
        nodes = []  # Priority queue of all nodes in Graph 所有节点的优先序列

        for vertex in self.vertices:
            if vertex == start:  # Set root node as distance of 0
                distances[vertex] = 0
                heapq.heappush(nodes, [0, vertex])
            else:
                distances[vertex] = sys.maxsize
                heapq.heappush(nodes, [sys.maxsize, vertex])
            previous[vertex] = None

        while nodes:
            smallest = heapq.heappop(nodes)[1]  # Vertex in nodes with smallest distance in distances
            if smallest == finish:  # If the closest node is our target we're done so print the path
                path = []
                while previous[smallest]:  # Traverse through nodes til we reach the root which is 0
                    path.append(smallest)
                    smallest = previous[smallest]
                return path
            if distances[smallest] == sys.maxsize:  # All remaining vertices are inaccessible from source
                break

            for neighbor in self.vertices[smallest]:  # Look at all the nodes that this vertex is attached to
                alt = distances[smallest] + self.vertices[smallest][neighbor]  # Alternative path distance
                if alt < distances[neighbor]:  # If there is a new shortest path update our priority queue (relax)
                    distances[neighbor] = alt
                    previous[neighbor] = smallest
                    for n in nodes:
                        if n[1] == neighbor:
                            n[0] = alt
                            break
                    heapq.heapify(nodes)

        return distances

    def __str__(self):
        return str(self.vertices)


if __name__ == '__main__':
    g = Graph()
    df = pd.read_excel('29个节点数据.xlsx', na_values='inf')
    Distance = np.empty((29, 29), dtype='object')
    for i in range(0, 29):
        for j in range(0, 29):
            Distance[i, j] = df.loc[i][j + 1]
    for a in range(29):
        S = defaultdict(list)
        for b in range(29):
            if pd.isna(Distance[a, b]):
                continue
            elif Distance[a, b] == 0:
                continue
            else:
                k = b + 1
                S[k] = Distance[a, b]
        g.add_vertex(a + 1, S)
    # min = np.zeros((29, 29))
    # for x in range(1, 30):
    #     for y in range(1, 30):
    #         a = g.shortest_path(x, y)
    #         a.append(x)
    #         a.reverse()
    #         # 这里是输出路径
    #         print(a)
    #         for m in range(len(a) - 1):
    #             min[x - 1, y - 1] = min[x - 1, y - 1] + Distance[a[m] - 1, a[m + 1] - 1]
    # print(min)
    x1 = 19
    y1 = 27
    k = g.shortest_path(x1, y1)
    k.append(x1)
    k.reverse()
    juli = 0
    for xx in range(len(k) - 1):
        juli += Distance[k[xx] - 1, k[xx + 1] - 1]
    print(k)
    print(juli)

