#Solve 8-puzzle with A*
#you can only use one heusterics  function a time.
#f(x) = h(x) + g(x)
from copy import deepcopy
from tkinter import N
from operator import attrgetter
import random
import numpy

#initialize a node class
class Node:
    #-initialize the node
    def __init__(self,moves,data,f) -> None:
        #print("init")
        self.moves = moves
        self.data = data
        self.f = f

    #-generate the child nodes, the empty block 
    #can be replaced by 
    def generate_child_nodes(self):
        #print("kids")
        #get the indices of the empty square
        x,y = self.find()
        #list of possible moves: down, up, left, right
        pos_moves = [[x,y-1],[x,y+1],[x-1,y],[x+1,y]]
        child_node_list = []
        for move in pos_moves:
            child = self.move(x,y,move[0],move[1])
            if child is not None:
                child_node = Node(self.moves, child, 0)
                child_node_list.append(child_node)
        return child_node_list

    #-find the blank space
    def find(self):
        #print("find")
        for i in range(0,len(self.data)):
            for j in range(0,len(self.data[i])):
                if self.data[i][j] == 0:
                    return i,j

    #-copy the puzzle matrix
    def copy(self):
        #print("copy")
        return deepcopy(self.data)

    #-move the square in intended directions and
    #check for out of bounds
    def move(self,blank_x,blank_y,x,y):
        #print("move")
        if x >= 0 and y >= 0  and y < len(self.data) and x < len(self.data):
            puzz = []
            puzz = self.copy()
            #make the switch 
            tile = puzz[x][y]
            puzz[x][y] = puzz[blank_x][blank_y]
            puzz[blank_x][blank_y] = tile
            return puzz
        else:
            return None

