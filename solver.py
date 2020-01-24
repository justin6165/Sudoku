
exampleBoard = [
    [0, 3, 1, 9, 0, 0, 8, 0, 0],
    [0, 0, 0, 4, 0, 8, 0, 0, 0],
    [0, 5, 0, 0, 0, 0, 0, 0, 0],
    [3, 0, 0, 0, 8, 0, 5, 0, 4],
    [9, 0, 0, 0, 0, 0, 0, 0, 6],
    [6, 0, 7, 0, 5, 0, 0, 0, 2],
    [0, 0, 0, 0, 0, 0, 0, 5, 0],
    [0, 0, 0, 1, 0, 2, 0, 0, 0],
    [0, 0, 9, 0, 0, 3, 2, 1, 0],
]

def printBoard(bo):
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - -")
        for j in range(len(bo[i])):
            if j % 3 == 0 and j != 0:
                print(" | ", end = "")
            if j == 8:
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + " ", end = "")

def solve(bo, row):
    empty = nextEmpty(bo, row)
    if empty == None: return True #finished solving
    for j in range(1, 10):
        if isValid(bo, j , empty[0], empty[1]):
            bo[empty[0]][empty[1]] = j
            if solve(bo, empty[0]): 
                return True 
            else: 
                bo[empty[0]][empty[1]] = 0
    return False #have to backtrack

def isValid(bo, num, row, column):
    for i in range(len(bo[row])):
        if bo[row][i] == num and i != column:
            return False
    for i in range(len(bo)):
        if bo[i][column] == num and i != row:
            return False
    tempRow = row - (row % 3)
    tempCol = column - (column % 3)
    for i in range(tempRow, tempRow + 3):
        for j in range(tempCol, tempCol + 3):
            if bo[i][j] == num and (i, j) != (row, column):
                return False
    return True

def nextEmpty(bo, row):
    for i in range(row, len(bo)):
        for j in range(len(bo[i])):
            if bo[i][j] == 0:
                return (i, j)
    return None
