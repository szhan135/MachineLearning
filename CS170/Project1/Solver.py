import heapq # Used for the priority queue
import copy # Used to copy list of lists
import math # Used for Eucledian Distance heuristic calculation
from operator import add # Used for Misplaced Tile heuristic calculation

trivial = [[1, 2, 3], 
           [4, 5, 6], 
           [7, 8, 0]] 
veryEasy = [[1, 2, 3],
            [4, 5, 6],
            [7, 0, 8]] 
veryEasy2 = [[1, 2, 3], 
            [4, 8, 5], 
            [7, 0, 6]] 
easy = [[1, 2, 0],
        [4, 5, 3],
        [7, 8, 6]] 
doable = [[0, 1, 2], 
          [4, 5, 3], 
          [7, 8, 6]] 
oh_boy = [[8, 7, 1],
          [6, 0, 2],
          [5, 4, 3]]
impossible = [[1, 2, 3], 
              [4, 5, 6], 
              [8, 7, 0]] 

eightGoalState = [[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 0]]

failure = ["Impossible to solve"]

# Move blank instead of moving numbers
blankOperations = [[-1, 0], # move blank up
                   [ 1, 0], # move blank down
                   [ 0,-1], # move blank left
                   [ 0, 1]] # move blank right

class Node:
    def __init__ (self, parent, state, cost, estDistance):
        self.parent = parent
        self.state = state
        self.cost = cost # g(n)
        self.estDistance = estDistance # h(n)
        self.solutionCost = cost + estDistance # f(n) = g(n) + h(n)
    # override __lt__ for nodes to be ordered in the priority queue
    def __lt__(self, other):
       return self.solutionCost < other.solutionCost


class Puzzle:
    def __init__(self, initialState, goalState, operations):
        self.initialState = initialState
        self.goalState = goalState
        self.operations = operations

def getIndex2dList(list2d, value):
  for i, j in enumerate(list2d):
    if value in j:
      return [i, j.index(value)]

def default_puzzle_init(): # Initialize preset puzzles (copied from sample)
    puzzle_algorithm = input("Enter your choice of difficulty on a scale from 0 to 5.\n")
    if puzzle_algorithm == "0":
            puzzle = Puzzle(trivial, eightGoalState, blankOperations)
            print("Starting puzzle: trivial")
            for i in trivial:
                print(i)
            puzzle = Puzzle(trivial, eightGoalState, blankOperations)
    if puzzle_algorithm == "1":
            puzzle = Puzzle(veryEasy, eightGoalState, blankOperations)
            print("Starting puzzle: very easy")
            for i in veryEasy:
                print(i)
            puzzle = Puzzle(veryEasy, eightGoalState, blankOperations)
    if puzzle_algorithm == "2":
            puzzle = Puzzle(easy, eightGoalState, blankOperations)
            print("Starting puzzle: easy")
            for i in easy:
                print(i)
            puzzle = Puzzle(easy, eightGoalState, blankOperations)
    if puzzle_algorithm == "3":
            puzzle = Puzzle(doable, eightGoalState, blankOperations)
            print("Starting puzzle: medium")
            for i in doable:
                print(i)
            puzzle = Puzzle(doable, eightGoalState, blankOperations)
    if puzzle_algorithm == "4":
            puzzle = Puzzle(oh_boy, eightGoalState, blankOperations)
            print("Starting puzzle: hard")
            for i in oh_boy:
                print(i)
            puzzle = Puzzle(oh_boy, eightGoalState, blankOperations)
    if puzzle_algorithm == "5":
            puzzle = Puzzle(impossible, eightGoalState, blankOperations)
            print("Starting puzzle: impossible")
            for i in impossible:
                print(i)
            puzzle = Puzzle(impossible, eightGoalState, blankOperations)
    return puzzle

