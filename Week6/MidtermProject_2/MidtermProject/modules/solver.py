import time
from queue import PriorityQueue
from collections import deque

class Solver:
    def __init__(self, initial_state, strategy,cutoff_depth=float('inf')):
        self.initial_state = initial_state
        self.strategy = strategy
        self.solution = None
        self.time = None
        self.expanded_states = 0
        self.generated_states = 0
        self.moves_to_goal = 0
        self.visited_states = set()
        self.cutoff_depth = cutoff_depth
        self.cutoff_heuristic_estimate=float('inf')

    def solve(self):
        start_time = time.time()
        if self.strategy == 'bfs':
            self.solution = self.bfs()
            print("BFS Solution Path:", self.solution)  # Print the final path
        elif self.strategy == 'dfs':
            self.solution = self.dfs()
            print("DFS Solution Path:", self.solution)  # Print the final path
        elif self.strategy == 'ucs':
            self.solution = self.ucs()
            print("UCS Solution Path:", self.solution)  # Print the final path
        elif self.strategy == 'greedy':
            self.solution = self.greedy()
            print("Greedy Solution Path:", self.solution)  # Print the final path
        elif self.strategy == 'astar':
            self.solution = self.astar()
            print("A* Solution Path:", self.solution)  # Print the final path
        self.time = time.time() - start_time
        print("Time taken:", round(self.time, 3), "seconds")  # Print the time taken

    # Add print statements to each method to print the final path
    def bfs(self):
        print("Number of states generated:", self.generated_states)
        print("Number of expanded nodes:", self.expanded_states)
        print("Number of moves to the target:", self.moves_to_goal)
        queue = deque([(self.initial_state, [])])
        while queue:
            current_state, path = queue.popleft()
            self.expanded_states += 1
            if current_state.check_solved():
                self.moves_to_goal = len(path)
                return path
            if len(path) >= self.cutoff_depth:  # Prune branches beyond cutoff depth
                continue
            state_key = tuple(map(tuple, current_state.map))
            if state_key not in self.visited_states:
                self.visited_states.add(state_key)
                self.generated_states += 1
                for action in current_state.get_possible_moves():
                    next_state = current_state.move(action[0])
                    if tuple(map(tuple, next_state.map)) not in self.visited_states:
                        queue.append((next_state, path + [action[0]]))
        return None

    def dfs(self):
        stack = deque([(self.initial_state, [])])  # Khởi tạo stack với trạng thái ban đầu và đường dẫn rỗng
        while stack:
            state, path = stack.pop()  # Lấy trạng thái và đường dẫn từ đỉnh của stack
            if len(path) > self.cutoff_depth:  # Kiểm tra xem đã đạt đến độ sâu cắt hay chưa
                continue
            if state.check_solved():  # Kiểm tra xem trò chơi đã được giải quyết chưa
                self.moves_to_goal = len(path)
                return path
            state_key = tuple(map(tuple, state.map))
            if state_key not in self.visited_states:
                self.visited_states.add(state_key)
                self.expanded_states += 1
                for action in state.get_possible_moves():
                    next_state = state.move(action[0])  # Tạo trạng thái tiếp theo bằng cách di chuyển
                    self.generated_states += 1
                    stack.append((next_state, path + [action[0]]))  # Thêm trạng thái tiếp theo và đường dẫn cập nhật vào stack
        return []


    

    def ucs(self):
        print("Number of states generated:", self.generated_states)
        print("Number of expanded nodes:", self.expanded_states)
        print("Number of moves to the target:", self.moves_to_goal)
        priority_queue = PriorityQueue()
        priority_queue.put((0, self.initial_state, []))  # Khởi tạo hàng đợi ưu tiên với trạng thái ban đầu và đường dẫn rỗng
        while not priority_queue.empty():
            cost, state, path = priority_queue.get()  # Lấy trạng thái và đường dẫn từ hàng đợi ưu tiên
            if len(path) > self.cutoff_depth:  # Kiểm tra xem đã đạt đến độ sâu cắt hay chưa
                continue
            if state.check_solved():  # Kiểm tra xem trò chơi đã được giải quyết chưa
                self.moves_to_goal = len(path)
                return path
            state_key = tuple(map(tuple, state.map))
            if state_key not in self.visited_states:
                self.visited_states.add(state_key)
                self.expanded_states += 1
                for action in state.get_possible_moves():
                    next_state = state.move(action[0])  # Tạo trạng thái tiếp theo bằng cách di chuyển
                    self.generated_states += 1
                    priority_queue.put((next_state.get_total_cost(), next_state, path + [action[0]]))  # Thêm trạng thái tiếp theo và đường dẫn cập nhật vào hàng đợi ưu tiên
        return []
    
    

    def greedy(self):
        print("Number of states generated:", self.generated_states)
        print("Number of expanded nodes:", self.expanded_states)
        print("Number of moves to the target:", self.moves_to_goal)
        priority_queue = PriorityQueue()
        priority_queue.put((self.initial_state.get_heuristic(), self.initial_state, []))  # Khởi tạo hàng đợi ưu tiên với ước lượng heuristic của trạng thái ban đầu và đường dẫn rỗng
        while not priority_queue.empty():
            heuristic, state, path = priority_queue.get()  # Lấy ước lượng heuristic, trạng thái và đường dẫn từ hàng đợi ưu tiên
            if len(path) > self.cutoff_depth:  # Kiểm tra xem đã đạt đến độ sâu cắt hay chưa
                continue
            if state.check_solved():  # Kiểm tra xem trò chơi đã được giải quyết chưa
                self.moves_to_goal = len(path)
                return path
            state_key = tuple(map(tuple, state.map))
            if state_key not in self.visited_states:
                self.visited_states.add(state_key)
                self.expanded_states += 1
                for action in state.get_possible_moves():
                    next_state = state.move(action[0])  # Tạo trạng thái tiếp theo bằng cách di chuyển
                    self.generated_states += 1
                    priority_queue.put((next_state.get_heuristic(), next_state, path + [action[0]]))  # Thêm trạng thái tiếp theo và đường dẫn cập nhật vào hàng đợi ưu tiên
        return []
    


    def astar(self):
        print("Number of states generated:", self.generated_states)
        print("Number of expanded nodes:", self.expanded_states)
        print("Number of moves to the target:", self.moves_to_goal)
        queue = PriorityQueue()
        initial_total_cost = self.initial_state.get_total_cost()
        queue.put((initial_total_cost, [self.initial_state], []))
        while not queue.empty():
            _, path, actions = queue.get()
            state = path[-1]
            if state.check_solved():
                return actions
            state_key = tuple(map(tuple, state.map))
            if state_key not in self.visited_states:
                self.visited_states.add(state_key)
                for action in state.get_possible_moves():
                    next_state = state.move(action[0])
                    if tuple(map(tuple, next_state.map)) not in self.visited_states:
                        new_path = path + [next_state]
                        new_actions = actions + [action[0]]
                        # Improved heuristic estimation using a better heuristic function
                        heuristic_estimate = next_state.get_heuristic()
                        # Pruning branches by discarding those with high heuristic estimates
                        if heuristic_estimate < self.cutoff_heuristic_estimate:
                            queue.put((next_state.get_total_cost() + heuristic_estimate, new_path, new_actions))
        return []


    def custom(self):
        return ['U', 'U', 'D', 'D']

    def get_solution(self):
        return self.solution
