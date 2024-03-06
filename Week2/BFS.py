from collections import defaultdict


class Graph:
    def __init__(self):
        self.graph = defaultdict(list)

    # Thêm cạnh vào graph
    def addEdge(self, u, v):
        self.graph[u].append(v)

    def BFS(self, start, end):
        visited = set()
        queue = [[start]]
        
        if start == end:
            return [start]
        
        while queue:
            path = queue.pop(0) #Nhận đường dẫn đầu tiên từ hàng đợi
            node = path[-1] #Lấy node cuối cùng từ đường dẫn

            if node not in visited:
                adjacent_nodes = self.graph[node] #Lấy các node lân cận của nút hiện tại
                for adjacent_node in adjacent_nodes:
                    new_path = list(path)
                    new_path.append(adjacent_node)
                    queue.append(new_path)

                    if adjacent_node == end:
                        return new_path

                visited.add(node)

        return "NO"
    

# Driver code
g = Graph()

# Đọc từ file input.txt
with open("C:\\Users\ADMIN\OneDrive\Máy tính\Project\CS300 - Artificial Intelligence\Week2\input.txt", "r") as file:
    N, M = map(int, file.readline().split())  # Đọc N và M từ dòng đầu tiên
    for line in file:
        u, v = map(int, line.strip().split())
        g.addEdge(u, v)
        g.addEdge(v, u)

result = g.BFS(3,6)

# Lưu kết quả vào file "output.txt"
with open("C:\\Users\ADMIN\OneDrive\Máy tính\Project\CS300 - Artificial Intelligence\Week2\output.txt", "w") as file:
    if result == "NO":
        file.write("NO")
    else:
        file.write(" ".join(map(str, result)))


