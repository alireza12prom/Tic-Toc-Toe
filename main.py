from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from board import Board
import random
import time

class Game:
    def __init__(self, player1, player2, mode):
        self.__player1_nut = player1
        self.__player1_score = 0

        self.__player2_nut = player2
        self.__player2_score = 0
        
        self.__mode = mode

        self.__turn = self.__player1_nut
        self.__board = Board()
    
    @property
    def player1(self):
        return {"nut":self.__player1_nut, "score":self.__player1_score}
    
    @property    
    def player2(self):
        return {"nut":self.__player2_nut, "score":self.__player2_score}
    
    @property
    def turn(self):
        return self.__turn
    
    @property
    def mode(self):
        return self.__mode
    
    
    def requestForMove(self, n):
        self.__board.move(n, self.__turn)
        
        if self.requestForCheckSituation() == 1:
            if self.__turn == self.__player1_nut:
                self.__player1_score += 1
            else:
                self.__player2_score += 1

        else:
            self.__turn = "X" if self.__turn == "O" else "O"
        
    
    def requestForCheckSituation(self):
        result = self.__board.winner()
        return result
            

    def requestForReset(self):
        self.__board.reset()
        self.__turn = self.__player1_nut

    @staticmethod
    def __machine(nut:int, board:list):
        """ 
        [
            0:[0,1,2],
            1:[0,1,2],
            2:[0,1,2]
        ]
        """
        rowsIndex = [
            (0,0, 0,1, (0,2)), (0,0, 0,2, (0,1)), (0,1, 0,2, (0,0)),
            (1,0, 1,1, (1,2)), (1,0, 1,2, (1,1)), (1,1, 1,2, (1,0)),
            (2,0, 2,1, (2,2)), (2,0, 2,2, (2,1)), (2,1, 2,2, (2,0))
        ]

        columnsIndex = [
            (0,0, 1,0 ,(2,0)), (1,0, 2,0, (0,0)), (0,0 ,2,0, (1,0)),
            (0,1, 1,1, (2,1)), (1,1, 2,1, (0,1)), (0,1, 2,1, (1,1)),
            (0,2, 1,2, (2,2)), (1,2, 2,2, (0,2)), (0,2, 2,2, (1,2))
            ]
        
        diameterIndex = [
            (0,0, 1,1, (2,2)), (1,1, 2,2, (0,0)), (0,0, 2,2, (1,1)),
            (0,2, 1,1, (2,0)), (1,1, 2,0, (0,2)), (0,2, 2,0, (1,1))
            ]

        for IndexMap in [rowsIndex, columnsIndex, diameterIndex]:
            for index in IndexMap:
                row1, column1, row2, column2, answer = index
                row3, column3 = answer
                for row in range(3):
                    if board[row1][column1] == nut and \
                        board[row2][column2] == nut and board[row3][column3] == " ":
                        return answer
        
    def requestForBot(self):
        for nut in [self.__player2_nut, self.__player1_nut]:
            respons = self.__machine(nut, self.__board.board)
            if respons != None:
                return respons
        
        while True:
            row = random.randint(0,2)
            column = random.randint(0,2)
            if self.__board.board[row][column] == ' ':
                return (row, column)
        
        

            

        


def intro():
    window = Tk()
    window.title("Tic-Toc-Toe.Welcome :)")
    window.geometry("300x100")
    window.resizable(False, False)

    def click_start_game(player1_nut:str, player_mode:str):
        if player1_nut == "":
            messagebox.showinfo("Tic Toc Toe","Please select your nut!")
        elif player_mode == "":
            messagebox.showinfo("Tic Toc Toe", "Please specify that you play with 'Humen' or th 'Bot'")
        else:
            player2_nut = "X" if player1_nut == "O" else "O"
            window.destroy()
        
            game = Game(player1_nut, player2_nut, player_mode)
            main(game)


    root = Frame(window)
    root.pack()

    lbl1 = Label(root, text="Chose your nut:")
    lbl1.grid(ipady=10)

    selectNut = ttk.Combobox(root, state="readonly", values=["X", "O"], width=4)
    selectNut.grid(row=0, column=1)

    lbl2 = Label(root, text=" Play with:")
    lbl2.grid(row=0, column=2)

    selectPlayer = ttk.Combobox(root, state="readonly", values=["Humen", "Robot"], width=7)
    selectPlayer.grid(row=0, column=3)

    startBtn = ttk.Button(window, text="Start", width=20)
    startBtn.pack(ipady=10)
    startBtn.configure(command= lambda: click_start_game(selectNut.get(), selectPlayer.get()))
    
    window.mainloop()
    


