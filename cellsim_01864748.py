import os
import time
import random
import copy

class Cell():
    """
    Represents a class of healthy cells.

    Class Attribute:
    alive, type: boolean

    Class Methods:
    __init__(self, alive=False)
    __str__(self)
    is_alive(self)
    update_cell(self, matrix)
    
    """

    
    def __init__(self, alive=False):
        self.alive = alive


    def __str__(self):
        if self.alive:
            return "O"
        else:
            return "."
##        return "O" if self.alive else "."


    def is_alive(self):
        return self.alive


    def update_cell(self, matrix):
        num_alive = 0
        for i in range(len(matrix)): 
            for j in range(len(matrix[i])): 
                #Ignore the centre
                if (i,j) != (1,1): 
                    if matrix[i][j].alive:
                        num_alive += 1
        #Dies -> Overpopulation(>=4) / Loneliness(<=1)
        if (matrix[1][1].alive == True) and (num_alive >= 4 or num_alive <= 1) :
            self.alive = False
        #Birth -> 3 neighbours alive
        elif (matrix[1][1].alive == False) and (num_alive == 3):
            self.alive = True
        #Stasis -> doesn't change otherwise
        else:
            self.alive = matrix[1][1].alive
        


class Cancer(Cell):
    """
    Represents a class of cancer cells.

    Parent Class: Cell()

    Class Attribute:
    alive, type: boolean

    Class Methods:
    __init__(self, alive=False)
    __str__(self)
    is_alive(self)
    update_cell(self, matrix)
    
    """

    
    def __init__(self, alive=False):
        super().__init__(alive)


    def __str__(self):
        if self.alive:
            return "X"
        else:
            return "."
##        return "X" if self.alive else "."

##    #super()
    def is_alive(self):
        super().is_alive()

##    #super()
    def update_cell(self, matrix):
        num_alive = 0
        for i in range(len(matrix)): 
            for j in range(len(matrix[i])):
                #Ignore the centre
                if (i,j) != (1,1): 
                    if matrix[i][j].alive:
                        num_alive += 1
        #Dies -> Overpopulation(>=5) / Loneliness(<=1)
        if (matrix[1][1].alive == True) and (num_alive >= 5 or num_alive <= 1) :
            self.alive = False
        #Birth -> 3 neighbours alive
        elif (matrix[1][1].alive == False) and (num_alive == 3):
            self.alive = True
        #Stasis -> doesn't change otherwise
        else:
            self.alive = matrix[1][1].alive


class Tissue():
    """
    The class Tissue should represent the space where cells grow and die.

    Class Attribute:
    self.rows, type: int
    self.cols, type: int
    self.matrix, type: nested list
    self.CellType, type: class

    Class Methods:
    __init__(self, height=1, width=1, CellType=Cell)
    __str__(self)
    __getitem__(self, key)
    __setitem__(self, key, item)
    seed_from_matrix(self, array)
    seed_from_file(self, file, cell_type=Cell)
    seed_random(self, confluency, cells=Cell)
    next_state(self)
    
    """

    
    def __init__(self, height=1, width=1, CellType=Cell):
        self.rows, self.cols = height, width
        self.matrix = []
        self.CellType = CellType
        for i in range(self.rows):
            self.matrix.append([])
            for j in range(self.cols):
                self.matrix[i].append(CellType())

##    #REDO?? --> not sue if this is the best method
    def __str__(self):
        grid = str()
        for i in range(self.rows):
            for j in range(self.cols):
                grid = grid + self.matrix[i][j].__str__()
            grid = grid + "\n"
        #To remove the \n after the last grid
        if self.rows > 0:
            grid = grid[:-1]            
        return grid


##    ##RECHECK INPUT
##    def __getitem__(self, key):
##        return self.matrix[key]

    def __getitem__(self, key):
        #if input is matrix[0:2], for example
        if isinstance(key,slice):
            print (key)
            indices = range(*key.indices(len(self.matrix)))
            return [self.matrix[i] for i in indices]

        #if input is matrix[0], for example
        elif isinstance(key,int):
            print('int '+ str(key))
            return self.matrix[key]

        #for matrix[1,2] like inputs where 1 is row and 2 is col
        else:
            row, col = key
            if isinstance(row, int) and isinstance(col, (int, slice)):
                return self.matrix[row][col]
            elif isinstance(row, slice) and isinstance(col, (int, slice)):
                return [r[col] for r in self.matrix[row]]
            else :
                raise TypeError


##    ##RECHECK INPUT
    def __setitem__(self, key, item):
        new_mat = Tissue.__getitem__(self, key)
        print(new_mat)
        new_mat[:] = item
        return new_mat


    def seed_from_matrix(self, array):
        ## check that input is valid
        if len(array) == 0 or len(array[0]) == 0:
            assert(False)
            
        ## overwrite parameters
        self.matrix = array
        self.CellType = type(array[0][0])
        self.rows, self.cols = len(array), len(array[0])                   


    def seed_from_file(self, file, cell_type=Cell):
        os.getcwd()
        with open(file, "r") as file_name:
            num_lines = sum(1 for line in open(file, "r")) 
            array = []        
            for i in range(num_lines):
                array.append([])
                for cell in file_name.readline().strip():
                    array[i].append(cell)
            
            ## overwrite parameters
            self.matrix = array
            self.CellType = cell_type
            self.rows, self.cols = num_lines, len(array[0])


##    ##RECHECK - it works but is it what we want?
    def seed_random(self, confluency, cells=Cell):
##        #am I supposed to overwrite???
        self.CellType = cells 
        con = float(confluency)
        prob_alive = (con)*(self.rows*self.cols) #0.70 * (5*5) = 17.5
        print(prob_alive)##
        
##        array = Tissue() #--> getitem
        array = self.matrix
##        counter = 0

        for a_row in range(self.rows):
            for a_col in range(self.cols):
                array[a_row][a_col] = random.random()
                if array[a_row][a_col] < con:
                    self.matrix[a_row][a_col] = cells(True)
##                    counter += 1
                else:
                    self.matrix[a_row][a_col] = cells(False)
##        print(counter)
##        print(self.rows*self.cols - counter)
            

    def next_state(self):
        mat = copy.deepcopy(self.matrix)
        
        #add a row of dead cells at the top and botom
        new_mat = [[self.CellType(False)]*(len(mat[0]))] + mat + [[self.CellType(False)]*(len(mat[0]))]
        
        #add a column of dead cells at the start and end
        for r in range(len(new_mat)): 
            new_mat[r].insert(0, self.CellType(False))
            new_mat[r].append(self.CellType(False))

        #range --> because we don't care about the outer box of dead cells
        #box is there to avoid errors only
        for i in range(1, len(new_mat)-1):
            for j in range(1, len(new_mat[i])-1):
                if isinstance(new_mat[i][j], self.CellType):
                    
                    #check_mat is 3*3 array of the cell and it's neighbours
                    check_mat = [[new_mat[i-1][j-1], new_mat[i-1][j], new_mat[i-1][j+1]],
                                 [new_mat[i][j-1], new_mat[i][j], new_mat[i][j-1]],
                                 [new_mat[i+1][j-1], new_mat[i+1][j], new_mat[i+1][j+1]]]

                    self.matrix[i-1][j-1].update_cell(check_mat)
                    self.matrix[i-1][j-1].is_alive()
                    #test variable is of class CellType
##                    test = self.CellType()
##                    test.update_cell(check_mat)
##                    test.is_alive()
##
##                    #overwrite self.matrix --> are we supposed to?
##                    self.matrix[i-1][j-1] = test #because i,j begin as 1,1 and not 0,0
