import copy
import random
#Class to define an obj of each node of the next state for the puzzle
class Node:
    board = []
    rep_move = ''
    h = 0
    moves = 0
    empty_x = 0
    empty_y = 0
    prev_moves = []
    size = 0
    #constructor to define the state
    def __init__(self, size, board, parent = None) -> None:
        if parent is None:
            self.size  = size
            self.board = self.OnetoTwoD(board)
            self.empty_x, self.empty_y = self.find(0) #zero is the empty tile
            self.prev_moves = ["start"]
        else:
            self.board = copy.deepcopy(parent.board)
            self.empty_x = copy.deepcopy(parent.empty_x)
            self.empty_y = copy.deepcopy(parent.empty_y)
            self.moves = copy.deepcopy(parent.moves) + 1
            self.prev_moves = copy.deepcopy(parent.prev_moves)
            self.rep_move = copy.deepcopy(parent.rep_move)
        pass
    #auxillary function to convert 1D to 2D array of
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
    #auxillary func to find the tile 
    def find(self, tile):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == tile:
                    return j,i
        print("Can't find tile!")
    #move the tile for the puzzle
    def move(self, dir):
        x,y = self.empty_x, self.empty_y
        if dir == 'up':
            tile = self.board[y][x]
            self.board[y][x] = self.board[y-1][x]
            self.board[y-1][x] = tile
            self.empty_y = self.empty_y - 1
            self.prev_moves.append('up')
        elif dir == 'down':
            tile = self.board[y][x]
            self.board[y][x] = self.board[y+1][x]
            self.board[y+1][x] = tile
            self.empty_y = self.empty_y + 1
            self.prev_moves.append('down')
        elif dir == 'left':
            tile = self.board[y][x]
            self.board[y][x] = self.board[y][x-1]
            self.board[y][x-1] = tile
            self.empty_x = self.empty_x - 1
            self.prev_moves.append('left')
        elif dir == 'right':
            tile = self.board[y][x]
            self.board[y][x] = self.board[y][x+1]
            self.board[y][x+1] = tile
            self.empty_x = self.empty_x + 1
            self.prev_moves.append('right')
        else:
            print("Wrong Move!")
    #generate child nodes
    def generate_child_nodes(self):
        next_moves = []
        if self.empty_y != 0 and self.prev_moves[-1] != 'down':
            child = Node(0,None, self)
            child.move('up')
            next_moves.append(child)
        if self.empty_x != len(self.board)-1 and self.prev_moves[-1] != 'left':
            child = Node(0,None, self)
            child.move('right')
            next_moves.append(child)
        if self.empty_x != 0 and self.prev_moves[-1] != 'right':
            child = Node(0,None, self)
            child.move('left')
            next_moves.append(child)
        if self.empty_y != len(self.board)-1 and self.prev_moves[-1] != 'up':
            child = Node(0,None,self)
            child.move('down')
            next_moves.append(child)
        return next_moves