def main(game=None):
    """ game: an instance of Game class """

    window = Tk()
    window.title("Tic Toc Toe", )
    window.geometry("390x520")
    window.configure(bg='white')
    window.resizable(False, False)

    player1_turn_lbl = None
    player2_turn_lbl = None
    buttons = None

    detail = Frame(window,bg='white')
    detail.pack(ipadx=1)

    btnFrame = Frame(window)
    btnFrame.pack()

    def body():
        nonlocal player1_turn_lbl, player2_turn_lbl, buttons

        if game.mode == "Humen":

            player1_score_lbl = Label(detail, text="Player 1: {}".format(game.player1["score"]), font=("Behavier", 18), bg='white')
            player1_score_lbl.grid(row=0, column=0, ipadx=20)
            
            player2_score_lbl = Label(detail, text="Player 2: {}".format(game.player2['score']), font=("Behavier", 18), bg='white')
            player2_score_lbl.grid(row=0, column=1)

            player1_turn_lbl = Label(detail, text=game.player1["nut"], font=("Behavier", 42, 'bold'), bg='white')
            player1_turn_lbl.grid(row=1, column=0)
            
            player2_turn_lbl = Label(detail, text=game.player2["nut"], font=("Behavier", 42, 'bold'), bg='white', fg="white")
            player2_turn_lbl.grid(row=1, column=1)
        
        
        else:
            player1_score_lbl = Label(detail, text="You(^_^): {}".format(game.player1["score"]), font=("Behavier", 18), bg='white')
            player1_score_lbl.grid(row=0, column=0, ipadx=20)
            
            player2_score_lbl = Label(detail, text="Bot[O_O]: {}".format(game.player2['score']), font=("Behavier", 18), bg='white')
            player2_score_lbl.grid(row=0, column=1)

            player1_turn_lbl = Label(detail, text=game.player1["nut"], font=("Behavier", 42, 'bold'), bg='white')
            player1_turn_lbl.grid(row=1, column=0)
            
            player2_turn_lbl = Label(detail, text=game.player2["nut"], font=("Behavier", 42, 'bold'), bg='white')
            player2_turn_lbl.grid(row=1, column=1)





        btn1 = Button(btnFrame, text=' ', font=("Behavier", 50), width=3, border=1)
        btn1.grid(row=0, column=0)
        btn1.configure(command= lambda: request(0, btn1))

        btn2 = Button(btnFrame, text=' ', font=("Behavier", 50), width=3, border=1)
        btn2.grid(row=0, column=1)
        btn2.configure(command= lambda: request(1, btn2))

        btn3 = Button(btnFrame, text=' ', font=("Behavier", 50), width=3, border=1)
        btn3.grid(row=0, column=2)
        btn3.configure(command= lambda: request(2, btn3))



        btn4 = Button(btnFrame, text=' ', font=("Behavier", 50), width=3, border=1)
        btn4.grid(row=1, column=0)
        btn4.configure(command= lambda: request(3, btn4))

        btn5 = Button(btnFrame, text=' ', font=("Behavier", 50), width=3, border=1)
        btn5.grid(row=1, column=1)
        btn5.configure(command= lambda: request(4, btn5))

        btn6 = Button(btnFrame, text=' ', font=("Behavier", 50), width=3, border=1)
        btn6.grid(row=1, column=2)
        btn6.configure(command= lambda: request(5, btn6))



        btn7 = Button(btnFrame, text=' ', font=("Behavier", 50), width=3, border=1)
        btn7.grid(row=2, column=0)
        btn7.configure(command= lambda: request(6, btn7))

        btn8 = Button(btnFrame, text=' ', font=("Behavier", 50), width=3, border=1)
        btn8.grid(row=2, column=1)
        btn8.configure(command= lambda: request(7, btn8))

        btn9 = Button(btnFrame, text=' ', font=("Behavier", 50), width=3, border=1)
        btn9.grid(row=2, column=2)
        btn9.configure(command= lambda: request(8, btn9))




        resetBtn = ttk.Button(btnFrame, text="Play Again", width=20)
        resetBtn.grid(row=3, column=0)
        resetBtn.configure(command=resetCommand)

        settingBtn = ttk.Button(btnFrame, text="Setting", width=19)
        settingBtn.grid(row=3, column=1)
        settingBtn.configure(command=settingCommad)

        ExitBtn = ttk.Button(btnFrame, text="Exit", width=20)
        ExitBtn.grid(row=3, column=2)
        ExitBtn.configure(command=window.destroy)


        buttons = [
            [btn1, btn2, btn3],
            [btn4, btn5, btn6],
            [btn7, btn8, btn9]
        ]

    def request(n, btn):
        if btn['text'] != " ":
            return
        
        btn.configure(text=game.turn)
        game.requestForMove(n)
        respons = game.requestForCheckSituation()
        
        if respons == 1: 
            messagebox.showinfo("Finish", "Player {} is winner".format(btn['text']))
            resetCommand()
        
        elif respons == 2:
            messagebox.showinfo("Finish", "Equal!")
            resetCommand()
        
        elif game.mode == "Humen":
            if player1_turn_lbl["fg"] == "white":
                player1_turn_lbl.configure(fg="black")
                player2_turn_lbl.configure(fg="white")
            else:
                player2_turn_lbl.configure(fg="black")
                player1_turn_lbl.configure(fg="white")
        
        # bot moving
        else:
            respons = game.requestForBot()
            row, column = respons

            btn = buttons[row][column]
            btn.configure(text=game.turn)
                
            if row == 0:
                game.requestForMove(column)
            elif row == 1:
                rowMap = {0:3, 1:4, 2:5}
                game.requestForMove(rowMap[column])
            elif row == 2:
                rowMap = {0:6, 1:7, 2:8}
                game.requestForMove(rowMap[column])

            respons = game.requestForCheckSituation()

            if respons == 1: 
                messagebox.showinfo("Finish", "Bot[0,0] is winner")
                resetCommand()

            elif respons == 2:
                messagebox.showinfo("Finish", "Equal!")
                game.requestForReset()
                resetCommand()

    
    def resetCommand():
        game.requestForReset()
        body() 
    
    def settingCommad():
        window.destroy()
        intro()  

    body()
    window.mainloop()


if __name__ == "__main__":
    intro()