import heapq
import Queue
import time
start_time = time.time()
#                                                                                           --------------------------------------------
#A : starting                                                                               -----HELLO HELLO WELCOME TO CYBERSPACE------
#B : ending                                                                                 --------------------------------------------
#r : roads            1
#g : grasslands       5
#f : forests         10
#m : mountains       50
#w : water          100

#=======================boards==========================================================
#the text files must be in the same folder.
#Can use read_map method to generate string

board1 = "board-2-1.txt"
board2 = "board-2-2.txt"
board3 = "board-2-3.txt"
board4 = "board-2-4.txt"

#for printing to terminal
board = []

#========================Support Functions===============================================

def read_map(file_string):                          #This method reads a file that is in the same
    mapstring = ""                                  #folder and return it as a string.
    with open(file_string) as f:
        for line in f:
            mapstring = mapstring + line.strip()
        f.closed
    return mapstring

def makeEmptyGrid(grid_width,grid_height):
    for x in range(grid_width):
        board.append([0] * grid_height)

def retreive_closed_list(closed_set):               #Putting the closed list in a set
    coordinates = set()                             #for easier retrieval
    while len(closed_set):
        cell = closed_set.pop()
        coordinates.add((cell.x, cell.y))
    return coordinates

def retreive_open_list(open_list):                  #Putting the open list in a set
    coordinates = set()                             #for easier retrieval
    while len(open_list):
        f, cell = open_list.pop()
        coordinates.add((cell.x, cell.y))
    return coordinates

def output(board, open_set, closed_set):            #This method outputs to terminal

    for x in xrange(len(board)):
            for y in xrange(10):
                if board[x][y]=='*' or board[x][y]=='A' or board[x][y] =='B':
                    continue
                if (x, y) in open_set:
                    board[x][y] = '+'
                if (x, y) in closed_set:
                    board[x][y] = '-'

    for i in xrange(len(board)):
        print board[i]

    print "There are %d nodes in the open list" % (len(open_set))
    print "There are %d nodes in the closed list" % (len(closed_set))



#=====================MAPS_AS_String====================================================

map1 = read_map(board1)
map2 = read_map(board2)
map3 = read_map(board3)
map4 = read_map(board4)


#=========================THE_MAIN_CLASSES==============================================

class Cell(object):                                             #Each tile on the map is
    def __init__(self, x, y, cell_type, g_cost):                #Cell objects
        self.cell_type = cell_type                              #cell type can be: r ,g ,f ,m or w.
        self.x = x
        self.y = y
        self.parent = None
        self.g = g_cost
        self.h = 0
        self.f = 0

