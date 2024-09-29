
##     ##    ###    #### ##    ##
###   ###   ## ##    ##  ###   ##
#### ####  ##   ##   ##  ####  ##
## ### ## ##     ##  ##  ## ## ##
##     ## #########  ##  ##  ####
##     ## ##     ##  ##  ##   ###
##     ## ##     ## #### ##    ##

#       the main function and a small choice menu

#needed to make a backup of the board
import copy
#validates moves for both parties
import movechecker
#makes moves for both parties
import mover
#other functions
import functions
from chess.functions import print_board
from chess.mover import make_move


def main(given_fen:str):
    """calls all functions and checks for faults"""
    game_over = False
    depth = 0

    while depth not in range (1,19):
        depth = int(input("Op welke moeilijkheidsgraad wil je spelen? (1-18):\n"))

    depth = str(depth)
    #create board storing given depth
    board = functions.create_board(given_fen, depth)

    while not game_over:
        #we make a deep copy of the board to restore it if we make an illegal move only the API catches
        previous_board = copy.deepcopy(board)
        #custom function that prints the chess board
        functions.print_board(board)

        #we ask for a move and check if it is legal as much as we can. Together with the API it's pretty airtight
        #legality has to be earned
        legal = False
        #check for the obscure 50 turn chess rule
        check_halfmoves(board)

        while not legal:
            #get the move eg: A1B1
            move = input("uw zet: ")

            #check for stop
            if move.lower() == "stop":
                exit(0)

            #check if move has a length of 4
            if len(move) != 4:
                legal = False
                print("ongeldige zet")
                continue
            #convert to 1121
            move = functions.uci_to_numeric(move)
            #split into 11, 21. our 'from' and 'to' values and check for legality using our function in movechecker
            legal = movechecker.is_legal(board, move[0], move[1])

            #if it's an illegal move we ask again
            if not legal:
                print("ongeldige zet")
        #update the board with the players move
        board = mover.make_move(board, move[0], move[1])




        #ask the API for a responding move
        opponent_move = (functions.get_stockfish_move(board))
        # if the API returns -1 it found a mistake. We revert the move and ask for a new one
        if opponent_move == -1:
            board = previous_board
            print("ongeldige zet")
            continue

        # if return is None, the API is offline or did not respond
        if opponent_move is None:
            print("geen reactie gekregen van API... bent u online?")
            break

        #check for mate
        if board[8] == -1:
            make_move(board, opponent_move[0], opponent_move[1])
            print_board(board)
            print("Je staat schaakmat,\nGoed gespeeld!")
            game_over = True

        elif opponent_move is False:
            print ("schaakmat! Je hebt gewonnen")
            game_over = True

        else:
            #the move was legal and a possible captured piece is added to the players total
            #we kept this piece in a purgatory in case the move is reset. This could not be needed, but I'm not sure
            if board[6] != '':
                print(f"jij hebt {board[6]} gepakt")
                #update players total
                board[5] += board[6]
                #reset the piece-purgatory
                board[6] = ''
            #now we make the move the opponent gave us and we restart the loop
            mover.make_move(board, opponent_move[0], opponent_move[1])


def check_halfmoves(board):
    """checks for obscure chess rule"""
    if board[2] >= 50:
        print("er zijn 50 zetten gedaan waarbij geen stuk is veroverd of een pion is verzet.")
        print("volgens de schaakregels mag u nu een remise afdwingen. Wilt u dit doen? ja/nee")

        if input().lower() == 'ja':
            print("het is een remise. Goed gespeeld!")
            exit(0)


##     ## ######## ##    ## ##     ##
###   ### ##       ###   ## ##     ##
#### #### ##       ####  ## ##     ##
## ### ## ######   ## ## ## ##     ##
##     ## ##       ##  #### ##     ##
##     ## ##       ##   ### ##     ##
##     ## ######## ##    ##  #######

reaction = False
standard_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

print("\nWelkom!")
while not reaction:
    #this is the main menu where you can play with a default fen, put in a custom fen or try a puzzle


    print("1: spel tegen de computer")
    print("2: puzzel van de dag")
    print("3: eigen FEN code invoeren (u speelt als wit)")
    print("4: uitleg over het spel")
    answer = input()

    #put in the default fen and run main
    if answer == "1":
        reaction = True
        main(standard_fen)

    #get a fen from the chess.com API and run main
    elif answer == "2":
        print("wacht op reactie..,.")
        fen = functions.chessdotcom_api()
        if fen is None:
            print("geen reactie gekregen van API... bent u online?\n\n")
            reaction = False
            continue
        reaction = True
        main(fen)

    #put in your own fen and run main
    elif answer == "3":
        good = False
        while not good:
            fen = input("FEN code:\n")
            if type(fen) == str and 'w' in fen:
                good = True
            else:
                print("ongeldige FEN code. Speelt u als wit?")
        main(fen)
        reaction = True
    elif answer == '4':
        print("""
        Dit spel gebruikt UCI notatie;
        typ a2a4 om een stuk van a2 naar a4 te bewegen. Hoe de stukken mogen bewegen kunt u hier lezen:
        https://www.chess.com/learn-how-to-play-chess#chess-pieces-move
        rokeren kan door de koning twee stappen te verplaatsen naar links of rechts, dus e1c1 voor links rokeren en e1g1 voor rechts rokeren
        en passant is door een fout in de API helaas niet mogelijk, alle andere regels zoals promotie en de 50 halfzetten regel worden wel nageleefd        
        
        """)