def misTile(state, goalState):
    # Compare current state and goal state and calculate how many
    # tiles are out of place (not in their goal positions)
    heuristic = 0
    if state[0][0] != goalState[0][0]:
        heuristic += 1
    if state[0][1] != goalState[0][1]:
        heuristic += 1
    if state[0][2] != goalState[0][2]:
        heuristic += 1
    if state[1][0] != goalState[1][0]:
        heuristic += 1
    if state[1][1] != goalState[1][1]:
        heuristic += 1
    if state[1][2] != goalState[1][2]:
        heuristic += 1
    if state[2][0] != goalState[2][0]:
        heuristic += 1
    if state[2][1] != goalState[2][1]:
        heuristic += 1
    return heuristic

def eucDis(state, goalState):
    # Calculate the sum of the distances between each tile's current
    # position and its goal position
    distance = 0
    for i in range(1, len(state) * len(state[0])):
        currentPosition = tuple(getIndex2dList(state, i))
        goalPosition = tuple(getIndex2dList(goalState, i))
        distance += math.sqrt(sum([(a - b) ** 2 for a, b in zip(currentPosition, goalPosition)]))
    return distance

def traceBack(node, states):
    node = node.parent
    if node != None:
        states.append(node.state)
        states = traceBack(node, states)
    return states

def searchHolder(puzzle, algorithm):
    # The search algorithm, implement uniform cost, A* with Misplaced Tile heuristic
    # or A* with Eucledian Distance heuristic depending on arguments passed in
    if algorithm == 1: # Uniform cost search
        firstNode = Node(None, puzzle.initialState, 0, 0)
    elif algorithm == 2: # A* with Misplaced Tile heuristic
        firstNode = Node(None, puzzle.initialState, 0, misTile(puzzle.initialState, puzzle.goalState))
    else: # A* with Eucledian Distance heuristic
        firstNode = Node(None, puzzle.initialState, 0, eucDis(puzzle.initialState, puzzle.goalState))
    frontier = []
    # Push the first node to the frontier (priority queue)
    heapq.heappush(frontier, firstNode)
    explored = set()
    while True:
        print("\nExplored ", len(explored), " node(s)")
        print("Frontier has ", len(frontier), " node(s)")
        
        if len(frontier) == 0:
            return failure
        
        # Pop the node in frontier with lowest (path cost + estimated distance to goal)
        node = heapq.heappop(frontier)
        if puzzle.goalState == node.state:
            print("\nSuccess\nExplored ", len(explored), " node(s)")
            print("Frontier has ", len(frontier), " node(s)")
            # Traceback
            states = []
            states.append(node.state)
            states = traceBack(node, states)
            return states
        # Convert list of lists to tuple of tuple to be added to set
        explored.add(tuple(tuple(i) for i in node.state))
        
        print("The best state to expand with g(n) = ", node.cost, 
              " and h(n) = ", node.estDistance," is\n")
        for i in node.state:
            print(i)
        # Get position of the blank tile
        blankIndex = getIndex2dList(node.state, 0)
        # Try movement operations on the blank tile
        for i in puzzle.operations:
            # Have to make a copy to not modify the original index and state (lists)
            index = copy.copy(blankIndex)
            tempState = copy.deepcopy(node.state)
            moved = list(map(add, i, index)) # blank tile index after operation
            if moved[0] >= 0 and moved[0] <= 2: # illegal states check
                if moved[1] >= 0 and moved[1] <= 2: # illegal states check
                    index = moved;
                else:
                    continue
            else:
                continue
            # Swap blank tile and the tile on the new position, 
            # there is probably a more Pythonic way of doing this
            temp = tempState[index[0]][index[1]] 
            tempState[index[0]][index[1]] = 0
            tempState[blankIndex[0]][blankIndex[1]] = temp

            notInExplored = None
            notInFrontier = True
            # Generate a child node
            if algorithm == 1:
                child = Node(node, tempState, node.cost + 1, 0)
            elif algorithm == 2:
                child = Node(node, tempState, node.cost + 1, misTile(tempState, puzzle.goalState))
            else:
                child = Node(node, tempState, node.cost + 1, eucDis(tempState, puzzle.goalState))
            childTuple = (tuple(tuple(i) for i in child.state))
            # Check if child node has been explored
            if childTuple not in explored:
                notInExplored = True
            # Check if child node is in frontier
            if len(frontier) == 0:
                notInFrontier = True
            else:
                for i in frontier:
                    if child.state == i.state:
                        notInFrontier = None
            if notInExplored and notInFrontier:
                heapq.heappush(frontier, child)
            # If child node is in frontier but has a higher cost,
            # update with the new cost/node
            elif notInFrontier == None:
                for i in frontier:
                    if child.state == i.state:
                        if child.solutionCost < i.solutionCost:
                            frontier.remove(i)
                            heapq.heappush(frontier, child)

