#Solve 8-puzzle with A*
#you can only use one heusterics  function a time.
#f(x) = h(x) + g(x)
from copy import deepcopy
from tkinter import N
from operator import attrgetter

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
                if self.data[i][j] == '0':
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

    def neighbour_nodes(puzz_dict_start, key):
        counter = 0

        #-number of neighbours in correspondence with the position of the key
        dict = {
            1:2 , 2:3 , 3:2 ,
            4:3 , 5:4 , 6:3 ,
            7:2 , 8:3 , 9:2
        }

        for x in puzz_dict_start.keys():
            counter += 1
            if x == key:
                return dict[counter]

        return
         
    
    #-f(x) = g(x) + h(x)
    def f(self,start, goal):
        return self.h2(start.data,goal) + start.moves
    
  

    #-process:
            #accept start and goal
            #place start node in an open list 
            #if reached goal node then break
            #sort open list based on f value
    def process(self):
        print("Start array")
        start = self.read()
        print("")
        print("Goal array")
        goal = self.read()
        print("")
        #Make a node of the start array 
        self.open.append(Node(0,start,0))
        not_solved = True
        steps = 0
        while not_solved:
            current = self.open[0]
            self.open = []
            #print the matrix
            print("**------------------------------**")
            print("")
            for i in range(0,len(current.data)):
                for j in range(0,len(current.data[i])):
                    print(current.data[i][j], end =" ")
                print("\n")

            if self.h2(current.data,goal) == 0:
                not_solved = False
                break
            steps += 1
            for option in current.generate_child_nodes():
                option.moves = steps
                option.f = self.f(option, goal)
                self.open.append(option)
            self.done.append(current)
            self.open.sort(key = attrgetter('f'), reverse=False)
        
if __name__ == "__main__":
    puz = Puzzle(3)
    puz.process()
    print("Solved \n")

"""
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
