#Siyi Zhan
#862053955
#Uniform cost search 
#A* misplace Tile f(n)=h+g
#A* Edistance
#comments for oral exams and self-thinking 

import heapq # heappop and heappush, like pop() and push() for queue in C++
import copy 
import math 
from operator import add 

#The default puzzles model as professor gives, also for test
#Can be changed or modified or make it harder
#but not the first thing to do
trivial = [[1, 0, 2], [4, 5, 3], [7, 8, 6]] 

veryEasy = [[1, 2, 3],[4, 5, 6],[7, 0, 8]] 

easy = [[1, 2, 0],[4, 5, 3],[7, 8, 6]] 

doable = [[0, 1, 2], [4, 5, 3], [7, 8, 6]] 

oh_boy = [[8, 7, 1],[6, 0, 2],[5, 4, 3]]

impossible = [[1, 2, 3], [4, 5, 6], [8, 7, 0]]
                        
defaultFinalState = [[1, 2, 3],[4, 5, 6],[7, 8, 0]] #goal state default 
#Maybe players can enter their goal state for later GUI design


class Movement:
    def __init__(self, startState, goalState, moves):
        self.startState = startState
        self.goalState = goalState
        self.moves = moves

# Shows all possible directions of "0" up down left and right. 
directions = [[-1, 0], [ 1, 0], [ 0,-1], [ 0, 1]]

#######################################DEFAULT MODE###########################################
def defaultMode(): # default puzzles mode
#ask for user to choose which default mode he wants to play
    ModeChoices = input("Enter your choice of difficulty on a scale from 0 to 5.\n")
    #lists of choices
    if ModeChoices == "0":
            puzzle = Movement(trivial, defaultFinalState, directions)
            print("You choose puzzle trivial")
            for i in trivial:
                print(i)
            puzzle = Movement(trivial, defaultFinalState, directions)
    if ModeChoices == "1":
            puzzle = Movement(veryEasy, defaultFinalState, directions)
            print("You choose very easy puzzle")
            for i in veryEasy:
                print(i)
            puzzle = Movement(veryEasy, defaultFinalState, directions)
    if ModeChoices == "2":
            puzzle = Movement(easy, defaultFinalState, directions)
            print("You choose easy puzzle")
            for i in easy:
                print(i)
            puzzle = Movement(easy, defaultFinalState, directions)
    if ModeChoices == "3":
            puzzle = Movement(doable, defaultFinalState, directions)
            print("You choose medium puzzle")
            for i in doable:
                print(i)
            puzzle = Movement(doable, defaultFinalState, directions)
    if ModeChoices == "4":
            puzzle = Movement(oh_boy, defaultFinalState, directions)
            print("You choose hard puzzle")
            for i in oh_boy:
                print(i)
            puzzle = Movement(oh_boy, defaultFinalState, directions)
    if ModeChoices == "5":
            puzzle = Movement(impossible, defaultFinalState, directions)
            print("You choose impossible puzzle")
            for i in impossible:
                print(i)
            puzzle = Movement(impossible, defaultFinalState, directions)
    return puzzle

def StoreInList(list2d, value):
  for i, j in enumerate(list2d):
    if value in j:
      return [i, j.index(value)]
##################################### HELPER FUNCTION ##################################
#Helper function to get h(n)
def getHval(state, goalState):#Couting how many different spots are there comparing with goal puzzle
    h_Val = 0
    for i in range(0,3):
        for j in range(0,3):
            if state[i][j] != goalState[i][j] and state[i][j] != 0:
                h_Val += 1
    return h_Val
#Helper function to get the sum of the distances between each tile's current pos and goal pos
def getEdistance(state, goalState):
    distance = 0
    for i in range(1, len(state) * len(state[0])):
        currentPosition = tuple(StoreInList(state, i))
        goalPosition = tuple(StoreInList(goalState, i))
        distance += math.sqrt(sum([(a - b) ** 2 for a, b in zip(currentPosition, goalPosition)]))
    return distance

