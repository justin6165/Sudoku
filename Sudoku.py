import solver
import tkinter
from tkinter import *
from tkinter import messagebox
import time
import random
import os
import sys
import copy

boardColor = "black"

def restart():
    python = sys.executable
    os.execl(python, python, * sys.argv)

class Square:

    def __init__(self, master, pair, coordinate):
        self.master = master
        self.y = pair[0]
        self.x = pair[1]
        self.row = coordinate[0]
        self.col = coordinate[1]

        self.currentColor = boardColor
        self.frame = Frame(self.master, highlightbackground=self.currentColor, highlightthickness=1)
        self.frame.place(rely=float(self.y/3), relx=float(self.x/3), relwidth=float(1/3), relheight=float(1/3))
        self.frame.bind('<Button-1>', self.click)

        self.inputNum = board[self.row][self.col]
        if board[self.row][self.col] == 0:
            self.inputNum = ""
        self.label = Label(self.frame, text=self.inputNum, font="arial 12 bold")
        self.label.place(relx=.5, rely=.5, anchor="center")
        
    def click(self, event):
        global currentSquare
        currentSquare.frame.config(highlightbackground=boardColor)
        if self.currentColor == boardColor:
            self.frame.config(highlightbackground="red")
            self.currentColor = "red"
        else:
            self.frame.config(highlightbackground=boardColor)
            self.currentColor = boardColor
        currentSquare = self

def newBoard():
    offset = [2,8,5,3,6,0,4,7,1]
    board = [[] for i in range(9)]
    rows = []
    cols = []
    nums = random.sample(range(1, 10), 9)
    for r in random.sample(range(3), 3): 
        for c in random.sample(range(3), 3): 
            rows.append(r * 3 + c)  
    for r in random.sample(range(3), 3): 
        for c in random.sample(range(3), 3):
            cols.append(r * 3 + c)
    for r in rows:
        for c in cols:
            temp = nums[(offset[r] + c) % 9]
            board[r].append(temp)
    return board

def removeSquares(bo):
    tuples = []
    tempBoard = bo
    for i in range(9):
        for j in range(9):
            tuples.append((i, j))
    tuples = random.sample(tuples, 81)
    for i in range(46): #removing 46 squares so that 35 remain
        tempBoard[tuples[i][0]][tuples[i][1]] = 0
    return tempBoard

def key_backSpace(event):
    if currentSquare.currentColor == "red" and editable():
        currentSquare.label.config(text="")
        updateBoard(0)

def key_press(event):
    try:
        key = int(event.char)
        if currentSquare.currentColor == "red" and editable():
            if key > 0:
                if solver.isValid(modelBoard, key, currentSquare.row, currentSquare.col):
                    currentSquare.label.config(text=key, fg="gray")
                    updateBoard(key)
                    if won():
                        displayVictory()
                else: print(str(key) + " is not valid here")
            else: print("please enter a number between 1 and 9")
    except ValueError:
        print("please enter a number between 1 and 9")

def editable():
    return board[currentSquare.row][currentSquare.col] == 0

def updateBoard(key):
    modelBoard[currentSquare.row][currentSquare.col] = key

def won():
    if modelBoard == correctBoard:
        return True
    return False

def displayVictory():
    for i in range(len(squares)):
        for j in range(len(squares[i])):
            squares[i][j].label.config(fg="black")
    print("YOU WIN")
    messagebox.showinfo("Congratulations!", "YOU WIN!")

def outerGrid(parentFrame, outerFrames):
    for row in range(3):
        for col in range(3):
            frame = Frame(parentFrame, highlightbackground=boardColor, highlightthickness=2)
            frame.place(rely=float(row/3), relx=float(col/3), relwidth=float(1/3), relheight=float(1/3))
            outerFrames[row].append(frame)

def innerGrid(outerFrame, squares, rowIndex, colIndex):
    for row in range(3):
        for col in range(3):
            sudokuSquare = Square(outerFrame, (row, col), (row+rowIndex, col+colIndex))
            squares[row+rowIndex].append(sudokuSquare)

def clearBoard():
    for i in range(len(squares)):
        for j in range(len(squares[i])):
            if board[i][j] == 0:
                squares[i][j].label.config(text="")
    modelBoard = board

def solveBoard():
    clearBoard()
    currentSquare.currentColor=boardColor
    currentSquare.frame.config(highlightbackground=boardColor)
    solve(board, 0)
    modelBoard = correctBoard
    displayVictory()

def solve(bo, row):
    empty = solver.nextEmpty(bo, row)
    if empty == None: return True #finished solving
    for j in range(1, 10):
        if solver.isValid(bo, j , empty[0], empty[1]):
            bo[empty[0]][empty[1]] = j
            changeSquare(squares[empty[0]][empty[1]], j, "green")
            window.update_idletasks()
            time.sleep(.05)
            if solve(bo, empty[0]): 
                return True 
            else: 
                bo[empty[0]][empty[1]] = 0
                changeSquare(squares[empty[0]][empty[1]], 0, "red")
                window.update_idletasks()
                time.sleep(.05)
    return False #have to backtrack

def changeSquare(square, num, frameColor):
    square.label.config(text=num, fg="gray")
    square.frame.config(highlightbackground=frameColor)

correctBoard = newBoard()
board = removeSquares(copy.deepcopy(correctBoard))
modelBoard = copy.deepcopy(board)

window = Tk()
window.title("Sudoku")
window.geometry("540x600")

bigFrame = Frame(window, highlightbackground=boardColor, highlightthickness=2)
bigFrame.place(relwidth=1, relheight=.9)
mainFrame = Frame(bigFrame, highlightbackground=boardColor, highlightthickness=2)
mainFrame.place(relx=.05, rely=.05, relwidth=.9, relheight=.9)


bottomFrame = Frame(window)
bottomFrame.place(relwidth = .95, relheight=.05, relx=.5, rely=.95, anchor="center")

newGameButton = Button(bottomFrame, text="New Game", command=restart)
newGameButton.place(relx=.05, rely=0, relwidth=.25, relheight=1)
clearButton = Button(bottomFrame, text="Clear", command=clearBoard)
clearButton.place(relx=.7, rely=0, relwidth=.25, relheight=1)
solveButton = Button(bottomFrame, text="Solve", command=solveBoard)
solveButton.place(relx=.38, rely=0, relwidth=.25, relheight=1)


outerFrames = [[] for i in range(3)]
outerGrid(mainFrame, outerFrames)

squares = [[] for i in range(9)]
for row in range(3):
    for col in range(3):
        innerGrid(outerFrames[row][col], squares, row*3, col*3)
currentSquare = squares[0][0]

window.bind('<Key>', lambda value: key_press(value))
window.bind('<BackSpace>', lambda back: key_backSpace(back))

window.mainloop()