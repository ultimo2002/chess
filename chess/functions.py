
######## ##     ## ##    ##  ######  ######## ####  #######  ##    ##  ######
##       ##     ## ###   ## ##    ##    ##     ##  ##     ## ###   ## ##    ##
##       ##     ## ####  ## ##          ##     ##  ##     ## ####  ## ##
######   ##     ## ## ## ## ##          ##     ##  ##     ## ## ## ##  ######
##       ##     ## ##  #### ##          ##     ##  ##     ## ##  ####       ##
##       ##     ## ##   ### ##    ##    ##     ##  ##     ## ##   ### ##    ##
##        #######  ##    ##  ######     ##    ####  #######  ##    ##  ######

#       7 smaller functions including the 2 API requests

#needed for making and using requests respectively
import requests
import json


# the variables that are used to fill the board stored in order
fen_sequence = (18, 28, 38, 48, 58, 68, 78, 88
                , 17, 27, 37, 47, 57, 67, 77, 87
                , 16, 26, 36, 46, 56, 66, 76, 86
                , 15, 25, 35, 45, 55, 65, 75, 85
                , 14, 24, 34, 44, 54, 64, 74, 84
                , 13, 23, 33, 43, 53, 63, 73, 83
                , 12, 22, 32, 42, 52, 62, 72, 82
                , 11, 21, 31, 41, 51, 61, 71, 81)


#creates a board from a fen code. a fen code is a code that describes what pieces are on the board, and where they are. It also contains meta info about the game,
# like the turn
def create_board(fen:str, depth:int):
    """creates a board"""
    # Initialize the variables list with empty spaces
    board = [0] * 89

    #the first 10 variables (among others) are not used due to how the name corresponds with the numeric notation of each coordinate
    #we use these variables to store information about the game in the board itself to be read by other functions using the board



    # 0 index is used to keep track of who's turn it is POSSIBLY OVERWRITTEN BY FEN READER BELOW
    board[0] = 'w'
    # 1 index is used to keep track of an en passant target square in numeric notation
    board[1] = ''
    # 2 index is used to keep track of halfmoves
    board[2] = 0
    # 3 index is used to keep track of fullmoves
    board[3] = 0
    # 4 index is used to store pieces captured by opponent (black)
    board[4] = ''
    # 5 index is used to store pieces captured by player (white)
    board[5] = ''
    # 6 index stores a piece that is captured if the move goes through
    board[6] = ''
    # 7 index stores castling options for player OVERWRITTEN BY FEN READER
    board[7] = 'KQkq'
    # 8 stores mate true or false
    board[8] = False
    # 9 stores promotion by opponent
    board[9] = False
    # 10 stores the difficulty level (depth)
    board[10] = depth
    fen_to_board(board, fen)

    #the finished board is returned to the main function which will now ask for a move
    return board





# set up pieces using fen code
def fen_to_board(board, fen):
    """takes a fen and fills a board"""
    fen = fen.replace('/', '')
    # 2 counters are needed because the fen has fewer characters than the board due to the summation of empty spaces (8 == ' ', ' ', ' ', ' ',' ', ' ', ' ', ' ',)
    y = 0
    i = y
    # goes through all the pieces to place the piece in the fen code on the board
    while y < len(fen):
        piece = fen[y]

        if piece == 'r':
            board[fen_sequence[i]] = '♖'
        elif piece == 'n':
            board[fen_sequence[i]] = '♘'
        elif piece == 'b':
            board[fen_sequence[i]] = '♗'
        elif piece == 'q':
            board[fen_sequence[i]] = '♕'
        elif piece == 'k':
            board[fen_sequence[i]] = '♔'
        elif piece == 'p':
            board[fen_sequence[i]] = '♙'
        elif piece == 'R':
            board[fen_sequence[i]] = '♜'
        elif piece == 'N':
            board[fen_sequence[i]] = '♞'
        elif piece == 'B':
            board[fen_sequence[i]] = '♝'
        elif piece == 'Q':
            board[fen_sequence[i]] = '♛'
        elif piece == 'K':
            board[fen_sequence[i]] = '♚'
        elif piece == 'P':
            board[fen_sequence[i]] = '♟'
        elif piece == ' ':
            y += 1
            i += 1
            continue
        elif piece == ' ' and (board[0] == 'w' or board[0] == 'b'):
            break
        elif piece == '-':
            continue
        # store the turn in our designated variable
        elif piece == 'w':
            board[0] = 'w'
            break
        elif piece == 'b':
            board[0] = 'b'
            break
        else:
            # small loop to place 8 spaces if an 8 is encountered. 'i' keeps counting, 'y' stagnates because it indexes the fen code
            x = int(piece)
            while x > 0:
                board[fen_sequence[i]] = ' '
                x -= 1
                i += 1
            y += 1
            continue
        i += 1
        y += 1


