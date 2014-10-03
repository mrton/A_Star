import heapq
import turtle

board = []

class Cell(object):
    def __init__(self, x, y, reachable):
        """
        This is the cell class, each cell has a coordinate x and y.
        Reachable is True if the cell is not a wall and False if it is.
        """
        self.reachable = reachable
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0

class AStar(object):
    # This method is initializing the AStar object with:
    # 1. an openList that contains nodes that are not yet being processed
    # 2. an closedList that contains nodes that have been processed
    # 3. the dimension of the grid.

    def __init__(self):
        self.opened = []
        heapq.heapify(self.opened)
        self.closed = set()
        self.cells = []
        self.grid_height = 7
        self.grid_width = 20

    def init_grid(self):
        #This  Method will initialize the grid that A* algorithm will be applied on

        walls1 = ((9, 4), (10, 4), (11, 4), (12, 4), (13, 4),
                 (14, 4), (14, 3), (9, 2), (10, 2), (11, 2),
                 (12, 2), (13, 2), (14, 2))
        walls2 = ((6, 0),(10, 0),
                (5, 1) ,(8, 1) ,(11, 1),
                (4, 2), (7, 2), (12, 2),
                (3, 3), (6, 3),
                (4, 4), (7, 4),
                (5, 5), (7, 5),
                (7, 6))
        walls3 = ((7, 0),(8, 0), (9, 0),
                (6, 1), (10, 1),
                (6, 2), (8, 2), (11, 2),
                (6, 3), (9, 3), (11, 3),
                (7, 4), (8, 4), (11, 4),
                (10, 5))
        walls4 = ((11, 0),(15, 0),
                (0, 1), (2, 1), (3, 1), (4, 1), (5, 1), (7, 1), (8, 1), (10, 1), (11, 1), (13, 1), (15, 1), (17, 1), (18,1),
                (2, 2), (5, 2), (8, 2), (13,2), (17,2),
                (1, 3), (2, 3), (4, 3), (5, 3), (6, 3), (8, 3), (9, 3), (10, 3), (11, 3), (12, 3), (13, 3), (15, 3), (16, 3), (17, 3), (18, 3), (19, 3),
                (2, 4), (8, 4), (10, 4), (15,4 ),
                (0, 5), (2, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (10, 5), (12, 5), (13, 5), (14, 5), (15, 5), (17, 5),
                (2, 6 ),(10, 6), (17, 6))

        #Making an empty matrix of the same size as the board, for view.
        makeEmptyGrid(self.grid_width,self.grid_height)

        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if (x, y) in walls2:
                    board[x][y] = 2
                    reachable = False
                else:
                    reachable = True
                self.cells.append(Cell(x, y, reachable))

        #------------Board1-------------
        #self.start = self.get_cell(11, 3)
        #self.end = self.get_cell(17, 3)
        #board[11][3] = 1
        #board[17][3] = 3
        #------------Board2-------------
        self.start = self.get_cell(0, 3)
        self.end = self.get_cell(19, 3)
        board[0][3] = 1
        board[19][3] = 3
        #------------Board3-------------
        #self.start = self.get_cell(8, 3)
        #self.end = self.get_cell(19, 0)
        #board[8][3] = 1
        #board[19][0] = 3
        #------------Board4-------------
        #self.start = self.get_cell(0, 6)
        #self.end = self.get_cell(4, 2)
        #board[0][6] = 1
        #board[4][2] = 3


    def get_heuristic(self, cell):
        #Compute the heuristic value H for a cell: distance between
        #this cell and the ending cell multiply by 10.
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
        cell = self.end
        while cell.parent is not self.start:
            cell = cell.parent
            board[cell.x][cell.y] = 8
            print 'path: cell: %d,%d' % (cell.x, cell.y)

    def compare(self, cell1, cell2):
        """
        Compare 2 cells F values

        @param cell1 1st cell
        @param cell2 2nd cell
        @returns -1, 0 or 1 if lower, equal or greater
        """
        if cell1.f < cell2.f:
            return -1
        elif cell1.f > cell2.f:
            return 1
        return 0

    def update_cell(self, adj, cell):
        """
        Update adjacent cell

        @param adj adjacent cell to current cell
        @param cell current cell being processed
        """
        adj.g = cell.g + 10
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
                if adj_cell.reachable and adj_cell not in self.closed:
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
        boardRow = board[i*20:20*(i+1)]
        boardGrid.append(boardRow)
    return boardGrid

def printBoard(board):
    for i in xrange(len(board)):
        print board[i]

def turtlePrint(board, width, height):
    turtle.hideturtle()
    turtle.speed(0)
    turtle.penup()
    turtle.goto(-210, -60)
    turtle.pendown()
    turtle.goto(20*width-210, -60)
    turtle.goto(20*width-210, 20*height-60)
    turtle.goto(-210, 20*height-60)
    turtle.goto(-210, -60)
    turtle.penup()

    for y in xrange(height):
        for x in xrange(width):
            turtle.penup()
            turtle.goto(20*x-200,20*y-50)
            turtle.pendown()
            if board[x][y] is 1:
                turtle.pencolor("green")
                turtle.dot(10)
                turtle.pencolor("black")
            elif board[x][y] is 2:
                turtle.dot(20)
            elif board[x][y] is 3:
                turtle.pencolor("red")
                turtle.dot(10)
                turtle.pencolor("black")
            elif board[x][y] is 8:
                turtle.pencolor("blue")
                turtle.dot()
                turtle.pencolor("black")

    turtle.exitonclick()

#=====================================MAIN=============================================

def main():
    a = AStar()
    a.init_grid()
    a.process()
    printBoard(board)
    turtlePrint(board, a.grid_width, a.grid_height)



if __name__ == "__main__":
    main()
