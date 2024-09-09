
##     ##  #######  ##     ## ######## ########
###   ### ##     ## ##     ## ##       ##     ##
#### #### ##     ## ##     ## ##       ##     ##
## ### ## ##     ## ##     ## ######   ########
##     ## ##     ##  ##   ##  ##       ##   ##
##     ## ##     ##   ## ##   ##       ##    ##
##     ##  #######     ###    ######## ##     ##

#       most complicated function
#       make move on board
#       input board and 'from' and 'to' of the move
#       output updated board

def make_move(given_board, move_from: int, move_to: int):
    answer = True
    promotion = False
    piece = ''
    temp = given_board[move_from]

    #increment halfmove counter
    if given_board[0] == 'b':
        given_board[2] += 1
    # en passant logic
    # check if this move captures en passant

    # capture piece below target if white captures and store it in index 6 to be awarded after move is validated
    if given_board[1] != '' and move_to == int(given_board[1]) and given_board[0] == 'w':
        given_board[6] = given_board[int(given_board[1]) - 1]
        print(given_board[6])
        given_board[int(given_board[1]) - 1] = ' '

    # capture piece above if black captures and award it immediately to index 4
    elif given_board[1] != '' and move_to == int(given_board[1]) and given_board[0] == 'b':
        given_board[4] = given_board[int(given_board[1]) + 1]
        given_board[int(given_board[1]) + 1] = ' '

    # if the en passant is not captured it expires
    else:
        given_board[1] = ''

    # save target square when moving pawn 2 places
    if given_board[move_from] == '♟' or given_board[move_from] == '♙':
        # a pawn was moved so halfmove counter is reset
        given_board[2] = 0
        if move_to - move_from == 2 or move_to - move_from == -2:
            # the average is always the target square for both sides, think about it, the math behind it is fun
            given_board[1] = str(int((move_from + move_to) / 2))

    # promotion logic
    if given_board[move_from] == '♟':
        # for black
        if given_board[9]:
            promotion = True
            piece = given_board[9]
        # for white
        if given_board[move_from] == '♟' and str(move_to)[1] == '8':
            print("Je promoveert een pion! Welk stuk wil je hebben?")
            while answer:
                piece = input("t voor toren, p voor paard, l voor loper of k voor koningin:\n").lower()
                if piece == 't' or piece == 'p' or piece == 'l' or piece == 'k':
                    answer = False
                    promotion = True

    # roquade logic
    if move_from == 51 and given_board[move_from] == '♚' and move_to == 71:
        given_board[61] = '♜'
        given_board[81] = ' '
    if move_from == 51 and given_board[move_from] == '♚' and move_to == 31:
        given_board[41] = '♜'
        given_board[11] = ' '

    # clear 'from' tile. It is saved in temp
    given_board[move_from] = ' '

    # logic to capture pieces. a captured piece for white is first held until the move is confirmed to be legal by both API and local logic
    if given_board[move_to] != ' ':
        #if a piece is captured the halfmove counter resets
        given_board[2] = 0
        # if it was blacks turn black gets the captured piece
        if given_board[0] == 'b':
            given_board[4] += given_board[move_to]
            print(f"tegenstander heeft {given_board[move_to]} gepakt")
        # if it was whites turn, they get it
        elif given_board[0] == 'w':
            given_board[6] += given_board[move_to]
        else:
            print("error while capturing piece")
    # move piece to new tile
    given_board[move_to] = temp
    if promotion:
        promote(given_board, move_to, piece)

    # change whose turn it is in the fen code
    if given_board[0] == 'w':
        given_board[0] = 'b'
    else:
        given_board[0] = 'w'

    # reset promotion
    given_board[9] = False
    #add fullmove
    given_board[3] += 1
    # return the board
    return given_board







# promote the pawn to previously selected piece
def promote(given_board, move_to, piece,):
    if piece == 'k':
        given_board[move_to] = '♛'
    elif piece == 'l':
        given_board[move_to] = '♝'
    elif piece == 'p':
        given_board[move_to] = '♞'
    elif piece == 't':
        given_board[move_to] = '♜'
    elif piece == 'r':
        given_board[move_to] = '♖'
    elif piece == 'n':
        given_board[move_to] = '♘'
    elif piece == 'b':
        given_board[move_to] = '♗'
    elif piece == 'q':
        given_board[move_to] = '♕'
    else:
        print("error while promoting piece")
