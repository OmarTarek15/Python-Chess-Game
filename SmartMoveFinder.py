import random

pieceScore = {"K": 0, "Q":10, "R":5, "B":3, "N":3, "p":1}
CHeckMate = 1000
StaleMate = 0
DEPTH = 2 


def findRandomMove(validMoves):
  return validMoves[random.randint(0, len(validMoves)-1)]

def findMoveMinMax (gs, ValidMoves, depth, whiteToMove):
    global nextMove   #bescause we will call this fun recursively we need a var to hold the next move 
    if depth == 0:
        return ScoreMaterial(gs.board)
    if whiteToMove:
        maxScore = -CHeckMate
        for move in ValidMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score =  findMoveMinMax(gs, nextMoves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore    
    else:
        minScore =  CHeckMate
        for move in ValidMoves:
             gs.makeMove(move)
             nextMoves = gs.getValidMoves()
             score =  findMoveMinMax(gs, nextMoves, depth - 1, True)
             if score > minScore:
                minScore = score
                if depth == DEPTH:
                   nextMove = move
             gs.undoMove() 
        return minScore                
    
def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    
    #move ordering- implement later 
    maxScore = -CHeckMate
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth-1, -alpha, -beta, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
        if maxScore > alpha : #pruning happens 
            alpha = maxScore
        if alpha>= beta:
            break    

    return maxScore            

# helper method to make first recursive call             
def findBestMove(gs, validMoves):
    global nextMove , counter
    nextMove = None
    random.shuffle(validMoves)
    counter = 0
    findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
    #findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHeckMate, CHeckMate, 1 if gs.whiteToMove else -1)
    print(counter)
    return nextMove



# method to store all the vaild moves & all the vaild defense of the piece 
#-ve score black won __ +ve score white won 

def scoreBoard(gs):
    if gs.checkMate :
        if gs.whiteToMove:
            return -CHeckMate #black wins
        else :
            return CHeckMate #white wins
    elif gs.staleMate:
        return StaleMate
    
    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
        
    return score                




#score based on material
def ScoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    return score