class AStar(object):

    def __init__(self):
        self.opened = []
        heapq.heapify(self.opened)
        self.open_list = []
        self.closed = set()
        self.cells = []
        self.grid_height = 10
        self.grid_width = 40

    def init_grid(self):
        #Making an empty matrix of the same size as the board, for view.
        makeEmptyGrid(self.grid_width,self.grid_height)
        grid_width = 40
        grid_height = 10

        #Making a matrix 10x40 to represent the board.
        #The dimesions are opposite in order to make accesibility easier.
        #The access is by [x][y]
        w, h = 10, 40
        grid = [[None] * w for i in xrange(h)]

        #These loops takes the mapstring and turns it into a coordinate system of list
        for x in xrange(grid_width):
            for y in xrange(grid_height):                                                #Change map in the if statements: map1,map2,map3 or map4
                if map1[grid_width*(grid_height-y-1) + x] == 'r':                        #<---------------------------
                    grid[x][y] = 'r'
                    cell_type = 'r'
                    g_cost = 1
                    board[x][y] = 'r'

                if map1[grid_width*(grid_height-y-1) + x] == 'g':
                    grid[x][y] = 'g'
                    cell_type = 'g'
                    g_cost = 5
                    board[x][y] = 'g'

                if map1[grid_width*(grid_height-y-1) + x] == 'f':
                    grid[x][y] = 'f'
                    cell_type = 'f'
                    g_cost = 10
                    board[x][y] = 'f'

                if map1[grid_width*(grid_height-y-1) + x] == 'm':
                    grid[x][y] = 'm'
                    cell_type = 'm'
                    g_cost = 50
                    board[x][y] = 'm'

                if map1[grid_width*(grid_height-y-1) + x] == 'w':
                    grid[x][y] = 'w'
                    cell_type = 'w'
                    g_cost = 100
                    board[x][y] = 'w'

                if map1[grid_width*(grid_height-y-1) + x] == 'A':
                    grid[x][y] = 'A'
                    cell_type = 'A'
                    g_cost = 0
                    board[x][y] = 'A'
                    print "coordinates of A is: %d,%d" % (x, y)

                if map1[grid_width*(grid_height-y-1) + x] == 'B':
                    grid[x][y] = 'B'
                    cell_type = 'B'
                    g_cost = 0
                    board[x][y] = 'B'
                    print "coordinates of B is: %d,%d" % (x, y)

                #pushing every cell in to the cells-list, using a getMethod to get
                #the right cell out of the list

                self.cells.append(Cell(x, y, cell_type, g_cost))

        self.start = self.get_cell(17, 9)                                   #The starting coordinates and ending coordinates can be plotted in here
        self.end = self.get_cell(17, 0)                                     # <----------map1:start(17, 9), end(17,0)
                                                                            #            map2:start(2, 8), end(28, 0)
                                                                            #            map3:start(1, 2), end(27, 9)
                                                                            #            map3:start(14, 7), end(13, 3)


    def get_heuristic(self, cell):
        #Compute the heuristic value H for a cell: distance between
        #this cell and the ending cell multiply by 10.
        #Different heuristics can be used here.
        return 10 * (abs(cell.x - self.end.x) + abs(cell.y - self.end.y))

    def get_cell(self, x, y):
       #returning a cell from the cell list.
        return self.cells[x * self.grid_height + y]

    def get_adjacent_cells(self, cell):
        #Returns adjacent cells to a cell. Clockwise starting
        #from the one on the right.
        #returning a list of cells adjacent to current cell.
        cells = []
        if cell.x < self.grid_width-1:
            cells.append(self.get_cell(cell.x+1, cell.y))
        if cell.y > 0:
            cells.append(self.get_cell(cell.x, cell.y-1))
        if cell.x > 0:
            cells.append(self.get_cell(cell.x-1, cell.y))
        if cell.y < self.grid_height-1:
            cells.append(self.get_cell(cell.x, cell.y+1))
        return cells


    def display_path(self):
        total_cost = 0
        cell = self.end
        while cell.parent is not self.start:
            cell = cell.parent
            if cell.cell_type == 'r':
                total_cost += 1
                print "road"
            if cell.cell_type == 'g':
                total_cost += 5
                print "grass"
            if cell.cell_type == 'f':
                total_cost += 10
                print "forest"
            if cell.cell_type == 'm':
                total_cost += 50
                print "mountain"
            if cell.cell_type == 'w':
                total_cost += 100
                print "water"

            board[cell.x][cell.y] = '*'

            print 'path: cell: %d,%d' % (cell.x, cell.y)
        print "the totalcost is: %d" % (total_cost)

    def compare(self, cell1, cell2):
        if cell1.f < cell2.f:
            return -1
        elif cell1.f > cell2.f:
            return 1
        return 0

    def update_cell(self, adj, cell):
        cost_g = 10
        if adj.cell_type == 'r':
            cost_g = 1
        elif adj.cell_type == 'g':
            cost_g = 5
        elif adj.cell_type == 'f':
            cost_g = 10
        elif adj.cell_type == 'm':
            cost_g = 50
        elif adj.cell_type == 'w':
            cost_g = 100

        adj.g = cell.g + cost_g
        adj.h = self.get_heuristic(adj)
        adj.parent = cell
        #A*
        adj.f = adj.g + adj.h
        #Dijkstra
        #adj.f = adj.g

    # A* and Dijkstra(remember to uncomment the line right above too)
    def process(self):
        # add starting cell to open heap queue
        heapq.heappush(self.opened, (self.start.f, self.start))
        while len(self.opened):
            # pop cell from heap queue
            f, cell = heapq.heappop(self.opened)
            # add cell to closed list so we don't process it twice
            self.closed.add(cell)
            # if ending cell, display found path
            if cell is self.end:
                self.display_path()
                break
            # get adjacent cells for cell
            adj_cells = self.get_adjacent_cells(cell)
            for adj_cell in adj_cells:
                if adj_cell not in self.closed:
                    if (adj_cell.f, adj_cell) in self.opened:
                        # if adj cell in open list, check if current path is
                        # better than the one previously found
                        # for this adj cell.
                        if adj_cell.g > cell.g + 10:
                            self.update_cell(adj_cell, cell)
                    else:
                        self.update_cell(adj_cell, cell)
                        # add adj cell to open list
                        heapq.heappush(self.opened, (adj_cell.f, adj_cell))

        #printing out to screen
        open_set = retreive_open_list(self.opened)
        closed_set = retreive_closed_list(self.closed)
        output(board, open_set, closed_set)
    '''

    #BFS
    def process(self):

        #enqueue the first cell to the open list
        self.open_list.append((self.start.f, self.start))

        while len(self.open_list):
            # BFS: dequeue cell from list/queue
            f, cell = self.open_list.pop(0)

            # add cell to closed list so we don't process it twice
            self.closed.add(cell)
            # if ending cell, display found path
            if cell is self.end:
                self.display_path()
                break
            # get adjacent cells for cell
            adj_cells = self.get_adjacent_cells(cell)
            for adj_cell in adj_cells:
                if adj_cell not in self.closed:
                    if (adj_cell.f, adj_cell) in self.open_list:
                        # if adj cell in open list, check if current path is
                        # better than the one previously found
                        # for this adj cell.
                        if adj_cell.g > cell.g + 10:
                            self.update_cell(adj_cell, cell)
                    else:
                        self.update_cell(adj_cell, cell)
                        # add adj cell to open list
                        #heapq.heappush(self.opened, (adj_cell.f, adj_cell))
                        self.open_list.append((adj_cell.f, adj_cell))
        #printing out to screen
        open_set = retreive_open_list(self.open_list)
        closed_set = retreive_closed_list(self.closed)
        output(board, open_set, closed_set)
'''



#=====================================MAIN=============================================
def main():

    a = AStar()
    a.init_grid()
    a.process()


if __name__ == "__main__":
    main()
print "The runtime is: " + "--- %s seconds ---" % (time.time() - start_time)