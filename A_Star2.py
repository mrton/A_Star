import heapq
#                                                                                           --------------------------------------------
#A : starting                                                                               -----HELLO HELLO WELCOME TO CYBERSPACE------
#B : ending                                                                                 --------------------------------------------
#r : roads            1
#g : grasslands       5
#f : forests         10
#m : mountains       50
#w : water          100

#=======================boards=====================================
#the text files must be in the same folder

board1 = "board-2-1.txt"
board2 = "board-2-2.txt"
board3 = "board-2-3.txt"
board4 = "board-2-4.txt"

board11 = ( "mmmmmffffrrrrrrrrArrrrrrrrrrrrrrfffmmmmm"
            "mmmffffffffrrrrrrrrrrrrrrrrrrrrfffffmmmm"
            "mmfffffffffffffffffffffffffffrffffffmmmm"
            "mmfffffffffffffwwwwwfffffffffrfffffffmmm"
            "mfffffffffffffwwwwwwwffffffffrffffffmmmm"
            "mmffffffffffffwwwwwwwffrrrrrrrrrrrrrmmmm"
            "mmmffffffffffffwwwwwffffffffffffrffffmmm"
            "mmffffffffffffffffffffffffffffffrfffffmm"
            "mmffffffffggggggggggggggggggggggggffffmm"
            "mmmffffggggggggggBggggggggggggggggggffmm")


board = []

class Cell(object):
    def __init__(self, x, y, cell_type, g_cost):
        #cell type can be: r ,g ,f ,m or w.


        self.cell_type = cell_type
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
        #The access is by [x][y]
        w, h = 10, 40
        grid = [[None] * w for i in xrange(h)]

        for x in xrange(grid_width):
            for y in xrange(grid_height):
                if board11[grid_width*(grid_height-y-1) + x] == 'r':
                    grid[x][y] = 'r'
                    cell_type = 'r'
                    g_cost = 1
                    board[x][y] = 'r'

                if board11[grid_width*(grid_height-y-1) + x] == 'g':
                    grid[x][y] = 'g'
                    cell_type = 'g'
                    g_cost = 5
                    board[x][y] = 'g'

                if board11[grid_width*(grid_height-y-1) + x] == 'f':
                    grid[x][y] = 'f'
                    cell_type = 'f'
                    g_cost = 10
                    board[x][y] = 'f'

                if board11[grid_width*(grid_height-y-1) + x] == 'm':
                    grid[x][y] = 'm'
                    cell_type = 'm'
                    g_cost = 50
                    board[x][y] = 'm'

                if board11[grid_width*(grid_height-y-1) + x] == 'w':
                    grid[x][y] = 'w'
                    cell_type = 'w'
                    g_cost = 100
                    board[x][y] = 'w'

                if board11[grid_width*(grid_height-y-1) + x] == 'A':
                    grid[x][y] = 'A'
                    cell_type = 'A'
                    g_cost = 0
                    board[x][y] = 'A'

                if board11[grid_width*(grid_height-y-1) + x] == 'B':
                    grid[x][y] = 'B'
                    cell_type = 'B'
                    g_cost = 0
                    board[x][y] = 'B'

                self.cells.append(Cell(x, y, cell_type, g_cost))

        # The starting coordinates and ending coordinates can be plotted in here
        self.start = self.get_cell(17, 9)
        self.end = self.get_cell(17, 0)

    def get_heuristic(self, cell):
        #Compute the heuristic value H for a cell: distance between
        #this cell and the ending cell multiply by 10.
        #Manhatten distance
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
                total_cost = total_cost + 1
            if cell.cell_type == 'g':
                total_cost = total_cost + 5
            if cell.cell_type == 'f':
                total_cost = total_cost + 10
            if cell.cell_type == 'm':
                total_cost = total_cost + 50
            if cell.cell_type == 'w':
                total_cost = total_cost + 100
            board[cell.x][cell.y] = '*'
            print 'path: cell: %d,%d' % (cell.x, cell.y)
        print total_cost

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
        adj.f = adj.h + adj.g

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


#========================Support Functions===============================================

def makeEmptyGrid(grid_width,grid_height):
    for x in range(grid_width):
        board.append([0] * grid_height)

def createBoard(board, board_height):
    boardGrid = []
    boardWidth = len(board)/board_height

    for i in xrange(0,board_height):
        boardRow = board[i*40:40*(i+1)]
        boardGrid.append(boardRow)
    return boardGrid

def printBoard(board):
    for i in xrange(len(board)):
        print board[i]


def getCell(x, y, board, board_height):
    return board[x * board_height + y]

def gridify(file_string):
    grid_data = []
    with open(file_string) as f:
        for line in f:
            grid_data.append(line.strip())
    f.closed
    return grid_data


#=====================================MAIN=============================================
def main():

    a = AStar()
    a.init_grid()
    a.process()

    for i in xrange(len(board)):
        print board[i]


if __name__ == "__main__":
    main()