#Define a class to store the puzzle's attributes: state, level, faval and so on
#At first only have fval, however, hvalue is more useful to express fval
class Node:
    def __init__ (self, root, state, level, hValue):
        self.root = root
        self.state = state
        self.level = level # g(n)
        self.hValue = hValue # h(n)
        self.fValue = level + hValue # f(n) = g(n) + h(n)
    # override __lt__ for nodes to be ordered in the priority queue
    #the below is for lowest fval chosen
    def __lt__(self, other):
       return self.fValue < other.fValue

def trackBPath(node, generate_state):
    node = node.root
    if node != None: #not empty and move on
        generate_state.append(node.state)
        generate_state = trackBPath(node, generate_state)
    #states is generate_state
    #remember, all states now can not be added into visited, have to use list2d to convert
    return generate_state
################################### GENERATE CHILDE #######################################
#brainstorimg:
#after we know the directions, the methods of how to getFval and Hval, now we have to generate all possible nodes
#and according all above helper functions to know what goes next(like choose which node to be the next startState)
#Now implement generate_child
def generate_child(puzzle, AstarChoice):#generate all possible nodes according to userChoice 
    if AstarChoice == 1: # Uniform cost search
        firstNode = Node(None, puzzle.startState, 0, 0)
    elif AstarChoice == 2: # A* with Misplaced Tile heuristic
        firstNode = Node(None, puzzle.startState, 0, getHval(puzzle.startState, puzzle.goalState))
    else: # A* with Eucledian Distance heuristic
        firstNode = Node(None, puzzle.startState, 0, getEdistance(puzzle.startState, puzzle.goalState))
    frontier = []
    # use heapq to have the same functionality as open list where is waiting for visit
    heapq.heappush(frontier, firstNode)
    visited = set()
    while True:
        print("\nVisited ", len(visited), " node(s)")
        print("Frontier has ", len(frontier), " node(s)")
        #Valid situationcheck, if frontier is empty, take a break, post information.
        #it's better to have a error notice rather than break directly
        if len(frontier) == 0:
            Error = ["Sorry, it can't be solved"]
            return Error
        node = heapq.heappop(frontier)
        #f(n)=h(n)+g(n)
        #g(n) is the level of node
        #H(n) is calculated by GetH function
        #now we pop out the lowest f(n) -------------------------------A star
        if puzzle.goalState == node.state:
            print("\nAlready Visited ", len(visited), " nodes")
            print("\nStill has ", len(frontier), " nodes")
            generate_state = []
            generate_state.append(node.state)
            generate_state = trackBPath(node, generate_state)#go to check back path, like lecture "Traceback"
            return generate_state
       #Now states cannot be added into the visited yet
       #we have to use some helper function to convert list
       #after researching, tuple function matters attached in the report reference
        visited.add(tuple(tuple(i) for i in node.state))
        #now through tuple function, the states can be stored into visisted list

        print("The best state to expand with g(n) = ", node.level, 
              " and h(n) = ", node.hValue," is\n")
        for i in node.state:
            print(i)
        posOfZero = StoreInList(node.state, 0) #store zero position in the list

        # like shuffle function in main.cpp, which shows the movement of zero/blank:
        for i in puzzle.moves:
            #if we want to explore new position
            #while we don't want to ruin original state
            #make a copy for the postion
            #for latter movement swap
            pos = copy.copy(posOfZero)
            curState = copy.deepcopy(node.state)
            ##what happened after zero moves?
            newPos = list(map(add, i, pos)) # after movement, we have new zero position
            if newPos[0] >= 0 and newPos[0] < 3: 
                if newPos[1] >= 0 and newPos[1] < 3: #make sure that zero can not move over 3!!
                    pos = newPos
                else:
                    continue
            else:
                continue
#Now we have uploaded new possible postions for zero, after we know the newPos, we should let zero move to the newPos
            tempPos = curState[pos[0]][pos[1]] 
            curState[pos[0]][pos[1]] = 0
            curState[posOfZero[0]][posOfZero[1]] = tempPos

            haveNotVisited = None
            IsNotFrontNode = True
            # Now we have childNode
            if AstarChoice == 1:
                childNode = Node(node, curState, node.level + 1, 0)
            elif AstarChoice == 2:
                childNode = Node(node, curState, node.level + 1, getHval(curState, puzzle.goalState))
            else:
                childNode = Node(node, curState, node.level + 1, getEdistance(curState, puzzle.goalState))
            TupleChildNode = (tuple(tuple(i) for i in childNode.state))
            if TupleChildNode not in visited:
                haveNotVisited = True
            if len(frontier) == 0:
                IsNotFrontNode = True
            else:
                for i in frontier:
                    if childNode.state == i.state:
                        IsNotFrontNode = None
            if haveNotVisited and IsNotFrontNode:
                heapq.heappush(frontier, childNode)
