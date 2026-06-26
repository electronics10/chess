from tkinter import*
from  chess_project import*
import copy
game1 = GameRule()
TOP = "1.0"
class chessGame(Frame):
    def __init__(self, master = None, game_rule = None):
        Frame.__init__(self, master)
        self.master = master
        self.game = game_rule#like inheretance, but can't cause' board initialize means(64 buttons)
        #//////////////////
        self.retractButton = None
        self.quitButton = None
        self.newgameButton = None
        self.showAvailableButton = None
        self.SAM = False
        self.turnboard = None
        self.turn_times = 0
        self.myEntry = None
        self.instruction = None
        self.submitButton = None
        self.output = None
        self.moveindex = 0#check grid buttons parsing(startpos or endpos)
        self.startpos = None
        self.endpos = None     
        self.boardButtons = [[] for i in range(8)]#grid buttons blanked
        #self.game.placePieces()#place piece in gameboardDict
        #self.game.playersturn = WHITE#firstplayer's turn
        self.init_board()#initialize board:grid buttons assigned piece-str and get in right place in window 
        #default setings done
        self.gen_window()#generate interface
    
    def gen_window(self):        
        self.config(bg="black")
        self.master.title("Chessgame")
        self.pack(fill = BOTH, expand = 1)                       
        self.retractButton = Button(self, text="retract", width=5, height=1, bg="white", fg="red", font="none 16 bold",command=self.retract)
        self.retractButton.grid(row=7, column=8, sticky=E)
        self.quitButton = Button(self, text="Quit", width=5, height=1, bg="white", fg="black", font="none 16 bold",command=self.close_window)
        self.quitButton.grid(row=7, column=9, sticky=E)        
        self.newgameButton = Button(self, text="New", width=5, height=1, bg="white", fg="green", font="none 16 bold", command=self.newgame)
        self.newgameButton.grid(row=7, column=10, sticky=E)
        self.showAvailableButton = Button(self, text="SAM", width=5, height=1, bg="white", fg="brown", font="none 16 bold", command=self.show_available)
        self.showAvailableButton.grid(row=6, column=8, sticky=E)
        self.turnboard = Button(self, text="T90°", width=5, height=1, bg="white", fg="blue", font="none 16 bold", command=self.turn_board)
        self.turnboard.grid(row=6, column=9, sticky=E)
        self.myEntry = Entry(self, width=30,)
        self.myEntry.place(x=810, y=550)
        self.instruction = Label(self, width=30, height=2, text="Welcome")
        self.instruction.place(x=810, y=510)
        self.submitButton = Button(self, text="submit", width=5, height=1, bg="white", fg="black", font="none 16 bold", command=self.submit)
        self.submitButton.grid(row=6, column=10, sticky=E)
        self.output = Text(self,width=30, height=38, wrap=WORD, bg="gray" )
        self.output.place(x=810, y=10)


    def turn_board(self):
        self.turn_times += 1
        count = self.turn_times%4
        if count == 0:
            for row_ in range(8):
                for column_ in range(8):
                    self.boardButtons[row_][column_].grid(row=column_, column=row_, sticky=W)
        elif count == 1:
            for row_ in range(8):
                for column_ in range(8):
                    self.boardButtons[row_][column_].grid(row=7-row_, column=column_, sticky=W)
        elif count == 2:
            for row_ in range(8):
                for column_ in range(8):
                    self.boardButtons[row_][column_].grid(row=7-column_, column=7-row_, sticky=W)
        elif count == 3:
            for row_ in range(8):
                for column_ in range(8):
                    self.boardButtons[row_][column_].grid(row=row_, column=7-column_, sticky=W)
        
        
    def show_available(self):
        if self.moveindex != 1:
            if self.SAM == True: self.SAM = False
            else: self.SAM  = True

    def retract(self):
        if sum(self.game.rounds) == 0 and (tuple(self.game.rounds) not in self.game.steps): self.output.insert(TOP, "\nvery first step")
        elif self.moveindex == 1: pass
        else:
            self.game.previous_step()
            self.printpieces(self.game.gameboard)
            self.output.insert(TOP, "\nretracted")

    
    def close_window(self):
        self.destroy()
        self.master.destroy()


    def newgame(self):
        self.output.delete(0.0, TOP)
        self.game = None
        self.game = GameRule()        
        self.game.playersturn = WHITE
        self.game.gameboard.clear()
        self.retractButton = None
        self.quitButton = None
        self.newgameButton = None
        self.showAvailableButton = None
        self.SAM = False
        self.turnboard = None
        self.turn_times = 0
        self.myEntry = None
        self.instruction = None
        self.submitButton = None
        self.output = None
        self.moveindex = 0#check grid buttons parsing(startpos or endpos)
        self.startpos = None
        self.endpos = None     
        self.boardButtons = [[] for i in range(8)]#grid buttons blanked
        self.game.placePieces()#place piece in gameboardDict
        self.init_board()#initialize board:grid buttons assigned piece-str and get in right place in window
        #default setings done
        self.gen_window()


    def init_board(self):
        def dontfuncyet(name):
            return lambda : self.parseClick(name)
        color=""
        for row_ in range(8):
            for column_ in range(8):
                if (row_ + column_)%2 == 0: color="green"
                else: color="white"
                self.boardButtons[row_].append(Button(self, text=self.loadpieces((column_,row_)), bg=color, font="none 22 bold", width=5, height=2))
                self.boardButtons[row_][column_].grid(row=column_, column=row_, sticky=W)
                self.boardButtons[row_][column_].name= chr(column_+97)+str(row_+1)
                self.boardButtons[row_][column_]["command"] = dontfuncyet(self.boardButtons[row_][column_].name)

    def stop_board_function(self):
        for row_ in range(8):
            for column_ in range(8):
                self.boardButtons[row_][column_]["command"] = False
        self.retractButton["command"] = False

    def checkmate_display(self):
        print("checkmate")
        self.stop_board_function()

    def draw_display(self):
        print("draw")
        self.stop_board_function()

    def stalemate_display(self):
        print("stalemate")
        self.stop_board_function()

    def loadpieces(self,pos):
        if pos in self.game.gameboard: return self.game.gameboard[pos]
        else: return ""

    def printpieces(self, gameboard):
        for row_ in range(8):
            for column_ in range(8):
                self.boardButtons[row_][column_]["text"] = self.loadpieces((column_, row_))
        self.AvailableDisplay()#clear

    def AvailableDisplay(self):
        if self.SAM == True:
            if self.moveindex == 1:
                try:
                    available_moves = self.game.gameboard[self.startpos].availableMoves(self.startpos[0],self.startpos[1],self.game.gameboard )
                    for i in available_moves:
                        self.boardButtons[i[1]][i[0]]["bg"] = "yellow"
                except:
                    pass
            
            else:
                color=""
                for row_ in range(8):
                    for column_ in range(8):
                        if (row_ + column_)%2 == 0: color="green"
                        else: color="white"
                        self.boardButtons[row_][column_]["bg"] = color
        else: return None

    def submit(self):
        target = self.game.gameboard[self.endpos]
        if self.instruction["text"] == "Enter Queen,Rook,Knight or Bishop.":
            if self.myEntry.get() == "Queen":
                self.game.gameboard[self.endpos] = Queen(target.Color,uniDict[target.Color][Queen])
                self.instruction["text"] = "Welcome"
                self.init_board()
                self.printpieces(self.game.gameboard)
            elif self.myEntry.get() == "Rook":
                self.game.gameboard[self.endpos] = Rook(target.Color,uniDict[target.Color][Rook])
                self.instruction["text"] = "Welcome"
                self.init_board()
                self.printpieces(self.game.gameboard)
            elif self.myEntry.get() == "Knight":
                self.game.gameboard[self.endpos] = Knight(target.Color,uniDict[target.Color][Knight])
                self.instruction["text"] = "Welcome"
                self.init_board()
                self.printpieces(self.game.gameboard)
            elif self.myEntry.get() == "Bishop":
                self.game.gameboard[self.endpos] = Bishop(target.Color,uniDict[target.Color][Bishop])
                self.instruction["text"] = "Welcome"
                self.init_board()
                self.printpieces(self.game.gameboard)
            else:return None
        else:return None

    def choose_promotion(self):
        self.instruction["text"] = "Enter Queen,Rook,Knight or Bishop."
        self.stop_board_function()


    def parseClick(self, gridpos):
        self.moveindex += 1
        if self.moveindex == 1:
            self.startpos = ((ord(gridpos[0])-97), int(gridpos[1])-1)
            try:
                if self.game.gameboard[self.startpos].Color == self.game.playersturn: self.AvailableDisplay()
            except:pass
        elif self.moveindex == 2:
            self.endpos = ((ord(gridpos[0])-97), int(gridpos[1])-1)
            self.moveindex = 0
            self.parseGame(self.startpos, self.endpos)#run one round
        self.output.insert(TOP,"\n"+gridpos)

    def parseGame(self, startpos, endpos):
        rook_not_moved = False#castling condition
        no_pieces_between = None#castling condition
        count_castling_check = 0
        k_start_to_end = []#castling
        castling = False#if castling happenned in this round
        enpassant = False#if enpassant happenned in this round
        checkingpos = None#enpassant condition
        lastround = copy.deepcopy(self.game.rounds)#enpassant condition
        self.game.message = "" 
        try:#finding target piece
            target = self.game.gameboard[startpos]
        except:
            self.game.message = "could not find piece; index probably out of range"
            target = None
                
        if target:
            self.output.insert(TOP, "\nfound "+str(target))
            if target.Color != self.game.playersturn:
                self.output.insert(TOP, "\nyou aren't allowed to move that piece this turn")
                return None
            if isinstance(target, King):#raise castling
                if endpos[0] in (2,6):#want to proceed castling
                    if endpos[0] == 2:
                        try:
                            if self.game.gameboard[(0, endpos[1])].moved == False:#rook not moved 
                                rook_not_moved = True
                            else:rook_not_moved = False
                        except:
                            rook_not_moved = False
                        for x in range(1,4,1):#loop through between
                            no_pieces_between = True
                            try:
                                if self.game.gameboard[(x, endpos[1])] != None:
                                    no_pieces_between = False
                            except:
                                pass
                        for i in range(3):
                            k_start_to_end.append((endpos[0]+i, endpos[1]))
                    elif endpos[0] == 6:
                        try:
                            if self.game.gameboard[(7, endpos[1])].moved == False:#rook not moved 
                                rook_not_moved = True
                            else:rook_not_moved = False
                        except:
                            rook_not_moved = False
                        for x in range(5,7,1):#loop through between
                            no_pieces_between = True
                            try:
                                if self.game.gameboard[(x, endpos[1])] != None:
                                    no_pieces_between = False
                            except:
                                pass
                        for i in range(3):
                            k_start_to_end.append((endpos[0]-i, endpos[1]))
                    if (target.moved == False) and (rook_not_moved == True) and (no_pieces_between == True):
                        del self.game.gameboard[startpos]
                        for pos in k_start_to_end:#loop through check
                            try:
                                self.game.gameboard[pos] = target
                                if self.game.isCheck() == self.game.playersturn:#got check//////////////
                                    self.game.message = ""
                                    del self.game.gameboard[pos]
                                else:#no check yet
                                    count_castling_check += 1
                                    self.game.message = ""
                                    self.game.gameboard[startpos] = target
                            except:#checkmate problem
                                self.game.message = ""
                                del self.game.gameboard[pos]
                                break#checkmate between(because isCheck isn't well coded)
                        if count_castling_check == len(k_start_to_end):#castling!!
                            castling = True
                            if endpos[0] == 2:
                                self.game.gameboard[(endpos[0]+1,endpos[1])] = self.game.gameboard[(0,endpos[1])]
                                self.game.gameboard[(endpos[0]+1,endpos[1])].moved = True
                                self.game.castling_dict[tuple(self.game.rounds)] = ((0,endpos[1]), self.game.gameboard.pop((0,endpos[1])) )
                            elif endpos[0] == 6:
                                self.game.gameboard[(endpos[0]-1,endpos[1])] = self.game.gameboard[(7,endpos[1])]
                                self.game.gameboard[(endpos[0]-1,endpos[1])].moved = True
                                self.game.castling_dict[tuple(self.game.rounds)] = ((7,endpos[1]), self.game.gameboard.pop((7,endpos[1])) )
                        else:#can't do castling
                            k_start_to_end.clear()
                            pass
                    else:#can't do castling
                        k_start_to_end.clear()
                        pass
            elif isinstance(target, Pawn) and (startpos[1] in (3,4)):#raise enpassant
                checkingpos = (endpos[0], startpos[1])
                try:
                    if isinstance(self.game.gameboard[checkingpos], Pawn) and self.game.gameboard[checkingpos] != self.game.gameboard[startpos]:
                        if lastround[1] == 1: lastround[1]=0
                        else:
                            lastround[0]-=1
                            lastround[1]=1
                        if self.game.gameboard[(endpos[0], startpos[1])].en_passantable[tuple(lastround)] == True:
                            enpassant = True
                            self.game.gameboard[(endpos[0], startpos[1])].en_passanted = True
                except:
                    enpassant = False
            else:pass
            if target.isValid(startpos,endpos,target.Color,self.game.gameboard) or enpassant or castling:#checking if is valid move(special rules raised)
                target.moved = True
                if endpos in self.game.gameboard or enpassant == True:#eaten
                    if enpassant == False:
                        if isinstance(target, King):pass
                        else: self.game.eaten[tuple(self.game.rounds)] = (endpos,self.game.gameboard[endpos])
                    elif enpassant == True:
                        self.game.eaten[tuple(self.game.rounds)] = ((endpos[0], startpos[1]),self.game.gameboard[(endpos[0], startpos[1])])
                        del self.game.gameboard[(endpos[0], startpos[1])]                
                
                if tuple(self.game.rounds) not in self.game.steps:#recording
                    self.game.steps[tuple(self.game.rounds)] = (chr(startpos[0]+97)+str(startpos[1]+1),chr(endpos[0]+97)+str(endpos[1]+1),target)
                else:
                    self.game.rounds[1] += 1
                    self.game.steps[tuple(self.game.rounds)] =(chr(startpos[0]+97)+str(startpos[1]+1),chr(endpos[0]+97)+str(endpos[1]+1),target)
                self.game.message = "that is a valid move"                
                self.game.gameboard[endpos] = self.game.gameboard[startpos]#move chess
                del self.game.gameboard[startpos]
                if isinstance(self.game.gameboard[endpos], Pawn):#pawn special rules condition initialize
                    if abs(endpos[1] - startpos[1]) == 2:#see if pawn is en_passantable
                        target.en_passantable[tuple(self.game.rounds)] = True
                    if (endpos[1] in (0,7)):#raise promotion
                        #self.game.gameboard[endpos].promotion(endpos[0], endpos[1], self.game.gameboard, self.game.gameboard[endpos].Color)
                        self.endpos = endpos
                        self.choose_promotion()
                try:
                    self.game.isCheck()#check or checkmate
                except:
                    self.output.insert(TOP, "\ncheckmate!!!!!!")
                    self.checkmate_display()
                stalemate, not_enough_piece = self.game.draw() #check draw
                if stalemate or not_enough_piece: 
                    if not_enough_piece:
                        self.output.insert(TOP, "\ndraw!!!!!")
                        self.draw_display()
                    else:
                        self.output.insert(TOP, "\nstalemate!!!!!")
                        self.stalemate_display()
                else: pass
                if self.game.playersturn == WHITE:#change turn
                    self.game.playersturn = BLACK
                else : self.game.playersturn = WHITE
                self.game.rounds[0] += self.game.rounds[1]#parse record for next round
                if self.game.rounds[1] != 0:
                    self.game.rounds[1] = 0
                else:
                    self.game.rounds[1] = 1
            else :
                self.output.insert(TOP, "\ninvalid move")
        else : pass#game.message = "there is no piece in that space"
        self.output.insert(TOP,"\n"+self.game.message)#print message
        self.output.insert(TOP, "\nsteps:"+str(self.game.steps))
        self.output.insert(TOP, "\neaten:"+str(self.game.eaten))
        self.output.insert(TOP, "\ncastling_dict:"+str(self.game.castling_dict))       
        self.printpieces(self.game.gameboard)#display new pieces position on boardButtons


root = Tk()
root.geometry("1036x758")
app = chessGame(root, game1)
root.mainloop()
exit()
 