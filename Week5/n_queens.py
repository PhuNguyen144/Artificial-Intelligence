import random
import copy
import math

class NQueensStateNode:
    def __init__(self, initialState):
        self.state = initialState # list of queen positions for each column
        self.nQueen = len(initialState) #number of queens
        self.cRow = dict() # number of queens on the same row i
        self.cDiagonal1 = dict() # number of queens on the same diagonal1
        self.cDiagonal2 = dict() # number of queens on the same diagonal2
        
    def printState(self):
        print(' '.join(str(r) for r in self.state))

    # Count the number of queens in each row and diagonal
    def countQueenList(self):
        # Reset counters
        self.cRow = dict()
        self.cDiagonal1 = dict()
        self.cDiagonal2 = dict()

        # Iterate through columns
        for col in range(self.nQueen):
            row = self.state[col]
            # Update counters
            self.cRow[row] = self.cRow.get(row, 0) + 1
            self.cDiagonal1[row - col] = self.cDiagonal1.get(row - col, 0) + 1
            self.cDiagonal2[row + col] = self.cDiagonal2.get(row + col, 0) + 1
    
    # Calculate the heuristic value of the current state
    def getHeuristic(self):
        self.countQueenList()
        heuristic = 0

        # Calculate heuristic based on queens in the same row and diagonals
        for count in self.cRow.values():
            heuristic += count * (count - 1) // 2

        for count in self.cDiagonal1.values():
            heuristic += count * (count - 1) // 2

        for count in self.cDiagonal2.values():
            heuristic += count * (count - 1) // 2

        return heuristic

    # Find the best successor state with the lowest heuristic value
    def getBestSuccessor(self):
        bestState = None
        bestHeuristic = math.inf

        # Iterate through columns and rows to find the best successor
        for col in range(self.nQueen):
            for row in range(self.nQueen):
                if self.state[col] != row:
                    nextState = copy.deepcopy(self.state)
                    nextState[col] = row
                    nextStateNode = NQueensStateNode(nextState)
                    heuristic = nextStateNode.getHeuristic()
                    if heuristic < bestHeuristic:
                        bestState = nextState
                        bestHeuristic = heuristic

        return bestState

    # Find the first choice successor state with a lower heuristic value
    def getFirstChoice(self):
        candidates = []
        currentHeuristic = self.getHeuristic()
        
        # Iterate through columns and rows to find first choice successor
        for col in range(self.nQueen):
            for row in range(self.nQueen):
                if self.state[col] != row:
                    nextState = copy.deepcopy(self.state)
                    nextState[col] = row
                    nextStateNode = NQueensStateNode(nextState)
                    heuristic = nextStateNode.getHeuristic()
                    if heuristic < currentHeuristic:
                        candidates.append(nextState)

        if candidates:
            return random.choice(candidates)
        else:
            return None

    # Generate a random state with n queens
    @staticmethod
    def getRandomState(nQueen):
        state = list(range(nQueen))
        random.shuffle(state)
        return state


    # Perform hill climbing algorithm to find a solution
    @staticmethod
    def HillClimbing(state):
        currentStateNode = NQueensStateNode(state)
        currentHeuristic = currentStateNode.getHeuristic()

        print("Initial State:")
        currentStateNode.printState()
        print("Initial Heuristic:", currentHeuristic)

        while True:
            bestSuccessor = currentStateNode.getBestSuccessor()
            if bestSuccessor is None:
                break

            successorNode = NQueensStateNode(bestSuccessor)
            successorHeuristic = successorNode.getHeuristic()

            if successorHeuristic >= currentHeuristic:
                break

            currentStateNode = successorNode
            currentHeuristic = successorHeuristic

            print("Next State:")
            currentStateNode.printState()
            print("Heuristic:", currentHeuristic)

        return currentStateNode.state


    # Perform hill climbing algorithm with first choice selection to find a solution
    @staticmethod
    def HillClimbingFirstChoice(state):
        currentStateNode = NQueensStateNode(state)
        currentHeuristic = currentStateNode.getHeuristic()

        print("Initial State:")
        currentStateNode.printState()
        print("Initial Heuristic:", currentHeuristic)

        while True:
            bestSuccessor = currentStateNode.getFirstChoice()
            if bestSuccessor is None:
                break

            successorNode = NQueensStateNode(bestSuccessor)
            successorHeuristic = successorNode.getHeuristic()

            if successorHeuristic >= currentHeuristic:
                break

            currentStateNode = successorNode
            currentHeuristic = successorHeuristic

            print("Next State:")
            currentStateNode.printState()
            print("Heuristic:", currentHeuristic)

        return currentStateNode.state


    # Perform hill climbing algorithm with random restarts to find a solution
    @staticmethod
    def HillClimbingRandomRestart(state):
        restarts = 0
        while True:
            print("Restart:", restarts + 1)
            initialState = NQueensStateNode.getRandomState(state)
            finalState = NQueensStateNode.HillClimbing(initialState)
            if NQueensStateNode(finalState).getHeuristic() == 0:
                return finalState
            restarts += 1


if __name__ == '__main__':
    
    # Example usage of the NQueensStateNode class and its methods
    
    # Run hill climbing algorithm with initial state [2, 3, 0, 1]
    finalState = NQueensStateNode.HillClimbing([2, 3, 0, 1])
    print("Final State:")
    NQueensStateNode(finalState).printState()

    # Run hill climbing algorithm with a randomly generated initial state of size 4
    initialState = NQueensStateNode.getRandomState(4)
    finalState = NQueensStateNode.HillClimbingFirstChoice(initialState)
    print("Final State:")
    NQueensStateNode(finalState).printState()

    # Run hill climbing algorithm with random restarts for a board of size 4
    finalState = NQueensStateNode.HillClimbingRandomRestart(4)
    print("Final State:")
    NQueensStateNode(finalState).printState()