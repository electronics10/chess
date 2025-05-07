"""CONVENTIONS:
positions are done row-column from the bottom left and are both numbers. This corresponds to the alpha-number system in traditional chess while being computationally useful. they are specified as tuples
"""
import itertools
WHITE = "white"
BLACK = "black"







class GameRule:
    #ive decided since the number of pieces is capped but the type of pieces is not (pawn transformations), I've already coded much of the modularity to support just using a dictionary of pieces
    def __init__(self):
        self.steps = {}
        self.rounds = [0,0]
        self.eaten = {}
        self.castling_dict = {}
        self.playersturn = WHITE
        self.message = ""#"this is where prompts will go"
        self.gameboard = {}
        self.placePieces()
        print("hi")
        #self.main()
        
    def placePieces(self):

        for i in range(0,8):
            self.gameboard[(i,1)] = Pawn(WHITE,uniDict[WHITE][Pawn],1)
            self.gameboard[(i,6)] = Pawn(BLACK,uniDict[BLACK][Pawn],-1)
            
        placers = (Rook,Knight,Bishop,Queen,King,Bishop,Knight,Rook)
        
        for i in range(0,8):
            self.gameboard[(i,0)] = placers[i](WHITE,uniDict[WHITE][placers[i]])
            self.gameboard[(i,7)] = placers[i](BLACK,uniDict[BLACK][placers[i]])


        
    def main(self):
        
        #while True:
        #self.printBoard()
        print(self.message)#print message
        self.message = ""
        print("rounds",self.rounds,"steps",self.steps,"eaten",self.eaten)
        if sum(self.rounds) == 0 and (tuple(self.rounds) not in self.steps): startpos,endpos = self.parseInput() #very first step
        else:
            command = input("previous step? p for yes;any other keys to continue the game\n")#choose to parse or retract
            if command == "p":
                self.previous_step()
            else:
                print("this is where prompts will go")
                startpos,endpos = self.parseInput()
        try:#finding target piece
            target = self.gameboard[startpos]
        except:
            self.message = "could not find piece; index probably out of range"
            target = None
                
        if target:
            print("found "+str(target))
            if target.Color != self.playersturn:
                self.message = "you aren't allowed to move that piece this turn"
                #continue
            #if isinstance(self.gameboard[endpos], King) and (endpos[0] in (2,6)):#raise castling
                #self.gameboard[endpos].castling(endpos[0], endpos[1], self.gameboard, self.gameboard[endpos].Color)
            #if isinstance(self.gameboard[endpos], Pawn) and (endpos[0] in (2,6)):#raise enpassant
                #self.gameboard[endpos].castling(endpos[0], endpos[1], self.gameboard, self.gameboard[endpos].Color)
            if target.isValid(startpos,endpos,target.Color,self.gameboard):#checking if is valid move under regular rules 
                self.rounds[0] += self.rounds[1]#recording
                if self.rounds[1] != 0:
                    self.rounds[1] = 0
                else:
                    self.rounds[1] = 1
                if tuple(self.rounds) not in self.steps:
                    self.steps[tuple(self.rounds)] = (chr(startpos[0]+97)+str(startpos[1]+1),chr(endpos[0]+97)+str(endpos[1]+1),target)
                else:
                    self.rounds[1] += 1
                    self.steps[tuple(self.rounds)] =(chr(startpos[0]+97)+str(startpos[1]+1),chr(endpos[0]+97)+str(endpos[1]+1),target)
                self.message = "that is a valid move"
                if endpos in self.gameboard:#eaten
                    self.eaten[tuple(self.rounds)] = (endpos,self.gameboard[endpos])
                self.gameboard[endpos] = self.gameboard[startpos]#move chess
                del self.gameboard[startpos]
                if isinstance(self.gameboard[endpos], Pawn) and (endpos[1] in (0,7)):#raise promotion
                    self.gameboard[endpos].promotion(endpos[0], endpos[1], self.gameboard, self.gameboard[endpos].Color)
                try:
                    self.isCheck()#check or checkmate
                except:
                    print("checkmate")
                    #break
                stalemate, not_enough_piece = self.draw() #check draw
                if stalemate or  not_enough_piece: 
                    if not_enough_piece:
                        print("draw")
                    else:
                        print("stalemate")
                    #break
                else: pass#continue
                if self.playersturn == WHITE:#change turn
                    self.playersturn = BLACK
                else : self.playersturn = WHITE
            else :
                self.message = "invalid move" + str(target.availableMoves(startpos[0],startpos[1],self.gameboard))
                print(target.availableMoves(startpos[0],startpos[1],self.gameboard))
        else : self.message = "there is no piece in that space"



    def draw(self):  #lack: 1.draw agreement  2.50 consecutive rules  3.threefold repitition
        stalemate, not_enough_piece = False, False
        count, whitepiece, blackpiece = 1, 0, 0
        if len(self.gameboard) == 4: #both sides with a king and a knight or bishop
            for piece in self.gameboard.values():
                piece = str(piece)
                if piece in "♘♗♞♝":
                    count += 1
                elif piece in "♔♚":
                    count *= 1
                else:
                    count -= 10 #not important
        if count == 2: not_enough_piece = True 
        if len(self.gameboard) <= 18:#stalemate 18 = 16(oneside at most) + 2(king+any other)
            for piece in self.gameboard.values():
                if str(piece) in "♙♖♘♗♕":
                    whitepiece += 1
                if str(piece) in "♟♜♞♝♛":
                    blackpiece += 1
        if not (whitepiece or blackpiece): stalemate = False #when both side got no pieces other than king         
        elif not (whitepiece and blackpiece): stalemate = True #aside from king, either one side has no piece left
        return stalemate, not_enough_piece

        
    def isCheck(self):
        #ascertain where the kings are, check all pieces of opposing color against those kings, then if either get hit, check if its checkmate
        king = King
        kingDict = {}
        pieceDict = {BLACK : [], WHITE : []}
        for position,piece in self.gameboard.items():
            if type(piece) == King:
                kingDict[piece.Color] = position
            #print(piece)
            pieceDict[piece.Color].append((piece,position))
        #white
        if self.canSeeKing(kingDict[WHITE],pieceDict[BLACK]):
            self.message = "White player is in check"
            return WHITE
        if self.canSeeKing(kingDict[BLACK],pieceDict[WHITE]):
            self.message = "Black player is in check"
            return BLACK
        
    def canSeeKing(self,kingpos,piecelist):
        #checks if any pieces in piece list (which is an array of (piece,position) tuples) can see the king in kingpos
        for piece,position in piecelist:
            if piece.isValid(position,kingpos,piece.Color,self.gameboard):
                return True

    def previous_step(self):
        if self.rounds[1] == 1:#reverse recording
            self.rounds[1] -= 1
            self.playersturn = WHITE
        else: #rounds[1] == 0
            self.rounds[0] -= 1
            self.rounds[1] = 1
            self.playersturn = BLACK
            if self.rounds[0] == -1: self.rounds[0] = 0     
        castling_case = None
        retraction = self.steps.popitem()
        presentpos = ((ord(retraction[1][1][0])-97), int(retraction[1][1][1])-1)
        previouspos = ((ord(retraction[1][0][0])-97), int(retraction[1][0][1])-1)
        enpos = None
        #print( presentpos, "back to", previouspos)

        if tuple(retraction[0]) in self.castling_dict:#castling case
            self.gameboard[presentpos].moved = False
            self.gameboard[previouspos] = self.gameboard[presentpos]
            del self.gameboard[presentpos]
            castling_case = self.castling_dict.popitem()
            self.gameboard[castling_case[1][0]] = castling_case[1][1]
            self.gameboard[castling_case[1][0]].moved = False
            if presentpos[0] == 2: del self.gameboard[(presentpos[0]+1,presentpos[1])]
            elif presentpos[0] == 6: del self.gameboard[(presentpos[0]-1,presentpos[1])]
        elif tuple(retraction[0]) in self.eaten:
            self.gameboard[previouspos] = self.gameboard[presentpos]
            try:
                for tup in self.steps.values():
                    if tup[2] == self.gameboard[previouspos]:break
                else: self.gameboard[previouspos].moved = False
            except:
                pass
            try:
                if self.eaten[tuple(retraction[0])][1].en_passanted == True:#enpassant case
                    enpos = ((presentpos[0]), (presentpos[1]+self.eaten[tuple(retraction[0])][1].direction))
                    self.gameboard[enpos] = self.eaten.popitem()[1][1]
                    del self.gameboard[presentpos]
                else:#regular pawn eaten
                    self.gameboard[presentpos] = self.eaten.popitem()[1][1]
            except:#regular eaten(not pawn)
                self.gameboard[presentpos] = self.eaten.popitem()[1][1]
                
        else:#regular case
            self.gameboard[previouspos] = self.gameboard[presentpos]
            try:
                for tup in self.steps.values():
                    if tup[2] == self.gameboard[previouspos]:break
                else: self.gameboard[previouspos].moved = False
            except:
                pass
            del self.gameboard[presentpos]
            
           
            
        #self.main()


    def parseInput(self):
        try:
            a,b = input().split()
            a = ((ord(a[0])-97), int(a[1])-1)
            b = (ord(b[0])-97, int(b[1])-1)
            print(a,b)
            return (a,b)
        except:
            print("error decoding input. please try again")
            return((-1,-1),(-1,-1))
    
    """def validateInput(self, *kargs):
        for arg in kargs:
            if type(arg[0]) is not type(1) or type(arg[1]) is not type(1):
                return False
        return True"""
        

    """def printBoard(self):
        print("  1   | 2   | 3   | 4   | 5   | 6   | 7   | 8   |")
        for i in range(0,8):
            print("-"*47)
            print(chr(i+97),end=" |")
            for j in range(0,8):
                item = self.gameboard.get((i,j)," ")
                print(str(item)+'  |', end = " ")
            print()
        print("-"*47)
    """
            
           
        
    """game class. contains the following members and methods:
    two arrays of pieces for each player
    8x8 piece array with references to these pieces
    a parse function, which turns the input from the user into a list of two tuples denoting start and end points
    a checkmateExists function which checks if either players are in checkmate
    a checkExists function which checks if either players are in check (woah, I just got that nonsequitur)
    a main loop, which takes input, runs it through the parser, asks the piece if the move is valid, and moves the piece if it is. if the move conflicts with another piece, that piece is removed. ischeck(mate) is run, and if there is a checkmate, the game prints a message as to who wins
    """

