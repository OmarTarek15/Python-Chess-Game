import pygame as p
import ChessEngine, SmartMoveFinder


WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


def LoadImages():
    pieces = ["wp", "wR", "wN", "wB", "wK", "wQ", "bp", "bR", "bN", "bB", "bK", "bQ"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(
            p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE)
        )


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    animate = False
    LoadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    gameOver = False
    playerOne = True #if human is playing white then true if ai false
    playerTwo = False
    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos()  # (x,y)location of mouse
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sqSelected == (
                        row,
                        col,
                    ):  #  the user clicked the same square twice
                        sqSelected = ()  # deselect
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(
                            sqSelected
                        )  # Append for both 1st and snd clicks
                    if len(playerClicks) == 2:  # after2nd click
                        move = ChessEngine.Move(
                            playerClicks[0], playerClicks[1], gs.board
                        )
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                    animate = False
                if e.key == p.K_r:
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
#ai move finder
        if not gameOver and not humanTurn:
            AIMove = SmartMoveFinder.findBestMove(gs,validMoves)
            if AIMove is None:
                AIMove = SmartMoveFinder.findRandomMove(validMoves)
            gs.makeMove((AIMove))
            moveMade = True
            animate = True

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False

        drawGameState(screen, gs, validMoves, sqSelected)

        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, "Black wins by checkmate")
            else:
                drawText(screen, "White wins by checkmate")
        elif gs.staleMate:
            gameOver = True
            drawText(screen, "Stalemate")

        clock.tick(MAX_FPS)
        p.display.flip()


"""
Resbonsible for all graphics within a currenr game state
"""


def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ("w" if gs.whiteToMove else "b"):
            # selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)  # transparency
            s.fill(p.Color("blue"))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            # moves from the square
            s.fill(p.Color("yellow"))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (SQ_SIZE * move.endCol, SQ_SIZE * move.endRow))


def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)


def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(
                screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            )


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(
                    IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                )


def animateMove(move, screen, board, clock):
    global colors
    R = move.endRow - move.startRow
    C = move.endCol - move.startCol
    framesPerSquare = 10  # frames to move one square
    frameCount = (abs(R) + abs(C)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (
            move.startRow + R * frame / frameCount,
            move.startCol + C * frame / frameCount,
        )
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(
            move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE
        )
        p.draw.rect(screen, color, endSquare)
        if move.pieceCaptured != "--":
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        screen.blit(
            IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        )
        p.display.flip()
        clock.tick(60)


def drawText(screen, text):
    font = p.font.SysFont("Arial", 32, True, False)
    textObject = font.render(text, 0, p.Color("Gray"))
    textLoc = p.Rect(0, 0, WIDTH, HEIGHT).move(
        WIDTH / 2 - textObject.get_width() / 2, HEIGHT / 2 - textObject.get_height() / 2
    )
    screen.blit(textObject, textLoc)
    textObject = font.render(text, 0, p.Color("Black"))
    screen.blit(textObject, textLoc.move(2, 2))


if __name__ == "__main__":
    main()