# # from datetime import datetime
#
# # # Giả sử bạn có hai chuỗi thời gian
# # time_str1 = "2023-11-10 15:55:58"
# # time_str2 = "2023-11-10 12:30:45"
# #
# # # Chuyển đổi chuỗi thành đối tượng datetime
# # time1 = datetime.strptime(time_str1, "%Y-%m-%d %H:%M:%S")
# # time2 = datetime.strptime(time_str2, "%Y-%m-%d %H:%M:%S")
# #
# # # Thực hiện phép trừ
# # time_difference = time1 - time2
# #
# # # Lấy tổng số giây chênh lệch
# # total_seconds = time_difference.total_seconds()
# #
# # # Tách giờ, phút và giây từ tổng số giây chênh lệch
# # hours, remainder = divmod(total_seconds, 3600)
# # minutes, seconds = divmod(remainder, 60)
# #
# # print(f"{hours} giờ, {minutes} phút, {seconds} giây")
# #
# # # Kiểm tra điều kiện và tăng biến count nếu thỏa mãn
# # count = 0
# # if hours > 3 or (hours == 3 and minutes > 10):
# #     count += 1
# #
# # # In kết quả
# # print(f"Kết quả: {count}")
# # from datetime import datetime
# import cv2
# import os
# import firebase_admin
# from firebase_admin import credentials, storage
#
# # Khởi tạo Firebase với tệp tin cấu hình đã tải từ Firebase Console
# cred = credentials.Certificate("serviceAccountKey.json")
# firebase_admin.initialize_app(cred, {'storageBucket':'fir-c20cd.appspot.com'})
#
# def capture_and_upload_image():
#     # Nhập tên từ người dùng
#     ID = input("Nhập ID: ")
#
#     # Tạo thư mục 'img' nếu nó chưa tồn tại
#     img_folder = "img"
#     if not os.path.exists(img_folder):
#         os.makedirs(img_folder)
#
#     # TODO: Thêm mã để chụp ảnh bằng OpenCV
#     # Ví dụ: sử dụng OpenCV để chụp ảnh từ webcam
#     cap = cv2.VideoCapture(0)
#     ret, frame = cap.read()
#     cap.release()
#
#     # Lưu ảnh vào thư mục với tên do người dùng nhập
#     img_path = os.path.join(img_folder, f"{ID}.jpg")
#     cv2.imwrite(img_path, frame)
#
#     # Upload ảnh lên Firebase Storage
#     bucket = storage.bucket()
#     image_blob = bucket.blob(f"images/{ID}.jpg")
#     image_blob.upload_from_filename(img_path)
#
#     # Lấy URL của ảnh sau khi upload
#     download_url = image_blob.public_url
#
#     # TODO: Liên kết URL với dữ liệu trong Firebase Database (nếu cần)
#
#     print("File available at", download_url)
#
#     # Xóa tệp tin tạm thời
#     os.remove(img_path)
#
# # Chạy hàm để chụp và upload ảnh
# capture_and_upload_image()
#
#
from collections import deque
import random
import networkx as nx
import matplotlib.pyplot as plt

INF = 1e9
paths = []


class Edge:
    def __init__(self, from_, to, capacity, cost):
        self.from_ = from_
        self.to = to
        self.capacity = capacity
        self.cost = cost


def printPath(path, f, d, t):
    print("____________________________________________________________________")
    print('Path:', ' -> '.join(map(str, path)))
    print('Flow sent on this path: ', f)
    print('Cost per flow on this path: ', d[t])
    print("____________________________________________________________________")


def drawGraph(edges):
    graph = nx.DiGraph()
    for e in edges:
        graph.add_edge(e.from_, e.to, weight=e.cost, capacity=e.capacity)
    pos = nx.spring_layout(graph)
    nx.draw_networkx(graph, pos, with_labels=True)
    cost = nx.get_edge_attributes(graph, "weight")
    capacity = nx.get_edge_attributes(graph, "capacity")
    labels = {}
    for e in cost.keys():
        labels[e] = str(cost[e]) + " / " + str(capacity[e])
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    plt.axis('off')
    plt.draw()
    plt.get_current_fig_manager().set_window_title("Graph")
    plt.show()


def shortest_paths(n, v0, adj, cost, capacity):
    d = [INF] * (n + 2)
    d[v0] = 0
    inq = [False] * (n + 2)
    q = deque([v0])
    p = [-1] * (n + 2)
    count = [0] * (n + 2)

    while q:
        u = q.popleft()
        inq[u] = False
        for v in adj[u]:
            if capacity[u][v] > 0 and d[v] > d[u] + cost[u][v]:
                d[v] = d[u] + cost[u][v]
                p[v] = u
                if not inq[v]:
                    q.append(v)
                    inq[v] = True
                    count[v] += 1
                    if count[v] > n:
                        return None

    return d, p


def min_cost_flow(N, edges, K, sources, sinks):
    print("Total Car: ", K)

    adj = [[] for _ in range(N + 2)]
    cost = [[0] * (N + 2) for _ in range(N + 2)]
    capacity = [[0] * (N + 2) for _ in range(N + 2)]
    s = N
    t = N + 1

    graph = nx.DiGraph()
    for e in edges:
        graph.add_edge(e.from_, e.to, weight=e.cost, capacity=e.capacity)
        adj[e.from_].append(e.to)
        adj[e.to].append(e.from_)
        cost[e.from_][e.to] = e.cost
        cost[e.to][e.from_] = -e.cost
        capacity[e.from_][e.to] = e.capacity

    for so in sources:
        adj[s].append(so)
        adj[s].append(s)
        cost[s][so] = 0
        cost[so][s] = 0
        capacity[s][so] = K

    for si in sinks:
        adj[si].append(t)
        adj[t].append(si)
        cost[s][so] = 0
        cost[so][s] = 0
        capacity[si][t] = K

    flow = 0
    cost_ = 0
    while flow < K:
        result = shortest_paths(N, s, adj, cost, capacity)
        if result is None:
            raise ValueError("Negative cycle detected")
        d, p = result
        if d[t] == INF:
            break;

        # find max flow on that path
        f = K - flow
        cur = t
        path = []
        while cur != s:
            f = min(f, capacity[p[cur]][cur])
            cur = p[cur]
            if cur != s:
                path.append(cur)
        # path.append(s)
        path = path[::-1]
        paths.append(path)
        # print shortest path and flow
        printPath(path, f, d, t)

        # apply flow
        flow += f
        cost_ += f * d[t]
        cur = t
        while cur != s:
            capacity[p[cur]][cur] -= f
            capacity[cur][p[cur]] += f
            cur = p[cur]

    if flow < K:
        return -1
    else:
        return cost_


def Stage_1():
    sources = [0, 1]
    sinks = [4]
    edges = []
    N = 5
    K = 13

    edges.append(Edge(0, 1, 10, 2))
    edges.append(Edge(0, 2, 5, 6))
    edges.append(Edge(1, 2, 15, 1))
    edges.append(Edge(1, 3, 9, 3))
    edges.append(Edge(2, 3, 10, 1))
    edges.append(Edge(2, 4, 10, 3))
    edges.append(Edge(3, 4, 5, 5))

    res = min_cost_flow(N, edges, K, sources, sinks)
    if res == -1:
        print('No Path Found')
    else:
        print("____________________________________________________________________")
        print("Path found: ")
        for path in paths:
            print(' -> '.join(map(str, path)))
        print('Total Cost: ', str(res))
        drawGraph(edges)


Stage_1()