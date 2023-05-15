"""
This class is responsibale for storing all the information about the current state of chess game. it will also be
responsible for determining the valid moves at the current state.it will also keep a move log.
"""
class GameState():
     def __init__(self):
         # board is an 8x8 2d list, each element of the list has 2 characters.
         # The first character represents the color of the piece, 'b' or 'w'
         # The second character represents the type of the piece, 'K', 'Q', 'R','B','N'Or 'p'
         #"--"represent an empty space with no piece
         self.board =[
             ["bR" ,"bN" ,"bB" ,"bQ" ,"bK" ,"bB" ,"bN" ,"bR"],
             ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
             ["--", "--", "--", "--", "--", "--", "--", "--"],
             ["--", "--", "--", "--", "--", "--", "--", "--"],
             ["--", "--", "--", "--", "--", "--", "--", "--"],
             ["--", "--", "--", "--", "--", "--", "--", "--"],
             ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
             ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
         self.whiteToMove= True
         self.moveLog= []

     def makeMove(self,move):
         self.board[move.startRow][move.startCol] = "--"
         self.board[move.endRow][move.endCol] = move.pieceMoved
         self.moveLog.append(move) #log the move so we can undo it later
         self.whiteToMove = not self.whiteToMove #swap players

     def undoMove(self):
        if len(self.moveLog) != 0:
          move = self.moveLog.pop()
          self.board[move.startRow][move.startCol] = move.pieceMoved
          self.board[move.endRow][move.endCol] = move.pieceCaptured
          self.whiteToMove = not self.whiteToMove

     def getValidMoves(self):
         return  self.getAllPossibleMoves()

     def getAllPossibleMoves(self):
         moves= [Move((6,4),(4,4),self.board)]
         for r in range(len(self.board)):
             for c in range(len(self.board[r])):
                 turn = self.board[r][c][0]
                 if(turn =='w' and self.whiteToMove) and (turn=='b' and not self.whiteToMove):
                     piece= self.board[r][c][1]
                     if piece == 'p':
                         self.getPawnMoves(r, c, moves)
                     elif piece == 'R':
                         self.getRookMoves(r,c,moves)
         return moves
     def getPawnMoves(self,r,c,moves):
        pass


     def getRookMoves(self,r,c,moves):
         pass
class Move():
    ranksToRows = {"1":7,"2": 6, "3":5,"4":4,
                   "5": 3,"6":2, "7": 1,"8":0}
    rowsToRanks = {v: k for k,v in ranksToRows.items()}
    filesToCols ={"a": 0, "b":1 ,"c":2, "d":3,
                  "e": 4, "f": 5,"g": 6, "h": 7}
    colsToFiles = {v:k for k,v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        print(self.moveID)



    def __eq__(self,other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow,self.endCol)


    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
