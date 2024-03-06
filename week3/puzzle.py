from queue import Queue

class PuzzleNode:
    def __init__(self, board, parent=None, action=None):
        # Initialize PuzzleNode attributes
        self.board = board
        self.parent = parent
        self.action = action

    def __eq__(self, other):
        # Implement equality comparison
        return self.board == other.board

    def __hash__(self):
        # Implement hash function
        return hash(str(self.board))

    def is_goal_state(self, goal_state):
        # Implement goal state check
        return self.board == goal_state

    def generate_neighbors(self):
        # Generate neighboring states
        neighbors = []
        blank_row, blank_col = self.get_blank_position()

        # if possible
        if blank_row > 0:
            # Move up
            neighbors.append(self.move_tile(blank_row - 1, blank_col, blank_row, blank_col))
        if blank_row < len(self.board) - 1:
            # Move down
            neighbors.append(self.move_tile(blank_row + 1, blank_col, blank_row, blank_col))
        if blank_col > 0:
            # Move left
            neighbors.append(self.move_tile(blank_row, blank_col - 1, blank_row, blank_col))
        if blank_col < len(self.board) - 1:
            # Move right
            neighbors.append(self.move_tile(blank_row, blank_col + 1, blank_row, blank_col))

        return neighbors

    def move_tile(self, row, col, new_row, new_col):
        # Move tiles to different locations and create a new PuzzleNode
        new_board = [row[:] for row in self.board]
        temp = new_board[row][col]
        new_board[row][col] = new_board[new_row][new_col]
        new_board[new_row][new_col] = temp
        return PuzzleNode(new_board, self, (row, col, new_row, new_col))

    def get_blank_position(self):
        # Get the position of the blank tile
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[row][col] == 0:
                    return row, col

def bfs(start_node, goal_state):
    # Breadth-first search algorithm
    visited = set()  # Set to store visited states
    queue = Queue()  # Queue to store nodes to be explored
    
    queue.put(start_node)

    while not queue.empty():
        current_node = queue.get()

        if current_node.is_goal_state(goal_state):
            # Reconstruct the path from the goal state to the start state
            path = []
            while current_node.parent is not None:
                path.append(current_node.action)
                current_node = current_node.parent
            path.reverse()
            return path

        visited.add(current_node)
        
        # Enqueue neighboring states for exploration
        for neighbor in current_node.generate_neighbors():
            if neighbor not in visited:
                queue.put(neighbor)

    return None

def print_solution(solution):
    if solution:
        print("Solution found:")
        current_board = start_state  # Initialize with the starting state
        print_board(current_board)

        # Apply each action in the solution path and print the board
        for step, action in enumerate(solution):
            current_board = apply_action(current_board, action)
            print(f"Step {step + 1}")
            print_board(current_board)
    else:
        print("No solution found.")

# Apply the given action to the current board
def apply_action(board, action):
    new_board = [row[:] for row in board]
    row, col, new_row, new_col = action
    temp = new_board[row][col]
    new_board[row][col] = new_board[new_row][new_col]
    new_board[new_row][new_col] = temp
    return new_board

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
    
    # Create the initial PuzzleNode
    start_node = PuzzleNode(start_state)
    
    # Find the solution path using breadth-first search
    solution = bfs(start_node, goal_state)

    print_solution(solution)
    print("Start state: ")
    print_board(start_state)
    print("Goal state: ")
    print_board(goal_state)