def select_algorithm(puzzle):
    puzzle_algorithm = input("Enter your choice of algorithm.\n" +
        "Enter \"1\" to use Uniform Cost Search\n" +
        "Enter \"2\" to use A* with the Misplaced Tile heuristic\n" +
        "Enter \"3\" to use A* with the Eucledian distance heuristic\n")
    if puzzle_algorithm == "1":
        print("You selected Uniform Cost Search\n")
        result = searchHolder(puzzle, 1)
        print ("The solution path cost is", len(result)-1, ". The following is the" +
               "trace back of the solution:\n")
        for i in result[::-1]:
          for j in i:
              print(j)
          print("\n")
    if puzzle_algorithm == "2":
        print("You selected A* with the Misplaced Tile heuristic\n")
        result = searchHolder(puzzle, 2)
        print ("The solution path cost is", len(result)-1, ". The following is the" +
               "trace back of the solution:\n")
        for i in result[::-1]:
          for j in i:
              print(j)
          print("\n")
    if puzzle_algorithm == "3":
        print("You selected A* with the Eucledian distance heuristic\n")
        result = searchHolder(puzzle, 3)
        print ("The solution path cost is", len(result)-1, ". The following is the" +
               "trace back of the solution:\n")
        for i in result[::-1]:
          for j in i:
              print(j)
          print("\n")

def main():
    while True:
        # Input validation is not implemented, assuming user will only enter valid input
        puzzle_mode = input("Welcome to an 8-Puzzle Solver.\n" +
        "Enter \"1\" to use a default puzzle, or \"2\" to enter your own puzzle. " +
        "Enter \"3\" to exit.\n") 
        if puzzle_mode == "1": 
            print("You selected default puzzle.\n")
            select_algorithm(default_puzzle_init())
  
        if puzzle_mode == "2":
            # Referenced the sample project
            print("Enter your puzzle, using a zero to represent the blank. " +
                  "Please only enter valid 8-puzzles. Type the puzzle with a space " +
                  "between the numbers." + '\n') 
            puzzle_row_one = input("Enter the first row: ") 
            puzzle_row_two = input("Enter the second row: ") 
            puzzle_row_three = input("Enter the third row: ") 

            puzzle_row_one = puzzle_row_one.split() 
            puzzle_row_two = puzzle_row_two.split() 
            puzzle_row_three = puzzle_row_three.split() 
    
            for i in range(0, 3): 
                puzzle_row_one[i] = int(puzzle_row_one[i]) 
                puzzle_row_two[i] = int(puzzle_row_two[i]) 
                puzzle_row_three[i] = int(puzzle_row_three[i]) 
      
            user_puzzle_state = [puzzle_row_one, puzzle_row_two, puzzle_row_three]
            for i in user_puzzle_state:
                print (i)
            user_puzzle = Puzzle(user_puzzle_state, eightGoalState, blankOperations)
            select_algorithm(user_puzzle)
         
        if puzzle_mode == "3":
            return

main()