class Piece:
    
    def __init__(self,color,name):
        self.name = name
        self.Color = color
        self.moved = False
    def isValid(self,startpos,endpos,Color,gameboard):
        if endpos in self.availableMoves(startpos[0],startpos[1],gameboard, Color = Color):
            return True
        return False
    def __repr__(self):
        return self.name
    
    def __str__(self):
        return self.name
    
    def availableMoves(self,x,y,gameboard):
        print("ERROR: no movement for base class")
        
    def AdNauseum(self,x,y,gameboard, Color, intervals):
        """repeats the given interval until another piece is run into. 
        if that piece is not of the same color, that square is added and
         then the list is returned"""
        answers = []
        for xint,yint in intervals:
            xtemp,ytemp = x+xint,y+yint
            while self.isInBounds(xtemp,ytemp):
                #print(str((xtemp,ytemp))+"is in bounds")
                
                target = gameboard.get((xtemp,ytemp),None)
                if target is None: answers.append((xtemp,ytemp))
                elif target.Color != Color: 
                    answers.append((xtemp,ytemp))
                    break
                else:
                    break
                
                xtemp,ytemp = xtemp + xint,ytemp + yint
        return answers
                
    def isInBounds(self,x,y):
        "checks if a position is on the board"
        if x >= 0 and x < 8 and y >= 0 and y < 8:
            return True
        return False
    
    def noConflict(self,gameboard,initialColor,x,y):
        "checks if a single position poses no conflict to the rules of chess"
        if self.isInBounds(x,y) and (((x,y) not in gameboard) or gameboard[(x,y)].Color != initialColor) : return True
        return False
        
        