#converts UCI notation to numeric notation
#input something like 'a2a3'
#output a tuple containing (12,13) the numeric notation that we will use in all calculations
def uci_to_numeric(UCI:str):
    """converts user input to usable move variables"""
    result = ""
    move_from = ''
    move_to = ''
    for char in UCI:
        if char.isalpha():
            # Convert the letter to its corresponding alphabet index
            index = ord(char.lower()) - ord('a') + 1
            result += str(index)
        else:
            result += char
    for i in range (0, len(result)):
        if i < len(result)/2:
            move_from += result[i]
        else:
            move_to += result[i]
    return int(move_from), int(move_to)

#lets the API check the board, return None if the move was invalid, it will then be reverted by main()
#otherwise return a move (a tuple with two numeric coordinates)
def get_stockfish_move(given_board):
    """gets a move using the api and makes it"""
    #get response from API
    #turn json into usable dictionary
    response = stockfish_api(board_to_fen(given_board), given_board[10])
    if response == None:
        return None
    response = json.dumps(response)
    variables = json.loads(response)

    #here we check if the API spotted an error in the fen that we did not check for, like a move under mate. We restore the board to a previous state in main()
    if variables['type'] == 'error':
        # is the API cant make a valid move it is in checkmate. We return False to end the game
        if variables['error'] == 'INVALID_INPUT':
            return False

        return -1

    #reading response move from dictionary acquired from the API
    else:
        response_move = (int(variables['fromNumeric']), int(variables['toNumeric']))

    #print some info about the game
    print(f"tegenstander speelt {variables['move']}. Uw winkans is {int(variables['winChance'])}%")

    #store possible mate in designated variable
    given_board[8] = variables['mate']

    #store possible promotion
    if variables['promotion'] != '':
        given_board[9] = variables['promotion']

    return response_move


# Print the board. All the variables match up. 11 is a1, and 88 is h8
def print_board(board):
    """prints the board"""
    print(f"""
    8 [{board[18]}][{board[28]}][{board[38]}][{board[48]}][{board[58]}][{board[68]}][{board[78]}][{board[88]}]
    7 [{board[17]}][{board[27]}][{board[37]}][{board[47]}][{board[57]}][{board[67]}][{board[77]}][{board[87]}]          {board[4]}
    6 [{board[16]}][{board[26]}][{board[36]}][{board[46]}][{board[56]}][{board[66]}][{board[76]}][{board[86]}]
    5 [{board[15]}][{board[25]}][{board[35]}][{board[45]}][{board[55]}][{board[65]}][{board[75]}][{board[85]}]
    4 [{board[14]}][{board[24]}][{board[34]}][{board[44]}][{board[54]}][{board[64]}][{board[74]}][{board[84]}]
    3 [{board[13]}][{board[23]}][{board[33]}][{board[43]}][{board[53]}][{board[63]}][{board[73]}][{board[83]}]
    2 [{board[12]}][{board[22]}][{board[32]}][{board[42]}][{board[52]}][{board[62]}][{board[72]}][{board[82]}]          {board[5]}
    1 [{board[11]}][{board[21]}][{board[31]}][{board[41]}][{board[51]}][{board[61]}][{board[71]}][{board[81]}]
       a  b  c  d  e  f  g  h""")


