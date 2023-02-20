
#Ka - khan 
#K0 - prince 
#K1 - adventageous king 
#Ad - administrator 
#Vi - visier
#Gi - giraffe
#Ta - tali'a (picket (bishop))
#Mo - mongol 
#Rk - rook
#El - elepant 
#Ca - camel 
#We - war engine
#p[x] - pawn[type]
#--- - empty space

import pygame as p


"""
the Move class returns an object which contains the start and end square of a move 
as well as the piece moved and the piece captured
"""
class Move():
    ranksToRows = {"1": 9, "2": 8, "3": 7, "4": 6, "5": 5, "6": 4, "7": 3, "8": 2, "9": 1, "10": 0}
    rowsToRanks= {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8, "j": 9, "k": 10}
    colsToFiles = {v: l for l, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startCol = startSq[0] 
        self.startRow = startSq[1] 
        self.endCol = endSq[0] 
        self.endRow = endSq[1] 

        self.pieceMoved = board[self.startCol][self.startRow]
        self.pieceCaptured = board[self.endCol][self.endRow]

        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol


        def __eq__(self, other):
            if isinstance(other, Move):
                return self.moveID == other.moveID
            return False


WIDTH = HEIGHT = 1040
DIMENSION = 13
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
white = p.Color("#dad8da")
black = p.Color("#696369")  
green = p.Color("#303b47")
whiteKingLocation = (8,5)
blackKingLocation = (1,5)
whiteRoyalty = 1
blackRoyalty = 1
turnCount = 0
checkmate = False
draw = False
pawnXW = False
pawnXB = False
moveMade = False
whiteToMove = True
playerOne = True
playerTwo = False
winner = ""
validMoves = []
moveLog = []

"""
possible starting positions for the pieces according to various accounts of the game
"""
masculineArray = [
    ["bEl", "---", "bCa", "---", "bWe", "---", "bWe", "---", "bCa", "---", "bEl"],
    ["bRk", "bMo", "bTa", "bGi", 'bVi', "bKa", "bAd", "bGi", "bTa", "bMo", "bRk"],
    ["bpR", "bpM", "bpT", "bpG", "bpV", "bpK", "bpA", "bpE", "bpC", "bpW", "bp0"],
    ["---", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---"],
    ["---", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---"],
    ["---", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---"],
    ["---", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---"],
    ["wp0", "wpW", "wpC", "wpE", "wpA", "wpK", "wpV", "wpG", "wpT", "wpM", "wpR"],
    ["wRk", "wMo", "wTa", "wGi", 'wAd', "wKa", "wVi", "wGi", "wTa", "wMo", "wRk"],
    ["wEl", "---", "wCa", "---", "wWe", "---", "wWe", "---", "wCa", "---", "wEl"]
]       
feminineArray = [
    ["bEl", "---", "bCa", "---", "bVi", "bKa", "bAd", "---", "bCa", "---", "bEl"],
    ["bRk", "bMo", "bTa", "bGi", 'bWe', "bpK", "bWe", "bGi", "bTa", "bMo", "bRk"],
    ["bpR", "bpM", "pbT", "bpG", "bpV", "---", "bpA", "bpE", "bpC", "bpW", "bp0"],
    ["---", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---"],
    ["---", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---"],
    ["---", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---"],
    ["---", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---"],
    ["wp0", "wpW", "wpC", "wpE", "wpA", "---", "wpV", "wpG", "wpT", "wpM", "wpR"],
    ["wRk", "wMo", "wTa", "wGi", 'wWe', "wpK", "wWe", "wGi", "wTa", "wMo", "wRk"],
    ["wEl", "---", "wCa", "---", "wAd", "wKa", "wVi", "---", "wCa", "---", "wEl"]
]
thirdArray = [
    ["bEl", "---", "bCa", "---", "bVi", "bKa", "bAd", "---", "bCa", "---", "bEl"],
    ["bRk", "bMo", "bWe", "bTa", 'bGi', "bpK", "bGi", "bTa", "bWe", "bMo", "bRk"],
    ["bpR", "bpM", "pbT", "bpG", "bpV", "---", "bpA", "bpE", "bpC", "bpW", "bp0"],
    ["---", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---"],
    ["---", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---"],
    ["---", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---"],
    ["---", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---"],
    ["wp0", "wpW", "wpC", "wpE", "wpA", "---", "wpV", "wpG", "wpT", "wpM", "wpR"],
    ["wRk", "wMo", "wWe", "wTa", 'wGi', "wpK", "wGi", "wTa", "wWe", "wMo", "wRk"],
    ["wEl", "---", "wCa", "---", "wAd", "wKa", "wVi", "---", "wCa", "---", "wEl"]
]
testBoard = [
    ["---", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---"],    
    ["---", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---"],
    ["---", "wVi", "---", "---", "---", "---", "---", "---", "---", "---", "---"],
    ["---", "---", "---", "---", "---", "bRk", "---", "---", "---", "---", "---"],
    ["---", "---", "wTa", "---", "---", "---", "---", "---", "---", "---", "wKa"],
    ["---", "---", "---", "---", "wGi", "---", "---", "---", "---", "---", "---"],
    ["---", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---"],
    ["---", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---"],
    ["---", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---"],
    ["bKa", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---"]
]

board = masculineArray #this is the standard set up
#board = feminineArray
#board = thirdArray
#board = testBoard

"""
initialize a global dictionary of images. This is called once in main
"""
def loadImages():
    pieces = ["bKa", "wKa", "bK0", "wK0", "bK1", "wK1", "bAd", "wAd", "bVi", "wVi", "bGi", "wGi", "bTa", "wTa", "bMo", "wMo", "bRk", "wRk", "bEl", "wEl", "bCa", "wCa", "bWe", "wWe",
              "wp0","wp1","wpx", "wpK", "wpA", "wpV", "wpG", "wpT", "wpM", "wpR", "wpE", "wpC", "wpW", "bp0","bp1","bpx", "bpK", "bpA", "bpV", "bpG", "bpT", "bpM", "bpR", "bpE", "bpC", "bpW"]

    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    
def getChessNotation(move):
    return getRankFile(move.startRow, move.startCol) + getRankFile (move.endRow, move.endCol)

def getRankFile(r, c):
    ranksToRows = {"1": 9, "2": 8, "3": 7, "4": 6, "5": 5, "6": 4, "7": 3, "8": 2, "9": 1, "10": 0}
    rowsToRanks= {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8, "j": 9, "k": 10}
    colsToFiles = {v: l for l, v in filesToCols.items()}
    return colsToFiles[c] + rowsToRanks[r]

def makeMove(move):
    global whiteKingLocation, blackKingLocation
    pieceMoved = move.pieceMoved
    board[move.endCol][move.endRow]=board[move.startCol][move.startRow]
    board[move.startCol][move.startRow] = "---"
    if(pieceMoved == "wKa"):
        whiteKingLocation = (move.endCol,move.endRow)
    if(pieceMoved == "bKa"):
        blackKingLocation = (move.endCol,move.endRow)
    return(whiteKingLocation,blackKingLocation)

def undoMove():
    global moveLog
    if(len(moveLog) != 0):
        move = moveLog.pop()
        board[move.startCol][move.startRow] = move.pieceMoved
        board[move.endCol][move.endRow] = move.pieceCaptured
    findKings()
    moveMade = True

def main():
    global whiteToMove, whiteKingLocation, blackKingLocation, moveMade, winner, validMoves, playerOne, playerTwo
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    validMoves = getValidMoves()
    loadImages()
    findKings()
    running = True
    sqSelected = ()
    playerClicks = []
    while(running):
        isHumanTurn = (whiteToMove and playerOne) or (not whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if isHumanTurn:
                    location = p.mouse.get_pos() #(x,y)
                    row = (location[0]//SQ_SIZE)-1
                    col = (location[1]//SQ_SIZE)-1
                    print("col =",col," row =",row)
                    if(p.mouse.get_pos()[0] > 15 and p.mouse.get_pos()[1] > 15 and p.mouse.get_pos()[0] < 250 and p.mouse.get_pos()[1] < 70):
                        if canDraw(whiteToMove) == True:
                            callDraw()
                    if(col >= 0 and col <= 9 and row >= 0 and row <= 10):
                        if sqSelected == (col,row): #same square
                            sqSelected = ()
                            playerClicks = []
                        else:
                            sqSelected = (col,row)
                            playerClicks.append(sqSelected)
                        if len(playerClicks) == 2:
                            move = Move(playerClicks[0], playerClicks[1], board)
                            checkMove = [(move.startCol,move.startRow),(move.endCol,move.endRow)]
                            if(checkMove in validMoves):
                                if (board[move.startCol][move.startRow] != "---"):
                                    makeMove(move)
                                    moveLog.append(move)
                                    whiteToMove = not whiteToMove
                                    if board[0][0] == "wpx" or board[9][10] == "bpx":
                                        checkPawnForks()
                                    if len(validMoves) == 0:
                                        if whiteToMove: 
                                            winner = "b"
                                        else: 
                                            winner = "w"
                                    moveMade = True
                            sqSelected = ()
                            playerClicks = []
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    undoMove()

        if not isHumanTurn and winner == "":
            AIMove = findGreedyMove()
            if AIMove is not None:
                AIMove = Move(AIMove[0], AIMove[1], board)
                makeMove(AIMove)
                moveLog.append(AIMove)
                whiteToMove = not whiteToMove
                if board[0][0] == "wpx" or board[9][10] == "bpx":
                    checkPawnForks()
            validMoves=getValidMoves()
            if len(validMoves) == 0:
                if whiteToMove: 
                    winner = "b"
                else: 
                    winner = "w"
            moveMade = True
        if moveMade:
            #animation is broken when using undo, fix when rest of logic is finished
            animateMove(moveLog[-1], screen, clock)
            findKings()
            checkDrawOnMaterial()
            checkPromotion()
            validMoves=getValidMoves()
            moveMade = False
        drawGameState(screen, validMoves, sqSelected)
        p.display.flip()
        clock.tick(MAX_FPS)

def callDraw():
    global winner, validMoves
    validMoves = []
    winner = "d"

def checkDrawOnMaterial():
    pieceList = []
    for c in range(len(board)):
        for r in range(len(board[c])):
            if board[c][r] != "---":
                pieceList.append(board[c][r])
    if len(pieceList) == 2:
        callDraw()

def canDraw(side):
    if side: side = "w"
    else: side = "b"
    if side == "w":
        if(board[2][0][0] == "w" or board[1][0][0] == "w" or board[0][0][0] == "w"):
            if(board[2][0][1] == "K" or board[1][0][1] == "K" or board[0][0][1] == "K" ):
                return True
    if  side == "b":
        if(board[7][10][0] == "b" or board[8][10][0] == "b" or board[9][10][0] == "b"):
            if(board[7][10][1] == "K" or board[8][10][1] == "K" or board[9][10][1] == "K" ):
                return True
    return False
"""
functions to calculate moves
"""
#this function is working for white, but sees black as in check when it is not  

def getValidMoves():  
    global whiteToMove,whiteKingLocation,blackKingLocation,moveMade    
    #1) generate all ally moves
    allMoves =  getAllPossibleMoves()
    _validMoves = []
    if whiteToMove:
        royalty = whiteRoyalty
    else:
        royalty = blackRoyalty
    #2) for each move, make the move     
    for i in range(len(allMoves)):
        _move = Move([allMoves[i][0][0],allMoves[i][0][1]],[allMoves[i][1][0],allMoves[i][1][1]],board)   
        makeMove(_move)
        moveLog.append(_move)
        if(isKingInCheck() == False or royalty > 1): #only add to valid moves if king is not in check unless you have multiple royal pieces
            appendMoves(_validMoves, _move)
        undoMove()
    return _validMoves
    
def getAllPossibleMoves():
    global whiteToMove
    moves = []
    for c in range(len(board)):
        for r in range(len(board[c])):
            turn = board[c][r][0]
            if((turn == "w" and whiteToMove) or (turn == "b" and not whiteToMove)):        
                piece = board[c][r][1]
                #all piece logic
                if(piece == "p"):
                    getPawnMoves(r,c,moves)
                if(piece == "R"):
                    getRookMoves(r,c,moves)
                if(piece == "K"):
                    getKhanMoves(r,c,moves)
                if(piece == "A"):
                    getAdminMoves(r,c,moves)
                if(piece == "V"):
                    getVizierMoves(r,c,moves )
                if(piece == "W"):
                    getWarEngineMoves(r,c,moves )
                if(piece == "E"):
                    getElephantMoves(r,c,moves )
                if(piece == "M"):
                    getMongolMoves(r,c,moves )
                if(piece == "C"):
                    getCamelMoves(r,c,moves )
                if(piece == "T"):
                    getPicketMoves(r,c,moves )
                if(piece == "G"):
                    getGiraffeMoves(r,c,moves )
    return moves

def isKingInCheck():
    global whiteToMove, whiteKingLocation, blackKingLocation
    if whiteToMove:
        if(whiteRoyalty == 1):
            return isUnderAttack(whiteKingLocation[0], whiteKingLocation[1])
    else:
        if(blackRoyalty == 1):
            return isUnderAttack(blackKingLocation[0], blackKingLocation[1])

def isUnderAttack(c,r):
    global whiteToMove
    oppMoves = getOppMoves()
    for i in range(len(oppMoves)):
        if(oppMoves[i][1] == (c,r)):
            return True
    return False

def getOppMoves():
    global whiteToMove
    oppMoves = []
    whiteToMove = not whiteToMove
    oppMoves = getAllPossibleMoves()
    whiteToMove = not whiteToMove
    return oppMoves

def findKings(): 
    global whiteKingLocation, blackKingLocation, whiteRoyalty, blackRoyalty
    _whiteRoyalty = 0
    _blackRoyalty = 0
    for c in range(len(board)):
        for r in range(len(board[c])):
            if(board[c][r][0] == "w" and board[c][r][1] == "K"):
                whiteKingLocation = (c,r)
                _whiteRoyalty += 1
            if(board[c][r][0] == "b" and board[c][r][1] == "K"):
                blackKingLocation = (c,r)
                _blackRoyalty += 1
    whiteRoyalty = _whiteRoyalty
    blackRoyalty = _blackRoyalty
"""
piece logic
"""
def getPawnMoves(r,c,moves):
    global whiteToMove
    if whiteToMove:
        if c -1  >= 0:
            if board[c-1][r] == "---":#move 1
                _move = Move((c,r), (c-1,r), board)
                appendMoves(moves, _move)
            if r - 1 >= 0:#capture left
                if board[c-1][r-1][0] == "b":
                    _move = (Move((c,r),(c-1,r-1),board))
                    appendMoves(moves, _move)
            if r+1 <= 10: #capture right
                if board[c-1][r+1][0] == "b":
                    _move = (Move((c,r),(c-1,r+1),board))
                    appendMoves(moves, _move)
    else: #black to move
        if c + 1 <= 9:
            if board[c+1][r] == "---":#move 1
                _move = Move((c,r), (c+1,r), board)
                appendMoves(moves, _move)
            if r - 1 >= 0:#capture left
                if board[c+1][r-1][0] == "w":
                    _move = (Move((c,r),(c+1,r-1),board))
                    appendMoves(moves, _move)
            if r+1 <= 10: #capture right
                if board[c+1][r+1][0] == "w":
                    _move = (Move((c,r),(c+1,r+1),board))
                    appendMoves(moves, _move)

def getRookMoves(r,c,moves):
    global whiteToMove
    allyColor = "w"
    enemyColor = "b"
    if not whiteToMove:
        enemyColor = "w"
        allyColor = "b"
    spaceUp = c
    spaceDown = -((c - 10) +1)
    spaceLeft = r
    spaceRight = -((r - 9)+1)+2
    for spaces in range(spaceUp):
        newc=(c-spaces)-1
        _move = Move((c,r),(newc,r),board)
        if (board[_move.endCol][_move.endRow]) == "---":
            appendMoves(moves, _move)
        if (board[_move.endCol][_move.endRow][0]) == enemyColor:
            appendMoves(moves, _move)
            break
        if (board[_move.endCol][_move.endRow][0]) == allyColor:
            break
    for spaces in range(spaceDown):
        newc = c + spaces+1
        _move = Move((c,r),(newc,r),board)
        if (board[_move.endCol][_move.endRow]) == "---":
            appendMoves(moves, _move)
        if (board[_move.endCol][_move.endRow][0]) == enemyColor:
            appendMoves(moves, _move)
            break
        if (board[_move.endCol][_move.endRow][0]) == allyColor:
            break
    for spaces in range(spaceLeft):
        newr = r - spaces - 1
        _move = Move((c,r),(c,newr),board)
        if (board[_move.endCol][_move.endRow]) == "---":
            appendMoves(moves, _move)
        if (board[_move.endCol][_move.endRow][0]) == enemyColor:
            appendMoves(moves, _move)
            break
        if (board[_move.endCol][_move.endRow][0]) == allyColor:
            break
    for spaces in range(spaceRight):
        newr = r + spaces + 1
        _move = Move((c,r),(c,newr),board)
        if (board[_move.endCol][_move.endRow]) == "---":
            appendMoves(moves, _move)
        if (board[_move.endCol][_move.endRow][0]) == enemyColor:
            appendMoves(moves, _move)
            break
        if (board[_move.endCol][_move.endRow][0]) == allyColor:
            break

def getKhanMoves(r,c,moves):
    global whiteToMove
    allyColor = "w" if whiteToMove else "b"
    _move = []
    if(c-1 >= 0):
        if(board[c-1][r][0] != allyColor):#up 
            _move = Move((c,r),(c-1,r),board)
            appendMoves(moves, _move)
    if( c+1 <= 9):
        if(board[c+1][r][0] != allyColor):#down
            _move = Move((c,r),(c+1,r),board)
            appendMoves(moves, _move)
    if( r-1 >= 0):
        if(board[c][r-1][0] != allyColor):#left
            _move = Move((c,r),(c,r-1),board)
            appendMoves(moves, _move)
    if(r+1 <= 10):
        if(board[c][r+1][0] != allyColor):#right
            _move = Move((c,r),(c,r+1),board)
            appendMoves(moves, _move)
    if(c-1 >=0 and r-1 >= 0):
        if(board[c-1][r-1][0] != allyColor ):#up + left
            _move = Move((c,r),(c-1,r-1),board)
            appendMoves(moves, _move)
    if(c+1 <= 9  and r-1 >= 0):
        if(board[c+1][r-1][0] != allyColor):#down + left
            _move = Move((c,r),(c+1,r-1),board)
            appendMoves(moves, _move)
    if(c-1 >= 0  and r+1 <= 10):
        if(board[c-1][r+1][0] != allyColor):#up + right
            _move = Move((c,r),(c-1,r+1),board)
            appendMoves(moves, _move)
    if(c+1 <= 9  and r+1 <= 10):
        if(board[c+1][r+1][0] != allyColor):#down + right
            _move = Move((c,r),(c+1,r+1),board)
            appendMoves(moves, _move)

def getAdminMoves(r,c,moves):
    global whiteToMove
    allyColor = "w" if whiteToMove else "b"
    _move = []
    if(c-1 >=0 and r-1 >= 0):
        if(board[c-1][r-1][0] != allyColor ):#up + left
            _move = Move((c,r),(c-1,r-1),board)
            appendMoves(moves, _move)
    if(c+1 <= 9  and r-1 >= 0):
        if(board[c+1][r-1][0] != allyColor):#down + left
            _move = Move((c,r),(c+1,r-1),board)
            appendMoves(moves, _move)
    if(c-1 >= 0  and r+1 <= 10):
        if(board[c-1][r+1][0] != allyColor):#up + right
            _move = Move((c,r),(c-1,r+1),board)
            appendMoves(moves, _move)
    if(c+1 <= 9  and r+1 <= 10):
        if(board[c+1][r+1][0] != allyColor):#down + right
            _move = Move((c,r),(c+1,r+1),board)
            appendMoves(moves, _move)

def getVizierMoves(r,c,moves):
    global whiteToMove
    allyColor = "w" if whiteToMove else "b"
    _move = []
    if(c-1 >= 0):
        if(board[c-1][r][0] != allyColor):#up 
            _move = Move((c,r),(c-1,r),board)
            appendMoves(moves, _move)
    if( c+1 <= 9):
        if(board[c+1][r][0] != allyColor):#down
            _move = Move((c,r),(c+1,r),board)
            appendMoves(moves, _move)
    if( r-1 >= 0):
        if(board[c][r-1][0] != allyColor):#left
            _move = Move((c,r),(c,r-1),board)
            appendMoves(moves, _move)
    if(r+1 <= 10):
        if(board[c][r+1][0] != allyColor):#right
            _move = Move((c,r),(c,r+1),board)
            appendMoves(moves, _move)

def getElephantMoves(r,c,moves):
    global whiteToMove
    allyColor = "w" if whiteToMove else "b"
    _move = []
    if(c-2 >=0 and r-2 >= 0):
        if(board[c-2][r-2][0] != allyColor ):#up + left
            _move = Move((c,r),(c-2,r-2),board)
            appendMoves(moves, _move)
    if(c+2 <= 9  and r-2 >= 0):
        if(board[c+2][r-2][0] != allyColor):#down + left
            _move = Move((c,r),(c+2,r-2),board)
            appendMoves(moves, _move)
    if(c-2 >=0  and r+2 <= 10):
        if(board[c-2][r+2][0] != allyColor):#up + right
            _move = Move((c,r),(c-2,r+2),board)
            appendMoves(moves, _move)
    if(c+2 <= 9  and r+2 <= 10):
        if(board[c+2][r+2][0] != allyColor):#down + right
            _move = Move((c,r),(c+2,r+2),board)
            appendMoves(moves, _move)

def getWarEngineMoves(r,c,moves):
    global whiteToMove
    allyColor = "w" if whiteToMove else "b"
    _move = []
    if(c-2 >= 0):
        if(board[c-2][r][0] != allyColor):#up 
            _move = Move((c,r),(c-2,r),board)
            appendMoves(moves, _move)
    if(c+2 <= 9):
        if(board[c+2][r][0] != allyColor):#down
            _move = Move((c,r),(c+2,r),board)
            appendMoves(moves, _move)
    if( r-2 >= 0):
        if(board[c][r-2][0] != allyColor):#left
            _move = Move((c,r),(c,r-2),board)
            appendMoves(moves, _move)
    if(r+2 <= 10):
        if(board[c][r+2][0] != allyColor):#right
            _move = Move((c,r),(c,r+2),board)
            appendMoves(moves, _move)

def getMongolMoves(r,c,moves):
    global whiteToMove
    allyColor = "w" if whiteToMove else "b"
    _move = []
    if(c-2 >= 0 and r+1 <= 10):
        if(board[c-2][r+1][0] != allyColor):#up 
            _move = Move((c,r),(c-2,r+1),board)
            appendMoves(moves, _move)
    if(c-2 >= 0 and r-1 >= 0):
        if(board[c-2][r-1][0] != allyColor):#up 
            _move = Move((c,r),(c-2,r-1),board)
            appendMoves(moves, _move)
    if(c+2 <= 9 and r+1 <= 10):
        if(board[c+2][r+1][0] != allyColor):#down
            _move = Move((c,r),(c+2,r+1),board)
            appendMoves(moves, _move)
    if(c+2 <= 9 and r-1 >= 0):
        if(board[c+2][r-1][0] != allyColor):#down
            _move = Move((c,r),(c+2,r-1),board)
            appendMoves(moves, _move)
    if( r-2 >= 0 and c-1 >= 0):
        if(board[c-1][r-2][0] != allyColor):#left
            _move = Move((c,r),(c-1,r-2),board)
            appendMoves(moves, _move)
    if( r-2 >= 0 and c+1<= 9):
        if(board[c+1][r-2][0] != allyColor):#left
            _move = Move((c,r),(c+1,r-2),board)
            appendMoves(moves, _move)
    if(r+2 <= 10 and c-1 >= 0):
        if(board[c-1][r+2][0] != allyColor):#right
            _move = Move((c,r),(c-1,r+2),board)
            appendMoves(moves, _move)
    if(r+2 <= 10 and c+1 <= 9):
        if(board[c+1][r+2][0] != allyColor):#right
            _move = Move((c,r),(c+1,r+2),board)
            appendMoves(moves, _move)

def getCamelMoves(r,c,moves):
    global whiteToMove
    allyColor = "w" if whiteToMove else "b"
    _move = []
    if(c-3 >= 0 and r+1 <= 10):
        if(board[c-3][r+1][0] != allyColor):#up 
            _move = Move((c,r),(c-3,r+1),board)
            appendMoves(moves, _move)
    if(c-3 >= 0 and r-1 >= 0):
        if(board[c-3][r-1][0] != allyColor):#up 
            _move = Move((c,r),(c-3,r-1),board)
            appendMoves(moves, _move)
    if(c+3 <= 9 and r+1 <= 10):
        if(board[c+3][r+1][0] != allyColor):#down
            _move = Move((c,r),(c+3,r+1),board)
            appendMoves(moves, _move)
    if(c+3 <= 9 and r-1 >= 0):
        if(board[c+3][r-1][0] != allyColor):#down
            _move = Move((c,r),(c+3,r-1),board)
            appendMoves(moves, _move)
    if( r-3 >= 0 and c-1 >= 0):
        if(board[c-1][r-3][0] != allyColor):#left
            _move = Move((c,r),(c-1,r-3),board)
            appendMoves(moves, _move)
    if( r-3 >= 0 and c+1<= 9):
        if(board[c+1][r-3][0] != allyColor):#left
            _move = Move((c,r),(c+1,r-3),board)
            appendMoves(moves, _move)
    if(r+3 <= 10 and c-1 >= 0):
        if(board[c-1][r+3][0] != allyColor):#right
            _move = Move((c,r),(c-1,r+3),board)
            appendMoves(moves, _move)
    if(r+3 <= 10 and c+1 <= 9):
        if(board[c+1][r+3][0] != allyColor):#right
            _move = Move((c,r),(c+1,r+3),board)
            appendMoves(moves, _move)

def getPicketMoves(r,c,moves):
    global whiteToMove
    enemyColor = "b" if whiteToMove else "w"
    allyColor = "w" if whiteToMove else "b"
    _move = []
    for i in range(1,10):
        if(c-i >= 0 and r-i >= 0):
            if(board[c-i][r-i][0] == allyColor):
                break
            if (board[c-1][r-1][0]) == enemyColor:
                break
            _move = Move((c,r),(c-i,r-i),board)
            if(_move.endCol,_move.endRow) == (c-1,r-1):
                if(board[c-1][r-1] == "---"):
                    pass
                else:
                    break
            elif(_move.endCol,_move.endRow) != (c-1,r-1):
                if (board[_move.endCol][_move.endRow]) == "---":
                    appendMoves(moves, _move)
                if (board[_move.endCol][_move.endRow][0]) == enemyColor:
                    appendMoves(moves, _move)
                    break
    for i in range(1,10):
        if(c-i >= 0 and r+i <= 10):
            if(board[c-i][r+i][0] == allyColor):
                break
            if (board[c-1][r+1][0]) == enemyColor:
                break
            _move = Move((c,r),(c-i,r+i),board)
            if(_move.endCol,_move.endRow) == (c-1,r+1):
                if(board[c-1][r+1] == "---"):
                    pass
                else:
                    break
            elif(_move.endCol,_move.endRow) != (c-1,r+1):
                if (board[_move.endCol][_move.endRow]) == "---":
                    appendMoves(moves, _move)
                if (board[_move.endCol][_move.endRow][0]) == enemyColor:
                    appendMoves(moves, _move)
                    break
    for i in range(1,10):
        if(c+i <= 9 and r+i <= 10):
            if(board[c+i][r+i][0] == allyColor):
                break
            if (board[c+1][r+1][0]) == enemyColor:
                break
            _move = Move((c,r),(c+i,r+i),board)
            if(_move.endCol,_move.endRow) == (c+1,r+1):
                if(board[c+1][r+1] == "---"):
                    pass
                else:
                    break
            elif(_move.endCol,_move.endRow) != (c+1,r+1):
                if (board[_move.endCol][_move.endRow]) == "---":
                    appendMoves(moves, _move)
                if (board[_move.endCol][_move.endRow][0]) == enemyColor:
                    appendMoves(moves, _move)
                    break
    for i in range(1,10):
        if(c+i <= 9 and r-i >= 0):
            if(board[c+i][r-i][0] == allyColor):
                break
            if (board[c+1][r-1][0]) == enemyColor:
                break
            _move = Move((c,r),(c+i,r-i),board)
            if(_move.endCol,_move.endRow) == (c-1,r-1):
                if(board[c+1][r-1] == "---"):
                    pass
                else:
                    break
            elif(_move.endCol,_move.endRow) != (c+1,r-1):
                if (board[_move.endCol][_move.endRow]) == "---":
                    appendMoves(moves, _move)
                if (board[_move.endCol][_move.endRow][0]) == enemyColor:
                    appendMoves(moves, _move)
                    break
 
def getGiraffeMoves(r,c,moves):
    global whiteToMove
    #tracking for spaces is very important because the giraffe will be blocked by other pieces
    #this is handled by a universal giraffe function
    calculateGiraffePaths(c,r,c-1,r-1,(-1),(0),  moves)
    calculateGiraffePaths(c,r,c-1,r-1,(0),(-1),  moves)
    calculateGiraffePaths(c,r,c+1,r-1,(1),(0),  moves)
    calculateGiraffePaths(c,r,c+1,r-1,(0),(-1),  moves)
    calculateGiraffePaths(c,r,c-1,r+1,(-1),(0),  moves)
    calculateGiraffePaths(c,r,c-1,r+1,(0),(1),  moves)
    calculateGiraffePaths(c,r,c+1,r+1,(1),(0),  moves)
    calculateGiraffePaths(c,r,c+1,r+1,(0),(1),  moves)

def calculateGiraffePaths(c,r,startc,startr,cmod,rmod,moves):
    global whiteToMove
    allyColor = "w"
    enemyColor = "b"
    if not whiteToMove:
        enemyColor = "w"
        allyColor = "b"
    newc = startc
    newr = startr
    ticker = 1
    for i in range(10):
        if(newc >=0 and newc <= 9 and newr >= 0 and newr <= 10):
            if(ticker < 3):
                if(board[newc][newr] == "---"):
                    ticker=ticker+1
                if(board[newc][newr][0] == allyColor):
                    break
                if(board[newc][newr][0] == enemyColor):
                    break
            elif(newc >=0 and newc <= 9 and newr >= 0 and newr <= 10):
                _move = Move((c,r),(newc,newr),board)
                if(board[newc][newr] == "---"):
                    appendMoves(moves,_move)
                if(board[newc][newr][0] == enemyColor):
                    appendMoves(moves,_move)  
                    break 
                if(board[newc][newr][0] == allyColor):
                    break
            
        else:break
        newc=newc+cmod
        newr=newr+rmod

def checkPromotion():
    global whiteToMove, whiteRoyalty, blackRoyalty, pawnXB, pawnXW
    for i in range(len(board[0])):
        if board[0][i]== "wpR":
            board[0][i] = "wRk"
        if board[0][i]== "wpA":
            board[0][i] = "wAd"
        if board[0][i]== "wpV":
            board[0][i] = "wVi"
        if board[0][i]== "wpG":
            board[0][i] = "wGi"
        if board[0][i]== "wpM":
            board[0][i] = "wMo"
        if board[0][i]== "wpT":
            board[0][i] = "wTa"
        if board[0][i]== "wpE":
            board[0][i] = "wEl"
        if board[0][i]== "wpW":
            board[0][i] = "wWe"
        if board[0][i]== "wpC":
            board[0][i] = "wCa"
        if board[0][i]== "wp0":
            board[0][i] = "---"
            board[0][0] = "wpx"
            pawnXW = True
        if board[0][i]== "wp1":
            board[0][i] = "wK0"
            whiteRoyalty += 1
        if board[0][i]== "wpK":
            board[0][i] = "wK1"
            whiteRoyalty += 1
    for i in range(len(board[9])):
        if board[9][i]== "bpR":
            board[9][i] = "bRk"
        if board[9][i]== "bpA":
            board[9][i] = "bAd"
        if board[9][i]== "bpV":
            board[9][i] = "bVi"
        if board[9][i]== "bpG":
            board[9][i] = "bGi"
        if board[9][i]== "bpM":
            board[9][i] = "bMo"
        if board[9][i]== "bpT":
            board[9][i] = "bTa"
        if board[9][i]== "bpE":
            board[9][i] = "bEl"
        if board[9][i]== "bpW":
            board[9][i] = "bWe"
        if board[9][i]== "bpC":
            board[9][i] = "bCa"
        if board[9][i]== "bp0":
            board[9][i] = "---"
            board[9][10] = "bpx"
            pawnXB = True
        if board[9][i]== "bp1":
            board[9][i] = "bK0"
            blackRoyalty += 1
        if board[9][i]== "bpK":
            board[9][i] = "bK1"
            blackRoyalty += 1

def checkPawnForks():
    global whiteToMove, pawnXW, pawnXB
    running = True
    if whiteToMove:
        for c in range(len(board)) :
            for r in range((len(board[c]))):
                if r+2 <= 10 and board[c][r][0] == "b" and board[c][r+2][0] == "b" and board[0][0] == "wpx" and running: 
                    if(c+1 <= 9 and board[c+1][r+1][1] != "K"):
                        board[0][0] = "---"
                        board[c+1][r+1] = "wp1"
                        running = False
    else:
        for c in range(len(board)):
            for r in range((len(board[c]))):
                if r+2 <= 10 and board[c][r][0] == "w" and board[c][r+2][0] == "w" and board[9][10] == "bpx" and running: 
                    if(c-1 > 0 and board[c-1][r+1][1] != "K"):
                        board[9][10] = "---"
                        board[c-1][r+1] = "bp1"
                        running = False

def appendMoves(_moves, _move):
    global whiteRoyalty, blackRoyalty
    if board[_move.endCol][_move.endRow] != "wpx" and board[_move.endCol][_move.endRow] != "bpx":
        _moves.append([(_move.startCol,_move.startRow),(_move.endCol,_move.endRow)])
"""
highlight selected and show available moves
"""
def highlightSquares(screen, validMoves, sqSelected):
    global whiteToMove
    if sqSelected != ():
        r,c = sqSelected
        if board[r][c][0] == ('w' if whiteToMove else "b"):
            s = p.Surface((SQ_SIZE,SQ_SIZE))
            s.set_alpha(150)
            s.fill(p.Color("blue"))
            screen.blit(s, ((c+1)*SQ_SIZE, (r+1)*SQ_SIZE))
            #highlight movesS
            s.fill(p.Color("yellow"))
            for move in validMoves:
                if move[0][0] == r and move[0][1] == c:
                    screen.blit(s, (SQ_SIZE*(move[1][1]+1),SQ_SIZE *(move[1][0]+1)))
"""
Responsible for all graphics
"""
def write(text,screen,color,pos,size):
    font=p.font.Font(None,size)
    screen.blit(font.render(text,True,color),pos)

def drawGameState(screen, validMoves, sqSelected):
    global whiteToMove, green
    b = p.Surface((SQ_SIZE*3,SQ_SIZE-20))
    bg = p.transform.scale(p.image.load("images/bg.png"), (WIDTH, HEIGHT))
    screen.blit(bg, (0,0))
    if(canDraw(whiteToMove) == True):
        b.fill((250,200,150))
        screen.blit(b, (10,10))
        #p.draw.rect(screen,(250,200,150),[10,10,SQ_SIZE*3,SQ_SIZE-20])
        write("Call Draw", screen, (0,0,0),(15,17),70)
    drawBoard(screen)
    highlightSquares(screen, validMoves, sqSelected)
    if(isKingInCheck()):
        if whiteToMove: kloc = whiteKingLocation
        else: kloc = blackKingLocation
        s = p.Surface((SQ_SIZE,SQ_SIZE))
        s.set_alpha(200)
        s.fill(p.Color(	(220,20,60)))
        screen.blit(s, ((kloc[1]+1)*SQ_SIZE, (kloc[0]+1)*SQ_SIZE))
    drawPieces(screen)
    if winner == "w" or winner == "b":
        write("Checkmate", screen, green,(225,425),150)
    if winner == "d":
        write("Draw", screen, green,(350,415),200)
    p.display.flip()
"""
Draw squares
"""
def drawBoard(screen):
    global white, black

    a = [1,3,5,7,9,11]
    aa = [1,3,5,7,9]

    b = [2,4,6,8,10]
    bb = [2,4,6,8,10,12]
    
    for r in a:
        for c in aa:
            p.draw.rect(screen, white, p.Rect(r*SQ_SIZE, c*SQ_SIZE, SQ_SIZE, SQ_SIZE))

    for r in b:
        for c in b:
            p.draw.rect(screen, white, p.Rect(r*SQ_SIZE, c*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            
    for r in aa:
        for c in aa:
            p.draw.rect(screen, black, p.Rect((r+1)*SQ_SIZE, c*SQ_SIZE, SQ_SIZE, SQ_SIZE))

        for r in bb:
            for c in b:
                p.draw.rect(screen, black, p.Rect((r-1)*SQ_SIZE, (c)*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            
    #fortresses
    p.draw.rect(screen, white, p.Rect(0*SQ_SIZE, 2*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    p.draw.rect(screen, black, p.Rect(12*SQ_SIZE, 9*SQ_SIZE, SQ_SIZE, SQ_SIZE))             
"""
Draw pieces
"""
def drawPieces(screen):
    for r in range(len(board)):
        for c in range(len(board[r])):
            piece = board[r][c]
            if piece != "---":
                screen.blit(IMAGES[piece], p.Rect((c+1)*SQ_SIZE, (r+1)*SQ_SIZE, SQ_SIZE, SQ_SIZE))
"""
animations
"""
def animateMove(move, screen, clock):
    colors =(p.Color(white),p.Color(black))
    dr = move.endRow - move.startRow
    dc = move.endCol - move.startCol
    framesPerSquare = 10
    frameCount = (abs(dr) + abs(dc)) + framesPerSquare
    for frame in range(frameCount + 1):
        r,c = (move.startRow + dr*frame/frameCount, move.startCol + dc*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen)
        #erase the piece
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect((move.endRow+1)*SQ_SIZE,(move.endCol+1)*SQ_SIZE, SQ_SIZE,SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        #draw captured piece onto rect
        if move.pieceCaptured != "---":
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        #draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect((r+1)*SQ_SIZE,(c+1)*SQ_SIZE,SQ_SIZE,SQ_SIZE))
        p.display.flip()
        clock.tick(60)


"""
This is the Tamerlane Chess bot
"""

import random

pieceValues = {
"K": 3.5,
"p": 1,
"M": 3,
"C": 2,
"G": 4,
"R": 5,
"T": 2.5,
"E": 1.5,
"W": 2,
"V": 1.5,
"A": 1.5,
}

CHECKMATE = 1000
DRAW = 0

def findRandomMove():
    if(len(validMoves) > 0):
        return random.choice(validMoves)

def findGreedyMove():
    global whiteToMove, moveLog
    turnMultiplier = 1 if whiteToMove else -1
    startingBoard = turnMultiplier * scoreMaterial()
    potentialBoardScore = startingBoard
    bestMove = None
    for i in range(len(validMoves)):
        #makes move
        _move = Move([validMoves[i][0][0],validMoves[i][0][1]],[validMoves[i][1][0],validMoves[i][1][1]],board)   
        makeMove(_move)
        moveLog.append(_move)
        #grabs valid enemy moves
        whiteToMove = not whiteToMove
        oppMoves = getValidMoves()
        whiteToMove = not whiteToMove
        #checks the score
        newScore = turnMultiplier * scoreMaterial()
        if newScore > potentialBoardScore:
            potentialBoardScore = newScore
            bestMove = validMoves[i]
        #checks for checkmate
        if len(oppMoves) == 0:
            potentialBoardScore = CHECKMATE
            bestMove = validMoves[i]
        undoMove()
    if potentialBoardScore > startingBoard:
        return bestMove
    else:
        return findRandomMove()
            
def findGreedyMoveScore():
    global whiteToMove, moveLog
    turnMultiplier = 1 if whiteToMove else -1
    startingBoard = turnMultiplier * scoreMaterial()
    potentialBoardScore = startingBoard
    bestMove = None
    for i in range(len(validMoves)):
        #makes move
        _move = Move([validMoves[i][0][0],validMoves[i][0][1]],[validMoves[i][1][0],validMoves[i][1][1]],board)   
        makeMove(_move)
        moveLog.append(_move)
        #grabs valid enemy moves
        whiteToMove = not whiteToMove
        oppMoves = getValidMoves()
        whiteToMove = not whiteToMove
        #checks the score
        newScore = turnMultiplier * scoreMaterial()
        if newScore > potentialBoardScore:
            potentialBoardScore = newScore
            bestMove = validMoves[i]
        #checks for checkmate
        if len(oppMoves) == 0:
            potentialBoardScore = CHECKMATE
            bestMove = validMoves[i]
        undoMove()
    return potentialBoardScore
            
def findMinMax1():
    global whiteToMove, moveLog
    turnMultiplier = 1 if whiteToMove else -1
    startingBoard = scoreMaterial()
    print(startingBoard)
    enemyMinMax = CHECKMATE
    loops = 0
    bestMove = None
    for i in range(len(validMoves)):
        #makes move
        _move = Move([validMoves[i][0][0],validMoves[i][0][1]],[validMoves[i][1][0],validMoves[i][1][1]],board)   
        makeMove(_move)
        moveLog.append(_move)
        #grabs valid enemy moves
        whiteToMove = not whiteToMove
        oppMoves = getValidMoves()
        whiteToMove = not whiteToMove
        #checks for checkmate
        if len(oppMoves) == 0:
            enemyMinMax = -CHECKMATE
            bestMove = validMoves[i]
        #if no checkmate available, try enemy responses
        else:
            highestLocal = startingBoard
            #checks the score for the worst possible enemy response
            for j in range(len(oppMoves)): 
                #make enemy response
                _move = Move([oppMoves[j][0][0],oppMoves[j][0][1]],[oppMoves[j][1][0],oppMoves[j][1][1]],board)   
                makeMove(_move)
                moveLog.append(_move)
                #checks if their response will leave us in checkmate
                whiteToMove = not whiteToMove
                _oppMoves = getValidMoves()
                if len(_oppMoves) == 0:
                    highestLocal = CHECKMATE
                #grabs board score
                newScore = (-turnMultiplier) * scoreMaterial()
                #if board score is 
                print(newScore)
                if newScore < highestLocal:
                    highestLocal = newScore
                whiteToMove = not whiteToMove
                undoMove()
        #if the best enemy response is WORSE than enemyMinMax (default as 
        #current board state) then mark this as the best move
        if(highestLocal < enemyMinMax):
            enemyMinMax = highestLocal
            bestMove = validMoves[i]
        undoMove()
    print(startingBoard,enemyMinMax)
    return bestMove
            
def findMinMax(depth, alpha, beta, maximizingPlayer):
    global validMoves, board, whiteToMove
    if depth == 0 or len(getValidMoves()) == 0:
        return scoreMaterial()

    if maximizingPlayer:
        bestValue = -float('inf')
        for move in getValidMoves():
            _move = Move([move[0][0],move[0][1]],[move[1][0],move[1][1]],board)   
            makeMove(_move)
            moveLog.append(_move)
            whiteToMove = not whiteToMove
            value = findMinMax(depth - 1, alpha, beta, not maximizingPlayer)
            bestValue = max(bestValue, value)
            alpha = max(alpha, bestValue)
            undoMove()
            whiteToMove = not whiteToMove
            if beta <= alpha:
                break
        return bestValue
    else:
        bestValue = float('inf')
        for move in getValidMoves():
            _move = Move([move[0][0],move[0][1]],[move[1][0],move[1][1]],board)   
            makeMove(_move)
            moveLog.append(_move)
            whiteToMove = not whiteToMove
            value = findMinMax(depth - 1, alpha, beta, not maximizingPlayer)
            bestValue = min(bestValue, value)
            beta = min(beta, bestValue)
            undoMove()
            whiteToMove = not whiteToMove
            if beta <= alpha:
                break
        return bestValue

def getBestMove(depth, maximizingPlayer):
    global validMoves, board
    bestValue = -float('inf')
    bestMove = None
    for move in getValidMoves():
        _move = Move([move[0][0],move[0][1]],[move[1][0],move[1][1]],board)   
        makeMove(_move)
        moveLog.append(_move)
        value = findMinMax(depth - 1, -float('inf'), float('inf'), maximizingPlayer)
        if value > bestValue:
            bestValue = value
            bestMove = move
        undoMove()
    return bestMove
        
def scoreMaterial():
    score = 0
    for c in range(len(board)):
        for r in range(len(board[c])):
            if board[c][r][0] == "w":
                score += pieceValues[board[c][r][1]]
            if board[c][r][0] == "b":
                score -= pieceValues[board[c][r][1]] 
    return score



if __name__ == "__main__":
    main()