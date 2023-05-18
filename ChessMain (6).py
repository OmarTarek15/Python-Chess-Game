import pygame as p
import ChessEngine, SmartMoveFinder
import sys
from multiprocessing import Process, Queue

BOARD_WIDTH = BOARD_HEIGHT = 650
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8
SQUARE_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


def loadImages():
    pieces = ["wp", "wR", "wN", "wB", "wK", "wQ", "bp", "bR", "bN", "bB", "bK", "bQ"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(
            p.image.load("images/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE)
        )


def main():
    p.init()
    screen = p.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    game_state = ChessEngine.GameState()
    valid_moves = game_state.getValidMoves()
    move_made = False
    animate = False
    loadImages()
    running = True
    square_selected = ()
    ai_thinking = False
    move_finder_process = None

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                sys.exit()

        if not game_state.checkmate and not game_state.stalemate:
            if not ai_thinking:

                ai_thinking = True
                return_queue = Queue()
                move_finder_process = Process(
                    target=SmartMoveFinder.findBestMove,
                    args=(game_state, valid_moves, return_queue),
                )
                move_finder_process.start()

            if not move_finder_process.is_alive():
                ai_move = return_queue.get()
                if ai_move is None:
                    ai_move = SmartMoveFinder.findRandomMove(valid_moves)
                game_state.makeMove(ai_move)
                move_made = True
                animate = True
                ai_thinking = False

        if move_made:
            if animate:
                animateMove(game_state.move_log[-1], screen, game_state.board, clock)
            valid_moves = game_state.getValidMoves()
            move_made = False
            animate = False
            move_undone = False

        drawGameState(screen, game_state, valid_moves, square_selected)

        if game_state.checkmate:
            if game_state.white_to_move:
                drawEndGameText(screen, "Black wins by checkmate")
            else:
                drawEndGameText(screen, "White wins by checkmate")

        elif game_state.stalemate:
            drawEndGameText(screen, "Stalemate")

        clock.tick(MAX_FPS)
        p.display.flip()


def drawGameState(screen, game_state, valid_moves, square_selected):
    drawBoard(screen)
    highlightSquares(screen, game_state, valid_moves, square_selected)
    drawPieces(screen, game_state.board)


def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = colors[((row + column) % 2)]
            p.draw.rect(
                screen,
                color,
                p.Rect(
                    column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE
                ),
            )


def highlightSquares(screen, game_state, valid_moves, square_selected):
    if (len(game_state.move_log)) > 0:
        last_move = game_state.move_log[-1]
        s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
        s.set_alpha(100)
        s.fill(p.Color("green"))
        screen.blit(
            s, (last_move.end_col * SQUARE_SIZE, last_move.end_row * SQUARE_SIZE)
        )
    if square_selected != ():
        row, col = square_selected
        if game_state.board[row][col][0] == ("w" if game_state.white_to_move else "b"):
            s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(100)
            s.fill(p.Color("blue"))
            screen.blit(s, (col * SQUARE_SIZE, row * SQUARE_SIZE))

            s.fill(p.Color("yellow"))
            for move in valid_moves:
                if move.start_row == row and move.start_col == col:
                    screen.blit(
                        s, (move.end_col * SQUARE_SIZE, move.end_row * SQUARE_SIZE)
                    )


def drawPieces(screen, board):
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != "--":
                screen.blit(
                    IMAGES[piece],
                    p.Rect(
                        column * SQUARE_SIZE,
                        row * SQUARE_SIZE,
                        SQUARE_SIZE,
                        SQUARE_SIZE,
                    ),
                )


def drawMoveLog(screen, game_state, font):
    move_log_rect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color("black"), move_log_rect)
    move_log = game_state.move_log
    move_texts = []
    for i in range(0, len(move_log), 2):
        move_string = str(i // 2 + 1) + ". " + str(move_log[i]) + " "
        if i + 1 < len(move_log):
            move_string += str(move_log[i + 1]) + "  "
        move_texts.append(move_string)

    moves_per_row = 3
    padding = 5
    line_spacing = 2
    text_y = padding
    for i in range(0, len(move_texts), moves_per_row):
        text = ""
        for j in range(moves_per_row):
            if i + j < len(move_texts):
                text += move_texts[i + j]

        text_object = font.render(text, True, p.Color("white"))
        text_location = move_log_rect.move(padding, text_y)
        screen.blit(text_object, text_location)
        text_y += text_object.get_height() + line_spacing


def drawEndGameText(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    text_object = font.render(text, False, p.Color("gray"))
    text_location = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(
        BOARD_WIDTH / 2 - text_object.get_width() / 2,
        BOARD_HEIGHT / 2 - text_object.get_height() / 2,
    )
    screen.blit(text_object, text_location)
    text_object = font.render(text, False, p.Color("black"))
    screen.blit(text_object, text_location.move(2, 2))


def animateMove(move, screen, board, clock):
    global colors
    d_row = move.end_row - move.start_row
    d_col = move.end_col - move.start_col
    frames_per_square = 10  # frames to move one square
    frame_count = (abs(d_row) + abs(d_col)) * frames_per_square
    for frame in range(frame_count + 1):
        row, col = (
            move.start_row + d_row * frame / frame_count,
            move.start_col + d_col * frame / frame_count,
        )
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.end_row + move.end_col) % 2]
        end_square = p.Rect(
            move.end_col * SQUARE_SIZE,
            move.end_row * SQUARE_SIZE,
            SQUARE_SIZE,
            SQUARE_SIZE,
        )
        p.draw.rect(screen, color, end_square)
        if move.piece_captured != "--":
            if move.is_enpassant_move:
                enpassant_row = (
                    move.end_row + 1
                    if move.piece_captured[0] == "b"
                    else move.end_row - 1
                )
                end_square = p.Rect(
                    move.end_col * SQUARE_SIZE,
                    enpassant_row * SQUARE_SIZE,
                    SQUARE_SIZE,
                    SQUARE_SIZE,
                )
            screen.blit(IMAGES[move.piece_captured], end_square)

        screen.blit(
            IMAGES[move.piece_moved],
            p.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
        )
        p.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
