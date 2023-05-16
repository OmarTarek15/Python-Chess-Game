import random

pieceScore = {"K": 0, "Q":10, "R":5, "B":3, "N":3, "p":1}
CHeckMate = 1000
StaleMate = 0


def findRandomMove(validMoves):
  return validMoves[random.randint(0, len(validMoves)-1)]

def findBestMove(gs,validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1
    opponentMinMaxScore = CHeckMate
    bestPlayerMove = None
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentMoves = gs.getValidMoves()
        opponentMaxScore = -turnMultiplier * CHeckMate
        for opponentMoves in opponentMoves:
            gs.makeMove(opponentMoves)
            if gs.checkMate:
                score = -CHeckMate
            elif gs.staleMate:
                score = StaleMate
            else:
                score = turnMultiplier * ScoreMaterial(gs.board)
            if score > opponentMaxScore:
                opponentMaxScore = score
            gs.undoMove()
        if opponentMaxScore <opponentMinMaxScore:
            opponentMinMaxScore = opponentMaxScore
            bestPlayerMove = playerMove
        gs.undoMove()
    return bestPlayerMove



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