chessCardinals = [(1,0),(0,1),(-1,0),(0,-1)]
chessDiagonals = [(1,1),(-1,1),(1,-1),(-1,-1)]

def knightList(x,y,int1,int2):
    """sepcifically for the rook, permutes the values needed around a position for noConflict tests"""
    return [(x+int1,y+int2),(x-int1,y+int2),(x+int1,y-int2),(x-int1,y-int2),(x+int2,y+int1),(x-int2,y+int1),(x+int2,y-int1),(x-int2,y-int1)]
def kingList(x,y):
    return [(x+1,y),(x+1,y+1),(x+1,y-1),(x,y+1),(x,y-1),(x-1,y),(x-1,y+1),(x-1,y-1)]



class Knight(Piece):
    def availableMoves(self,x,y,gameboard, Color = None):
        if Color is None : Color = self.Color
        return [(xx,yy) for xx,yy in knightList(x,y,2,1) if self.noConflict(gameboard, Color, xx, yy)]
        
class Rook(Piece):
    def availableMoves(self,x,y,gameboard ,Color = None):
        if Color is None : Color = self.Color
        return self.AdNauseum(x, y, gameboard, Color, chessCardinals)
        
class Bishop(Piece):
    def availableMoves(self,x,y,gameboard, Color = None):
        if Color is None : Color = self.Color
        return self.AdNauseum(x, y, gameboard, Color, chessDiagonals)
        
