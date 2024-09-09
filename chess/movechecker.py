
##     ##  #######  ##     ## ########  ######  ##     ## ########  ######  ##    ## ######## ########
###   ### ##     ## ##     ## ##       ##    ## ##     ## ##       ##    ## ##   ##  ##       ##     ##
#### #### ##     ## ##     ## ##       ##       ##     ## ##       ##       ##  ##   ##       ##     ##
## ### ## ##     ## ##     ## ######   ##       ######### ######   ##       #####    ######   ########
##     ## ##     ##  ##   ##  ##       ##       ##     ## ##       ##       ##  ##   ##       ##   ##
##     ## ##     ##   ## ##   ##       ##    ## ##     ## ##       ##    ## ##   ##  ##       ##    ##
##     ##  #######     ###    ########  ######  ##     ## ########  ######  ##    ## ######## ##     ##

#       biggest function, not that complicated
#       generates valid moves for every possible piece, deals with edge cases
#       input the move you want to make
#       returns if the move is valid or not
#       does not deal with mate, as this is caught by the chess-API

fen_sequence = (18, 28, 38, 48, 58, 68, 78, 88
                    , 17, 27, 37, 47, 57, 67, 77, 87
                    , 16, 26, 36, 46, 56, 66, 76, 86
                    , 15, 25, 35, 45, 55, 65, 75, 85
                    , 14, 24, 34, 44, 54, 64, 74, 84
                    , 13, 23, 33, 43, 53, 63, 73, 83
                    , 12, 22, 32, 42, 52, 62, 72, 82
                    , 11, 21, 31, 41, 51, 61, 71, 81)

#this list will be filles with all the possible moves a piece can make. Sometimes includes the tile the piece is on,
#but that move is prohibited later on
allowed_moves = None

#returns all the possible moves for a diagonally moving piece, used for bisschop and queen
def diagonal_moves(given_board,move_from):
    possible_moves = []

    # checks upper right
    current = move_from
    while given_board[current] == ' ' or given_board[current] == '♝' or given_board[current] == '♛':
        possible_moves.append(current)
        current = current + 11
        if current not in fen_sequence:
            break
    possible_moves.append(current)

    # checks lower right
    current = move_from
    while given_board[current] == ' ' or given_board[current] == '♝' or given_board[current] == '♛':
        possible_moves.append(current)
        current = current + 9
        if current not in fen_sequence:
            break
    possible_moves.append(current)

    #checks lower left
    current = move_from
    while given_board[current] == ' ' or given_board[current] == '♝' or given_board[current] == '♛':
        possible_moves.append(current)
        current = current -11
        if current not in fen_sequence:
            break
    possible_moves.append(current)

    #checks upper left
    current = move_from
    while given_board[current] == ' ' or given_board[current] == '♝' or given_board[current] == '♛':
        possible_moves.append(current)
        current = current - 9
        if current not in fen_sequence:
            break
    possible_moves.append(current)
    return possible_moves

#returns all the possible moves for a straight moving piece. used for rook and queen
def straight_moves(given_board,move_from):
    possible_moves = []

    #checks upper right
    current = move_from
    while given_board[current] == ' ' or given_board[current] == '♜' or given_board[current] == '♛':
        possible_moves.append(current)
        current = current + 1
        if current not in fen_sequence:
            break
    possible_moves.append(current)

    #checks lower right
    current = move_from
    while given_board[current] == ' ' or given_board[current] == '♜' or given_board[current] == '♛':
        possible_moves.append(current)
        current = current - 1
        if current not in fen_sequence:
            break
    possible_moves.append(current)

    #checks lower left
    current = move_from
    while given_board[current] == ' ' or given_board[current] == '♜' or given_board[current] == '♛':
        possible_moves.append(current)
        current = current - 10
        if current not in fen_sequence:
            break
    possible_moves.append(current)

    #checks upper left
    current = move_from
    while given_board[current] == ' ' or given_board[current] == '♜' or given_board[current] == '♛':
        possible_moves.append(current)
        current = current + 10
        if current not in fen_sequence:
            break
    possible_moves.append(current)
    return possible_moves