#graph searching always confirm the goal state before removing 
            elif IsNotFrontNode == None:
                for i in frontier:
                    if childNode.state == i.state:
                        if childNode.fValue < i.fValue:#who is lower?
                            frontier.remove(i)#before confirm the goal state
                            heapq.heappush(frontier, childNode)#push the lowest fval to be waitted to visit!!!
                            
################################################# USER CHOICES ###########################################
#This function shows the userChoice and redirect to different algorithms according to userInteger
#call generate_child to show the all the children nodes

def userChoice(puzzle):
    algorithmChoices = input("Enter your choice of algorithm:\n" +
        "1: Uniform Cost Search\n" +
        "2: A* with the Misplaced Tile heuristic\n" +
        "3: A* with the Eucledian distance heuristic\n")
    if algorithmChoices == "1":
        print("Uniform Cost Search Mode Start:\n")
        allNodes = generate_child(puzzle, 1) ##All Nodes mean all possible nodes

        print ("This Algorithm takes ", len(allNodes)-1, "Moves. The steps are" + " below: \n")
        #show the steps 
        for i in allNodes[::-1]:
          for j in i:
              print(j)
          print("\n")
    if algorithmChoices == "2":
        print("A* with the Misplaced Tile heuristic Mode Start:\n")
        allNodes = generate_child(puzzle, 2)
        print ("This Algorithm takes ", len(allNodes)-1, "Moves. The steps are" + " below: \n")
        #show the process
        for i in allNodes[::-1]:
          for j in i:
              print(j)
          print("\n")
    if algorithmChoices == "3":
        print("A* with the Eucledian distance heuristic Mode Start:\n")
        allNodes = generate_child(puzzle, 3)
        print ("This Algorithm takes ", len(allNodes)-1, "Moves. The steps are" + " below: \n")
        for i in allNodes[::-1]:
          for j in i:
              print(j)
          print("\n")

######################################## START THE GAME ######################################################


def process():#Where I design the GUI and run the general request
    while True:
        userInteger = input("Welcome to Siyi's(862053955) 8-Puzzle Solver.\n" + "Type '1' to use a default puzzle.\n " +
        "Type '2' to enter your own puzzle\n" + "Type '0' to exist the program.\n") 
        if userInteger == "1": 
            print("Welcome to default puzzle mode.\n")
            userChoice(defaultMode())
  
        if userInteger == "2":
            print("Enter your puzzle, using '0' to represent the blank. " +
                  "Please only enter valid 8-puzzles. Use a space or a tab " +
                  "between the numbers." + '\n') 
            firstRow = input("Enter your first row: ") 
            secRow = input("Enter your second row: ") 
            thirdRow = input("Enter your third row: ") 
#when get the input, split it by space or tab that user entered
#The basic GUI is based on the sample that professor gives
#Can be modified if have more time to make it more enjoyable
            firstRow = firstRow.split() 
            secRow = secRow.split() 
            thirdRow = thirdRow.split() 
#generate_rows: To make it possible 
            for i in range(0, 3): 
                firstRow[i] = int(firstRow[i]) 
                secRow[i] = int(secRow[i]) 
                thirdRow[i] = int(thirdRow[i]) 
      #now we have the puzzle that User entered!
            userInput = [firstRow, secRow, thirdRow]
            for i in userInput:
                print (i)
            generated_input = Movement(userInput, defaultFinalState, directions)
            userChoice(generated_input)
         
        if userInteger == "0":
            print("Bye! See u again!")
            return
        # if userInteger != "0" & userInteger != "1" & userInteger != "2":
        #     print("Invalid mode, please exist with '0' and try again")

process() #start the game