class Queen(Piece):
    def availableMoves(self,x,y,gameboard, Color = None):
        if Color is None : Color = self.Color
        return self.AdNauseum(x, y, gameboard, Color, chessCardinals+chessDiagonals)
        
class King(Piece):
    def availableMoves(self,x,y,gameboard, Color = None):
        if Color is None : Color = self.Color
        return  [(xx,yy) for xx,yy in kingList(x,y) if self.noConflict(gameboard, Color, xx, yy)]
    #def castling(self,x,y,gameboard,color):



class Pawn(Piece):
    def __init__(self,color,name,direction):
        self.name = name
        self.Color = color
        #of course, the smallest piece is the hardest to code. direction should be either 1 or -1, should be -1 if the pawn is traveling "backwards"
        self.direction = direction
        self.en_passantable ={}
        self.en_passanted = False

    def availableMoves(self,x,y,gameboard, Color = None):
        if Color is None : Color = self.Color
        answers = []
        if (x+1,y+self.direction) in gameboard and self.noConflict(gameboard, Color, x+1, y+self.direction) : #capture
            answers.append((x+1,y+self.direction))
        if (x-1,y+self.direction) in gameboard and self.noConflict(gameboard, Color, x-1, y+self.direction) : #capture
            answers.append((x-1,y+self.direction))
        if (x,y+self.direction) not in gameboard and self.isInBounds(x,y+self.direction) and Color == self.Color : 
            answers.append((x,y+self.direction))# the condition after the and is to make sure the non-capturing movement (the only fucking one in the game) is not used in the calculation of checkmate
        if (x,y+2*self.direction) not in gameboard and self.isInBounds(x,y+2*self.direction) and Color == self.Color: # two-steps move
            if Color == WHITE and y == 1: 
                answers.append((x,y+2*self.direction))
            if Color == BLACK and y == 6: 
                answers.append((x,y+2*self.direction))
            else:pass

        return answers



    def promotion(self,x,y,gameboard,color):
        if color == WHITE and y == 7:
            promDict = {"Rook":Rook, "Knight":Knight, "Bishop":Bishop, "Queen":Queen}
            while True:
                promote_as = input("white promotion:choose Rook, Knight, Bishop or Queen\n")
                if promote_as in promDict:
                    gameboard[(x,y)] =  promDict[promote_as](WHITE,uniDict[WHITE][promDict[promote_as]])
                    return None
                else: "invalid input"

        if color == BLACK and y == 0:
            promDict = {"Rook":Rook, "Knight":Knight, "Bishop":Bishop, "Queen":Queen}
            while True:
                promote_as = input("black promotion:choose Rook, Knight, Bishop or Queen\n")
                if promote_as in promDict:
                    gameboard[(x,y)] =  promDict[promote_as](BLACK,uniDict[BLACK][promDict[promote_as]]) 
                    return None
                else: "invalid input"

        

uniDict = {WHITE : {Pawn : "♙", Rook : "♖", Knight : "♘", Bishop : "♗", King : "♔", Queen : "♕" }, BLACK : {Pawn : "♟", Rook : "♜", Knight : "♞", Bishop : "♝", King : "♚", Queen : "♛" }}


        