#checks if a move is legal. These are the basic checks like not going outside the board and not capturing own pieces
def is_legal(given_board, move_from: int, move_to: int):

    own_pieces = ['♟', '♜', '♞', '♝', '♛', '♚']
    #used for the 2-step move of a pawn
    move_from_y = int(str(move_from)[1])

    allowed_moves = []
    if move_to not in fen_sequence or move_from not in fen_sequence:
        return False
    elif move_from == move_to:
        return False
    elif given_board[move_from] == ' ':
        return False
    elif given_board[move_to] in own_pieces:
        return False




    ########     ###    ##      ## ##    ##
    ##     ##   ## ##   ##  ##  ## ###   ##
    ##     ##  ##   ##  ##  ##  ## ####  ##
    ########  ##     ## ##  ##  ## ## ## ##
    ##        ######### ##  ##  ## ##  ####
    ##        ##     ## ##  ##  ## ##   ###
    ##        ##     ##  ###  ###  ##    ##

    #check for pawn
    elif given_board[move_from] == '♟':
        #is allowed forward
        if move_from + 1 in fen_sequence:
            allowed_moves.append(move_from + 1)
        #is allowed 2 forward if on row 2 and way is clear
        if move_from + 1 in fen_sequence and  move_from_y == 2 and given_board[move_from + 1] == ' ':
            allowed_moves.append(move_from + 2)
        if move_from - 9 in fen_sequence and  given_board[move_from - 9] != ' ':
            allowed_moves.append(move_from - 9)
        if move_from + 11 in fen_sequence and given_board[move_from + 11] != ' ':
            allowed_moves.append(move_from + 11)





    ##     ##  #######  ########   ######  ########
    ##     ## ##     ## ##     ## ##    ## ##                     [ ][2][ ][3][ ]
    ##     ## ##     ## ##     ## ##       ##                     [1][ ][ ][ ][4]
    ######### ##     ## ########   ######  ######                 [ ][ ][♞][ ][ ]
    ##     ## ##     ## ##   ##         ## ##                     [5][ ][ ][ ][8]
    ##     ## ##     ## ##    ##  ##    ## ##                     [ ][6][ ][7][ ]
    ##     ##  #######  ##     ##  ######  ########

    elif given_board[move_from] == '♞':

        #1
        if move_from - 19 in fen_sequence:
            allowed_moves.append(move_from - 19)
        #2
        if move_from - 8 in fen_sequence:
            allowed_moves.append(move_from - 8)
        #3
        if move_from + 12 in fen_sequence:
            allowed_moves.append(move_from + 12)
        #4
        if move_from + 21 in fen_sequence:
            allowed_moves.append(move_from + 21)
        #5
        if move_from - 21 in fen_sequence:
            allowed_moves.append(move_from - 21)
        #6
        if move_from - 12 in fen_sequence:
            allowed_moves.append(move_from - 12)
        #7
        if move_from + 8 in fen_sequence:
            allowed_moves.append(move_from + 8)
        #8
        if move_from + 19 in fen_sequence:
            allowed_moves.append(move_from + 19)

    ########  ####  ######   ######  ##     ##  #######  ########
    ##     ##  ##  ##    ## ##    ## ##     ## ##     ## ##     ##
    ##     ##  ##  ##       ##       ##     ## ##     ## ##     ##
    ########   ##   ######  ##       ######### ##     ## ########
    ##     ##  ##        ## ##       ##     ## ##     ## ##
    ##     ##  ##  ##    ## ##    ## ##     ## ##     ## ##
    ########  ####  ######   ######  ##     ##  #######  ##

    elif given_board[move_from] == '♝':
        allowed_moves = diagonal_moves(given_board, move_from)


    ########   #######   #######  ##    ##
    ##     ## ##     ## ##     ## ##   ##
    ##     ## ##     ## ##     ## ##  ##
    ########  ##     ## ##     ## #####
    ##   ##   ##     ## ##     ## ##  ##
    ##    ##  ##     ## ##     ## ##   ##
    ##     ##  #######   #######  ##    ##

    elif given_board[move_from] == '♜':
        allowed_moves = straight_moves(given_board, move_from)

    #######  ##     ## ######## ######## ##    ##
    ##     ## ##     ## ##       ##       ###   ##
    ##     ## ##     ## ##       ##       ####  ##
    ##     ## ##     ## ######   ######   ## ## ##
    ##  ## ## ##     ## ##       ##       ##  ####
    ##   ###  ##     ## ##       ##       ##   ###
     ###   ##  #######  ######## ######## ##    ##

    elif given_board[move_from] == '♛':
        allowed_moves = straight_moves(given_board, move_from)
        allowed_moves += diagonal_moves(given_board, move_from)

    ##    ## #### ##    ##  ######
    ##   ##   ##  ###   ## ##    ##
    ##  ##    ##  ####  ## ##
    #####     ##  ## ## ## ##   ####
    ##  ##    ##  ##  #### ##    ##
    ##   ##   ##  ##   ### ##    ##
    ##    ## #### ##    ##  ######

    elif given_board[move_from] == '♚':
        if move_from + 1 in fen_sequence:
            allowed_moves.append(move_from + 1)
        if move_from - 1 in fen_sequence:
            allowed_moves.append(move_from - 1)
        if move_from + 10 in fen_sequence:
            allowed_moves.append(move_from + 10)
        if move_from - 10 in fen_sequence:
            allowed_moves.append(move_from - 10)
        if move_from + 11 in fen_sequence:
            allowed_moves.append(move_from + 11)
        if move_from - 11 in fen_sequence:
            allowed_moves.append(move_from - 11)
        if move_from + 9 in fen_sequence:
            allowed_moves.append(move_from + 9)
        if move_from - 9 in fen_sequence:
            allowed_moves.append(move_from - 9)
        if 'Q' in given_board[7] and given_board[31] == ' ' and given_board[21] == ' ' and not given_board[8]:
            allowed_moves.append(31)
        if 'K' in given_board[7] and given_board[61] == ' ' and given_board[71] == ' ' and not given_board[8]:
            allowed_moves.append(71)


    #if the move is in the allowed list the function returns true
    if move_to in allowed_moves:
        return True
    return False