#initialize a puzzle class
class Puzzle:
    #-Initialize the puzzle
    def __init__(self, size) -> None:
        self.size = size
        self.done = []
        self.open = []
    #-read puzzle from the user
    def read(self):
        print("Enter puzzle rows: Ex:'1 2 3'")
        print("")
        puzz = []
        for i in range(0,self.size):
            row = input().split(" ")
            puzz.append(row)
        return puzz

    #-define h(x) -- number of matching tiles
    def h1(self,start,goal):
        counter = 0
        for i in range(0,len(start)):
            for j in range(0,len(start[i])):
                if start[i][j] != goal[i][j]:
                    counter += 1
        return counter
    def h2(self, start, goal):
        dist = 0
        puzz_dict_start = {}
        puzz_dict_goal = {}
        for i in range(0,len(start)):
            for j in range(0,len(start[i])):
                puzz_dict_start[start[i][j]] = [i,j]
                puzz_dict_goal[goal[i][j]] = [i,j]
        for key in puzz_dict_start.keys():
            dist += abs(puzz_dict_start[key][0] - puzz_dict_goal[key][0]) + abs(puzz_dict_start[key][1] - puzz_dict_goal[key][1])

        return dist
    
    #-define h(x) -- Direct Adjacent Reversal Heuristic (Checks if neighbours are direct reversals in terms of goal state coordinates)
    def h3(self, start, goal):
        dist = 0
        mult = 0    # The variable that stores how many direct reversal pairs there are
        pile = []
        puzz_dict_start = {}
        puzz_dict_goal = {}

        #-Indices which are each a key that refer to a list of neighbour indices
        indices = {
            0:[1,3],        1:[0,2,4],
            2:[1,5],        3:[4,0,6],
            4:[3,5,1,7],    5:[4,2,8],
            6:[7,3],        7:[6,8,4],
            8:[7,5] 
        }

        for i in range(0,len(start)):
            for j in range(0,len(start[i])):
                puzz_dict_start[start[i][j]] = [i,j]
                puzz_dict_goal[goal[i][j]] = [i,j]

        #Manhattan Distance (h2)
        for key in puzz_dict_start.keys():
            dist += abs(puzz_dict_start[key][0] - puzz_dict_goal[key][0]) + abs(puzz_dict_start[key][1] - puzz_dict_goal[key][1])

        
        for num in range(0, len(puzz_dict_start.keys())):         #Iterates through index of keys in a list
            for key in indices.keys():                            #Iterates through key in indices dictionary
                if num == key:                                    #-If index of the key in the start matrix is equal to the indice indicated key in the indice dictionary
                    for neighbour in indices[key]:                #-Then for each neighbour within the (indice) key
                            if (list(puzz_dict_start.keys())[num]) == (list(puzz_dict_goal.keys())[neighbour]) and (list(puzz_dict_start.keys())[neighbour]) == (list(puzz_dict_goal.keys())[num]):
                                # Start             Goal
                                # 1 2 3            1 2 3
                                # 4 0 5            4 0 5
                                # 6 7 8            6 8 7
                                #
                                #   (1) This if statement is checking if 7 (start state) is equal to its neighbours (8) key (7) in the goal state and vice versa
                                #   (2) if it is, then it is added to the pile list in order to collect the direct reversal pairs for a final count

                                pile.append(neighbour) 


        for value in pile:
            mult += 1
        mult = int((mult/2)) #Divided by two because there will always be double the amount of values in the pile list being counted
        dist += ((mult)*2)


        return dist
         
    
    #-f(x) = g(x) + h(x)
    def f(self,start, goal):
        return self.h3(start.data,goal) + start.moves
    
    #-auxillary function to convert 1D to 2D array of
    #variable size
    def OnetoTwoD(self, arr):
        puzzle = []
        count = 0
        for row in range(self.size):
            puzzle_row = []
            for col in range(self.size):
                puzzle_row.append(arr[count])
                count += 1
            puzzle.append(puzzle_row)
        return puzzle
  
    def printMatrix(self,list):
        print("")
        for i in range(0,len(list)):
            for j in range(0,len(list[i])):
                print(list[i][j], end =" ")
            print("\n")

    def notvisited(self,node):
        for mat in self.done:
            if mat.data == node:
                return 0
        return 1



    def getInvCount(self,arr):
        arr1=[]
        N = self.size
        for y in arr:
            for x in y:
                arr1.append(x)
        arr=arr1
        inv_count = 0
        for i in range(N * N - 1):
            for j in range(i + 1,N * N):
                # count pairs(arr[i], arr[j]) such that
                # i < j and arr[i] > arr[j]
                if (arr[j] and arr[i] and arr[i] > arr[j]):
                    inv_count+=1
            
        return inv_count


    # find Position of blank from bottom
    def findXPosition(self,puzzle):
        N = self.size
        # start from bottom-right corner of matrix
        for i in range(N - 1,-1,-1):
            for j in range(N - 1,-1,-1):
                if (puzzle[i][j] == 0):
                    return N - i


    # This function returns true if given
    # instance of N*N - 1 puzzle is solvable
    def isSolvable(self,puzzle):
        # Count inversions in given puzzle
        invCount = self.getInvCount(puzzle.data)
        # If grid is odd, return true if inversion
        # count is even.
        if (self.size & 1):
            return ~(invCount & 1)

        else: # grid is even
            pos = self.findXPosition(puzzle.data)
            if (pos & 1):
                return ~(invCount & 1)
            else:
                return invCount & 1

    #-process:
            #accept start and goal
            #place start node in an open list 
            #if reached goal node then break
            #sort open list based on f value
    def process(self,start):
        start = self.OnetoTwoD(start)
        goal = self.OnetoTwoD(list(range(0,(self.size*self.size))))
        print("Goal Matrix is:")
        self.printMatrix(goal)
        #Make a node of the start array 
        self.open.append(Node(0,start,0))
        not_solved = True
        steps = 0
        while not_solved:
            if len(self.open) != 0:
                current = self.open.pop(0)
            else:
                print("Sorry, tried ",steps," steps could not solve the problem")
                return 0
            #print the matrix
            print("**------------------------------**")
            self.printMatrix(current.data)
            print("step: ",current.moves)
            if self.h3(current.data,goal) == 0:
                not_solved = False
                break
            for option in current.generate_child_nodes():
                option.moves = current.moves + 1
                option.f = self.f(option, goal)
                if self.notvisited(option.data) and self.isSolvable(option):
                    self.open.append(option)
                else:
                    print(option.data)
                    print("not visited ",self.notvisited(option.data), " solvable: ",self.isSolvable(option))
                
            self.done.append(current)
            self.open.sort(key = attrgetter('f'), reverse=False)
        print("Solved \n")
        return 1