# function that makes a fen from current board layout
def board_to_fen(given_board: list):
    """reads fen from board to use with api"""

    #counts empty spaces
    counter = 0
    #counts when the row is over and a / is needed
    row_counter = 0

    fen = ""
    #the fen sequence can be found at the top of the page and stores all the variables that are actually part of the board
    for tile in fen_sequence:
        #stop counting empty tiles if the row ends
        if row_counter == 8:
            if counter != 0:
                fen += str(counter)
                counter = 0
        #put backslashes in the fen code every 8 tiles
            fen += '/'
            row_counter = 0
        #counts empty space
        if given_board[tile] == ' ':
            counter += 1
            row_counter += 1
            continue
        #identify piece on the square and put it in the fen code
        if counter != 0:
                fen += str(counter)
                counter = 0
        if given_board[tile] == '♖':
            fen += 'r'
            row_counter += 1
        if given_board[tile] == '♘':
            fen += 'n'
            row_counter += 1
        if given_board[tile] == '♗':
            fen += 'b'
            row_counter += 1
        if given_board[tile] == '♕':
            fen += 'q'
            row_counter += 1
        if given_board[tile] == '♔':
            fen += 'k'
            row_counter += 1
        if given_board[tile] == '♙':
            fen += 'p'
            row_counter += 1
        if given_board[tile] == '♜':
            fen += 'R'
            row_counter += 1
        if given_board[tile] == '♞':
            fen += 'N'
            row_counter += 1
        if given_board[tile] == '♝':
            fen += 'B'
            row_counter += 1
        if given_board[tile] == '♛':
            fen += 'Q'
            row_counter += 1
        if given_board[tile] == '♚':
            fen += 'K'
            row_counter += 1
        if given_board[tile] == '♟':
            fen += 'P'
            row_counter += 1
    if counter != 0:
        fen += str(counter)
    #add whose turn it is to the fen code. We stored this in index 0 of the board
    fen += f" {given_board[0]} "

    #add abilities to castle to the fen code
    default = '-'
    castling = ''
    if given_board[81] == '♜' and given_board[51] == '♚':
        castling += "K"
        given_board[7] += "K"
    if given_board[11] == '♜' and given_board[51] == '♚':
        castling += "Q"
        given_board[7] += "Q"
    if given_board[88] == '♖' and given_board[58] == '♔':
        castling += "k"
    if given_board[88] == '♖' and given_board[58] == '♔':
        castling += "q"
    if len(castling) != 0:
        fen += castling
    else:
        fen += default
    #add en passant target square, stored in index 1
    if given_board[1] == '':
        fen += " -"
    else:
        fen += " -"

    # ##### I wrote this correctly, but the API won't accept a completely valid en passant target square which is why I have to comment this out
    # your opponent cannot use en passant against you because of this API error. You are still able to en passant the opponent

    # else:
    #     string = given_board[1]
    #     letter = string[0]
    #     number = string[1]
    #     letter = chr(int(letter) + ord('a') - 1)
    #
    #     fen += f" {letter}{number}"

    #these two values have to be in the fen code, but they are not useful to my program so they are not calculated
    #add halfmoves stored in index 2
    fen += " " + str(given_board[2])
    #add fullmoves stored in index 3
    fen += " " + str(given_board[3])
    return fen










  ##      #####     #       #
 #  #    #     #    #     # #
#    #   #     #    #       #
######   ######     #       #
#    #   #          #       #
#    #   #          #       #
#    #   #          #     #####

# This API evaluates a fen and gives a move back using stockfish AI
# input: fen in string format
# returns data from chess-api
url_1 = "https://chess-api.com/v1"
def stockfish_api(data, depth):
    """does a call to the stockfish API"""
    if data is None:
        data = {}
    try:
        response = requests.post(
            url_1,
            headers={"Content-Type": "application/json"},
            json={"fen": data, "depth": int(depth)}
        )
    except:
        return None
    print("huidige FEN code: " + data)
    return response.json()



  ##      #####     #      ####
 #  #    #     #    #     #    #
#    #   #     #    #          #
######   ######     #         #
#    #   #          #       #
#    #   #          #      #
#    #   #          #     ######

#this API gets a puzzle fen to start a game with
#no input
#returns a fen from chess.com
url_2 =  "https://api.chess.com/pub/puzzle/random"
def chessdotcom_api():
    """does a call to the chess.com API"""
    fen = ""
    #we want a puzzle where we play as white, because that is how I set up the program. I haven't seen a b puzzle yet, but this loop is a precaution
    while 'w' not in fen:
        try:
            response = requests.get(
                url_2,
                #the api doesn't need a token, but for some reason it wants an email adress. I just gave it the one I use on chess.com
                headers={"Content-Type": "application/json", "Accept": "application/json", "User-Agent": "timo.rouw@outlook.com"}
            )
        except:
            return None
        response = json.dumps(response.json())
        variables = json.loads(response)
        fen = variables['fen']

    #print some fun info about the puzzle
    print(variables['title'])
    print(variables['fen'])
    print("see image:")
    print(variables['image'])
    #return the fen code of this puzzle. This is used to set up the board
    return fen