class Puzzle:
    #initialize the puzzle matrix
    def __init__(self,size) -> None:
        self.size = size
        self.done_states = []
        goal = list(range(1,(self.size*self.size)))
        goal.append(0)
        self.goal = self.OnetoTwoD(goal)
        pass
    #auxillary function to convert 1D to 2D array of
    #variable size
    def OnetoTwoD(self, arr):
        puzzle = []
        count = 0
        for _ in range(self.size):
            puzzle_row = []
            for _ in range(self.size):
                puzzle_row.append(arr[count])
                count += 1
            puzzle.append(puzzle_row)
        return puzzle
    #auxillary func to print the matrix
    def printMatrix(self,list):
        print("")
        for i in range(0,len(list)):
            for j in range(0,len(list[i])):
                print(list[i][j], end =" ")
            print()
    #heuristic 1: all incorrectly places tiles
    def h1(self,node):
        counter = 0
        for i in range(0,len(node.board)):
            for j in range(0,len(node.board[i])):
                if node.board[i][j] != self.goal[i][j]:
                    counter += 1
        return counter
    #heuristic 2: Manhattan distance
    def h2(self, node):
        val = 1
        dist = 0
        for i in range(len(node.board)):
            for j in range(len(node.board)):
                if val == self.size*self.size:
                    val = 0
                org_x, org_y = node.find(val)
                dist += abs(j - org_x) + abs(i - org_y)
                val += 1
        return dist
    #heuristic 3: Near neighbour
    def h3(self, node):
        start = node.board
        goal = self.goal
        dist = 0
        mult = 0    # The variable that stores how many direct reversal pairs there are
        pile = []
        puzz_dict_start = {}
        puzz_dict_goal = {}

        #-Indices which are each a key that refer to a list of neighbour indices
        if self.size == 3:
            indices = {
            0:[1,3],        1:[0,2,4],
            2:[1,5],        3:[4,0,6],
            4:[3,5,1,7],    5:[4,2,8],
            6:[7,3],        7:[6,8,4],
            8:[7,5] 
            }

        elif self.size == 4:
            indices = {
            0:[1,4], 1:[0,5,2], 2:[1,6,3], 3:[2,7],
            4:[0,5,8], 5:[1,4,9,6], 6:[2,5,7,10], 7:[3,6,11],
            8:[4,9,12], 9:[5,8,10,13], 10:[6,9,11,14], 11:[7,10,15],
            12:[8,13], 13:[9,12,14], 14:[10,13,15], 15:[11,14]
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
        
        for _ in pile:
            mult += 1
        mult = int((mult/2)) #Divided by two because there will always be double the amount of values in the pile list being counted
        dist += ((mult)*2)


        return dist
         
    
    #aux func: for counting inversions
    def getInversionCount(self,board):
        boardTemp = []
        for y in board:
            for x in y:
                boardTemp.append(x)
        count = 0
        for i in range(self.size*self.size - 1):
            for j in range(i+1,self.size*self.size):
                if boardTemp[j] and boardTemp[i] and boardTemp[i] > boardTemp[j]:
                    count += 1
        return count
    #aux func: get position of blank tile from bottom
    def findBlankTileBottom(self,board):
        for i in range(self.size-1,-1,-1):
            for j in range(self.size-1,-1,-1):
                if board[i][j] == 0:
                    return self.size - i
    #aux func: to see if the puzzle is solvable
    def isSolvable(self,board):
        inversion = self.getInversionCount(board)
        if self.size%2 == 1:
            return inversion%2 == 0
        else:
            pos = self.findBlankTileBottom(board)
            if (pos & 1):
                return ~(inversion & 1)
            else:
                return inversion & 1

    #this is the controller function
    def process(self,board):
        start = Node(self.size,board,None)
        start.h = self.h2(start)
        p_queue = [start]
        closed_dict = dict()
        while len(p_queue):
            
            current = p_queue.pop(0)
            '''
            print("**------------------------------**")
            self.printMatrix(current.board)
            print("Scores:")
            print("h value: ",current.h)
            print("steps: ",current.moves)
            total = (current.h + current.moves)
            print("combined: ", total)
            '''
            #to avoid repeats save the current node in a dict
            closed_dict[repr(current.board)] = current 
            #if solved
            if current.h == 0:
                #print(current.prev_moves)
                print("Number of steps: ", len(current.prev_moves)) #number of moves to solve 
                print("Number of Nodes visited: ",len(closed_dict)) # number of nodes visted
                return 1
            #check all nodes
            for option in current.generate_child_nodes():
                if repr(option.board) in closed_dict and self.isSolvable(option.board):
                    continue
                option.h = self.h2(option)
                p_queue.append(option)
            p_queue.sort(key=lambda x:(x.h+x.moves), reverse=False)
        return 0 #unsolved
class Solution:
    #constructor for saving size of puzzle
    def __init__(self,size) -> None:
        self.size = size
        pass
    #auxillary function to convert 1D to 2D array of
    #variable size
    def OnetoTwoD(self, arr):
        puzzle = []
        count = 0
        for _ in range(self.size):
            puzzle_row = []
            for _ in range(self.size):
                puzzle_row.append(arr[count])
                count += 1
            puzzle.append(puzzle_row)
        return puzzle
    #aux func: for counting inversions
    def getInversionCount(self,board):
        boardTemp = []
        for y in board:
            for x in y:
                boardTemp.append(x)
        count = 0
        for i in range(self.size*self.size - 1):
            for j in range(i+1,self.size*self.size):
                if boardTemp[j] and boardTemp[i] and boardTemp[i] > boardTemp[j]:
                    count += 1
        return count
    #aux func: get position of blank tile from bottom
    def findBlankTileBottom(self,board):
        for i in range(self.size-1,-1,-1):
            for j in range(self.size-1,-1,-1):
                if board[i][j] == 0:
                    return self.size - i
    #aux func: to see if the puzzle is solvable
    def isSolvable(self,board):
        inversion = self.getInversionCount(board)
        if self.size%2 == 1:
            return inversion%2 == 0
        else:
            pos = self.findBlankTileBottom(board)
            if (pos & 1):
                return ~(inversion & 1) 
            else:
                return inversion & 1 
    #this is to make an initial state for the puzzle
    def generate_states(self):
        not_solvable = True
        board = []
        num_of_tiles = self.size*self.size
        while not_solvable:
            open = list(range(0,num_of_tiles))
            board = []
            for i in range(0,num_of_tiles):
                index = random.randint(0,num_of_tiles-i-1)
                board.append(open.pop(index))
            
            puzzle = self.OnetoTwoD(board)
            if self.isSolvable(puzzle) and self.h2(puzzle)<10:
                not_solvable = False
                break

        return board
    #Manhattan distance
    def h2(self, node):
        val = 1
        dist = 0
        for i in range(len(node)):
            for j in range(len(node)):
                if val == self.size*self.size:
                    val = 0
                org_x, org_y = self.find(val,node)
                dist += abs(j - org_x) + abs(i - org_y)
                val += 1
        return dist
    #auxillary func to find the tile 
    def find(self, tile, node):
        for i in range(len(node)):
            for j in range(len(node)):
                if node[i][j] == tile:
                    return j,i
        print("Can't find tile!")
    #heuristic 1: all incorrectly places tiles
    def h1(self,node):
        goal = list(range(1,(self.size*self.size)))
        goal.append(0)
        goal = self.OnetoTwoD(goal)
        counter = 0
        for i in range(0,len(node)):
            for j in range(0,len(node[i])):
                if node[i][j] != goal[i][j]:
                    counter += 1
        return counter
if __name__ == "__main__":
    count = 0
    while count < 100:
        print("Puzzle #",count)
        p = Puzzle(3)
        s = Solution(3)
    #to_solve = [5,1, 2, 3, 9, 7, 11, 4, 13, 6, 15, 8, 14, 10, 0, 12]
    #to_solve = [3,15,7,11,13,5,0,9,2,4,10,12,6,8,14,1]
        to_solve = s.generate_states()
        p.process(to_solve)
        count += 1


            
            


    