class Solution:
    def __init__(self,location) -> None:
        self.location = location
        pass
    #generate states - generate hundred states of a given puzzle problem. 
    #input: n value and number of states
    def generate_states(self, n):
        not_solvable = True
        board = []
        num_of_tiles = n*n
        while not_solvable:
            open = list(range(0,num_of_tiles))
            board = []
            for i in range(0,num_of_tiles):
                index = random.randint(0,num_of_tiles-i-1)
                board.append(open.pop(index))
            
            puzzle = self.OnetoTwoD(board,n)
            if self.isSolvable(puzzle,n):
                not_solvable = False
                break

        return board

 
    def OnetoTwoD(self, arr,n):
        puzzle = []
        count = 0
        size = n
        for row in range(size):
            puzzle_row = []
            for col in range(size):
                puzzle_row.append(arr[count])
                count += 1
            puzzle.append(puzzle_row)
        return puzzle

    def getInvCount(self,arr,N):
        arr1=[]
        for y in arr:
            for x in y:
                arr1.append(x)
        arr=arr1
        inv_count = 0
        for i in range(N * N - 1):
            for j in range(i + 1,N * N):
                # count pairs(arr[i], arr[j]) such that
                # i < j and arr[i] > arr[j]
                if (arr[j] and arr[i] and arr[i] > arr[j]):
                    inv_count+=1
            
        return inv_count


    # find Position of blank from bottom
    def findXPosition(self,puzzle,N):
        # start from bottom-right corner of matrix
        for i in range(N - 1,-1,-1):
            for j in range(N - 1,-1,-1):
                if (puzzle[i][j] == 0):
                    return N - i


    # This function returns true if given
    # instance of N*N - 1 puzzle is solvable
    def isSolvable(self,puzzle,n):
        # Count inversions in given puzzle
        invCount = self.getInvCount(puzzle,n)
        # If grid is odd, return true if inversion
        # count is even.
        if (n%2 == 1):
            return (invCount%2 == 0)

        else: # grid is even
            pos = self.findXPosition(puzzle,n)
            if (pos%2 == 1):
                return not(invCount%2 == 1)
            else:
                return invCount & 1


     
        
if __name__ == "__main__":
    sol = Solution("temp")
    all_sols = []
    count = 0
    total_count = 0
    not_solv = []
    n = 3
    while count < 10:
        to_solve = sol.generate_states(n)
        #to_solve = [10,5,13,4,14,6,15,3,8,12,2,1,7,11,9,0]
        print("Will use A* to solve")
        print(to_solve)
        puz = Puzzle(n)
        total_count += 1
        if puz.process(to_solve) == 1:
            all_sols.append(to_solve)
            count += 1
        else:
            not_solv.append(to_solve)
        
    print("done")


"""
[1,2,3,4,0,5,8,6,7]
Start array
Enter puzzle rows: Ex:'1 2 3'

0 1 3
4 2 5
7 8 6

Goal array
Enter puzzle rows: Ex:'1 2 3'

1 2 3
4 5 6
7 8 0

**------------------------------**

0 1 3 

4 2 5 

7 8 6 

**------------------------------**

1 0 3 

4 2 5 

7 8 6 

**------------------------------**

1 2 3 

4 0 5 

7 8 6 

**------------------------------**

1 2 3 

4 5 0 

7 8 6 

**------------------------------**

1 2 3 

4 5 6 

7 8 0 

Solved 
"""
