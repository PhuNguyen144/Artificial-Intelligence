from queue import PriorityQueue

class PuzzleNode:
    def __init__(self, board, parent=None, action=None):
        self.board = board
        self.parent = parent
        self.action = action

    def __eq__(self, other):
        return self.board == other.board
    
    def __lt__(self, other):
        return self.board < other.board

    def __hash__(self):
        return hash(tuple(map(tuple, self.board)))

    def is_goal_state(self, goal_state):
        return self.board == goal_state

    def generate_neighbors(self):
        neighbors = []
        blank_i, blank_j = self.get_blank_position()

        for move in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_i, new_j = blank_i + move[0], blank_j + move[1]

            if 0 <= new_i < 3 and 0 <= new_j < 3:
                new_board = [row[:] for row in self.board]
                new_board[blank_i][blank_j], new_board[new_i][new_j] = new_board[new_i][new_j], new_board[blank_i][blank_j]
                neighbors.append(PuzzleNode(new_board, self, move))

        return neighbors

    def get_blank_position(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return i, j
    
    def hamming_distance(self, goal_state):
        # Implement Hamming distance heuristic
        distance = 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != 0 and self.board[i][j] != goal_state[i][j]:
                    distance += 1
        return distance

    def manhattan_distance(self, goal_state):
        # Implement Manhattan distance heuristic
        distance = sum(abs(i - goal_i) + abs(j - goal_j)
        for i, row in enumerate(self.board)
        for j, value in enumerate(row)
        if value != 0
        for goal_i, goal_row in enumerate(goal_state)
        for goal_j, goal_value in enumerate(goal_row)
        if value == goal_value)
        return distance
    
    
def astar(start_node, goal_state):
    visited = set()
    priority_queue = PriorityQueue()

    # Enqueue the start node with priority based on the heuristic values
    priority_queue.put((start_node.hamming_distance(goal_state), start_node))

    while not priority_queue.empty():
        current_node = priority_queue.get()[1]
        
        if current_node.is_goal_state(goal_state):
            # Return the path to the goal state
            path = []
            while current_node.parent is not None:
                path.insert(0, current_node.board)
                current_node = current_node.parent
            path.insert(0, start_node.board)
            return path

        visited.add(current_node)

        for neighbor in current_node.generate_neighbors():
            if neighbor not in visited:
                # Enqueue the neighbor with priority based on the heuristic values
                priority_queue.put((neighbor.hamming_distance(goal_state), neighbor))

    return None


def print_solution(solution):
    if solution:
        print("Solution found:")
        for step, board in enumerate(solution):
            print(f"Step {step + 1}:")
            print_board(board)
    else:
        print("No solution found.")

def print_board(board):
    for row in board:
        print(" ".join(map(str, row)))
    print()

if __name__ == "__main__":
    start_state = [
        [1, 2, 3],
        [4, 0, 5],
        [6, 7, 8]
    ]

    goal_state = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]

    start_node = PuzzleNode(start_state)

    solution = astar(start_node, goal_state)

    print_solution(solution)
