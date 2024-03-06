from collections import defaultdict

class Graph:
    def __init__(self):
        self.graph = defaultdict(list)
        self.visited = set()
        self.result = []  # Thêm danh sách để lưu kết quả

    def addEdge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    def DFS(self, s):
        # Kiểm tra đỉnh đã được thăm chưa
        if s not in self.visited:
            print(s, end=' ')
            self.visited.add(s)
            self.result.append(s)  # Thêm đỉnh vào danh sách kết quả

            # Duyệt qua các đỉnh kề của đỉnh s
            for neighbor in self.graph[s]:
                self.DFS(neighbor)
                
    def saveResultToFile(self, filename):
        with open(filename, "w") as f:
            for vertex in self.result:
                f.write(str(vertex) + "\n")
                
# Driver code
g = Graph()

# Đọc từ file "input.txt"
with open("C:\\Users\ADMIN\OneDrive\Máy tính\Project\CS300 - Artificial Intelligence\Week2\input.txt", "r") as f:
    N, M = map(int, f.readline().split())
    for line in f:
        u, v = map(int, line.strip().split())
        g.addEdge(u, v)
        g.addEdge(v, u)

# Gọi hàm DFS với đỉnh bắt đầu là n
g.DFS(6)

# Lưu kết quả vào file "output.txt"
g.saveResultToFile("C:\\Users\ADMIN\OneDrive\Máy tính\Project\CS300 - Artificial Intelligence\Week2\output.txt")