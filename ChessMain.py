import pygame as p
import ChessEngine


WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def LoadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    LoadImages()
    running = True
    sqSelected = ()
    playerClicks = []

    while running:
      for e in p.event.get():
         if e.type == p.QUIT:
             running = False

         elif e.type == p.MOUSEBUTTONDOWN:
            location = p.mouse.get_pos() #(x,y)location of mouse
            col =location[0]//SQ_SIZE
            row =location[1]//SQ_SIZE
            if  sqSelected == (row,col): #  the user clicked the same square twice
                 sqSelected = () #deselect
                 playerClicks=[]
            else:
                sqSelected=(row,col)
                playerClicks.append(sqSelected) #Append for both 1st and snd clicks
            if len(playerClicks) == 2: #after2nd click
                move = ChessEngine.Move(playerClicks[0],playerClicks[1], gs.board)
                print(move.getChessNotation())
                for i in range(len(validMoves)):
                    if move == validMoves[i]:
                        gs.makeMove(validMoves[i])
                        moveMade = True
                        sqSelected =()
                        playerClicks =[]
                if not moveMade:
                    playerClicks = [sqSelected]

         elif e.type == p.KEYDOWN:
            if e.key == p.K_z:
                gs.undoMove()
                moveMade = True

      if moveMade:
          validMoves = gs.getValidMoves()
          moveMade=False


      drawGameState(screen, gs)
      clock.tick(MAX_FPS)
      p.display.flip()

'''
Resbonsible for all graphics within a currenr game state
'''

def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)

def drawBoard(screen):
    colors = [p.Color("white"), p.Color("darkgreen")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()
