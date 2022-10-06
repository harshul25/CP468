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
        for i in range(0,self.size-1):
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

    #-f(x) = g(x) + h(x)
    def f(self,start, goal):
        return self.h1(start.data,goal) + start.moves

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

            if self.h(current.data,goal) == 0:
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
    puz = Puzzle(4)
    puz.process()
    print("Solved \n")