import time
from queue import PriorityQueue
from collections import deque

class Solver:
    def __init__(self, initial_state, strategy, cutoff_depth=float('inf')):
        self.initial_state = initial_state
        self.strategy = strategy
        self.solution = None
        self.time = None
        self.expanded_states = 0
        self.generated_states = 0
        self.moves_to_goal = 0
        self.visited_states = set()
        self.cutoff_depth = cutoff_depth
        self.cutoff_heuristic_estimate = float('inf')

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

    def bfs(self):
        visited_states = set()
        queue = deque([(self.initial_state, [])])
        while queue:
            current_state, path = queue.popleft()  # Dequeue the current state and its path
            self.expanded_states += 1 # Increment the count of expanded states
            if current_state.check_solved():
                self.moves_to_goal = len(path)
                print("Number of moves to the target:", self.moves_to_goal)  # Print number of moves
                print("Number of expanded nodes:", self.expanded_states)  # Print number of expanded nodes
                print("Number of states generated:", self.generated_states)  # Print number of states generated
                return path
            if len(path) >= self.cutoff_depth:  # Prune branches beyond cutoff depth
                continue
            state_key = tuple(map(tuple, current_state.map))
            if state_key not in visited_states:
                visited_states.add(state_key) # Add the current state to the set of visited states
                self.generated_states += 1
                for action in current_state.get_possible_moves(): # Iterate over possible actions from the current state
                    next_state = current_state.move(action[0]) # Generate the next state by applying the action
                    if tuple(map(tuple, next_state.map)) not in visited_states:
                        queue.append((next_state, path + [action[0]]))
        return None


    def dfs(self):
        stack = deque([(self.initial_state, [])])  # Initialize stack with initial state and empty path
        visited = set()  # Initialize set to track visited states
        visited.add(tuple(map(tuple, self.initial_state.map)))  # Add initial state to visited set
        while stack:
            state, path = stack.pop()  # Get state and path from the top of the stack
            if len(path) > self.cutoff_depth:  # Check if cutoff depth is reached
                continue
            if state.check_solved():  # Check if the game is solved
                self.moves_to_goal = len(path)
                print("Number of moves to the target:", self.moves_to_goal)  
                print("Number of expanded nodes:", self.expanded_states)  
                print("Number of states generated:", self.generated_states)  
                return path
            for action in state.get_possible_moves():
                next_state = state.move(action[0])  # Generate next state by applying action
                if tuple(map(tuple, next_state.map)) not in visited:
                    stack.append((next_state, path + [action[0]]))  # Add next state and updated path to stack
                    visited.add(tuple(map(tuple, next_state.map)))  # Mark next state as visited
                    self.expanded_states += 1
                    self.generated_states += 1
        return []
    
    def ucs(self):
        priority_queue = PriorityQueue()
        priority_queue.put((0, [self.initial_state], []))  # Initialize priority queue with initial state and empty path
        visited_states = set()  # Initialize set to track visited states
        visited_states.add(tuple(map(tuple, self.initial_state.map)))  # Add initial state to visited set
        while not priority_queue.empty():
            cost, path, actions = priority_queue.get()  # Get cost, path, and actions from the priority queue
            state = path[-1]

            if len(path) > self.cutoff_depth:  # Check if cutoff depth is reached
                continue
            if state.check_solved():  # Check if the game is solved
                self.moves_to_goal = len(actions)
                print("Number of moves to the target:", self.moves_to_goal)
                print("Number of expanded nodes:", self.expanded_states)
                print("Number of states generated:", self.generated_states)
                return actions
            for action in state.get_possible_moves():
                next_state = state.move(action[0])  # Generate next state by applying action
                next_state_key = tuple(map(tuple, next_state.map))
                if next_state_key not in visited_states:
                    new_path = path + [next_state]
                    new_actions = actions + [action[0]]
                    next_cost = cost + 1  # Increment the cost by 1 for each step
                    priority_queue.put((next_cost, new_path, new_actions))  # Add next state and updated path to the priority queue with updated cost
                    visited_states.add(next_state_key)  # Mark next state as visited
                    self.expanded_states += 1
                    self.generated_states += 1
        return []


    def greedy(self):
        priority_queue = PriorityQueue()
        priority_queue.put((self.initial_state.get_heuristic(), [self.initial_state], []))  # Initialize priority queue with initial state and empty path
        visited_states = set()  # Initialize set to track visited states
        visited_states.add(tuple(map(tuple, self.initial_state.map)))  # Add initial state to visited set
        while not priority_queue.empty():
            _, path, actions = priority_queue.get()  # Get heuristic, path, and actions from the priority queue
            state = path[-1]
            if len(path) > self.cutoff_depth:  # Check if cutoff depth is reached
                continue
            if state.check_solved():  # Check if the game is solved
                self.moves_to_goal = len(actions)
                print("Number of moves to the target:", self.moves_to_goal)  
                print("Number of expanded nodes:", self.expanded_states)  
                print("Number of states generated:", self.generated_states) 
                return actions
            for action in state.get_possible_moves():
                next_state = state.move(action[0])  # Generate next state by applying action
                state_key = tuple(map(tuple, next_state.map))
                if state_key not in visited_states:
                    new_path = path + [next_state]
                    new_actions = actions + [action[0]]
                    priority_queue.put((next_state.get_heuristic(), new_path, new_actions))  # Add next state and updated path to the priority queue
                    visited_states.add(state_key)  # Mark next state as visited
                    self.expanded_states += 1
                    self.generated_states += 1
        return []


    def astar(self):
        queue = PriorityQueue()
        initial_total_cost = self.initial_state.get_total_cost()
        queue.put((initial_total_cost, [self.initial_state], [])) # Put initial state, path, and actions into the priority queue
        visited = set()
        visited.add(tuple(map(tuple, self.initial_state.map))) # Add initial state to visited set
        while not queue.empty():
            _, path, actions = queue.get()
            state = path[-1]
            if state.check_solved():
                self.moves_to_goal = len(actions)
                print("Number of moves to the target:", self.moves_to_goal)  
                print("Number of expanded nodes:", self.expanded_states)  
                print("Number of states generated:", self.generated_states)
                return actions
            for action in state.get_possible_moves():
                next_state = state.move(action[0])
                if tuple(map(tuple, next_state.map)) not in visited:
                    new_path = path + [next_state] # Update the path and actions with the new state and action
                    new_actions = actions + [action[0]]
                    queue.put((next_state.get_total_cost(), new_path, new_actions)) 
                    # Put the next state, total cost, and updated path/actions into the priority queue
                    visited.add(tuple(map(tuple, next_state.map)))
                    self.expanded_states += 1
                    self.generated_states += 1
        return []

    

    def custom(self):
        return ['U', 'U', 'D', 'D']

    def get_solution(self):
        return self.solution
