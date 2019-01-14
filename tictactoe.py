#-------------------------------------------------------------------------------
# Name:         TicTacToe
# Purpose:      for fun, for kids
# Version       1.0
# Author:       luka
#
# Created:      07.01.2019
# Copyright:    None
# Licence:      open source
#-------------------------------------------------------------------------------
            
from tkinter import Tk, Frame, Button, Entry, Canvas, Label
import time
            
class Gui(Frame):
    def __init__(self, master):
        self.master = master
        self.font1 = font=("Segoe UI",18,"bold")
        self.font2 = font=("Segoe UI",26,"bold")
        Frame.__init__(self, self.master)
        self.grid()

        self.button_list = []       #list for tictactoe buttons
        self.cur_player = True      #player1 begins
        self.counter_pressed = 0    #how many times is pressed
        self.counter_buttons = 0
        self.backup_pressed = []

        self.create_containers()
        self.create_grid()
        self.game = Game(self.button_list)
        self.create_userinput()
    
    def create_containers(self):
        self.frame_info = Frame(self)                           #for all infos, player, score....   
        self.frame_tictactoe = Frame(self, pady=20, padx=20)    #for main window of tictactoe
        self.frame_userinput = Frame(self)                      #for users input

        self.frame_info.grid(row=0, column=0)
        self.frame_tictactoe.grid(row=1, column=0, padx=5)
        self.frame_userinput.grid(row=2, column=0)
    
    def create_grid(self):
        for i in range(3):
            for j in range(3):
                x = Button(self.frame_tictactoe, text=" ", 
                            font=self.font1, width=5, height=2, relief="ridge",
                            command=lambda x=self.counter_buttons:self.pressed(x))
                x.grid(row=i , column=j)
                self.button_list.append(x)  #button_list stores all tk buttons
                self.counter_buttons += 1
    
    def create_userinput(self):
        self.input_label = Label(self.frame_userinput, font=self.font1, text="Player 1 \'X\'")
        self.input_label.grid(row=0, column=0)
        self.ok_button = Button(self.frame_userinput, text="Again",
                                font=self.font1, command=self.again, padx=20)
        self.ok_button.grid(row=0, column=1)
    
    def again(self):
            self.button_list = []
            self.cur_player = True
            self.counter_pressed = 0
            self.counter_buttons = 0
            self.backup_pressed = []
            self.create_grid()
            self.game.set_button_list(self.button_list)
            self.input_label.configure(text="Player 1 \'X\'", bg="SystemButtonFace")    
            
    def pressed(self, id):        
        if self.button_list[id].cget("text") is not " ":
            return
        else:
            self.counter_pressed += 1
            if self.cur_player == True:
                self.button_list[id].configure(text="X")
                self.backup_pressed.append((id,"X"))
                self.cur_player = False
                self.input_label.configure(text="Player 2 \'O\'")
            else:
                self.button_list[id].configure(text="O")
                self.backup_pressed.append((id,"O",))
                self.cur_player = True
                self.input_label.configure(text="Player 1 \'X\'")         
            if self.counter_pressed < 5:
                return   
            else: 
                self.check_table()
            
    def check_table(self):
        check = self.game.test_check(self.backup_pressed)
        print("check ", check)
        if check:
            if self.cur_player:
                print("Player2 wins")
                self.input_label.configure(text="Player 2 wins", bg="Lime")
                self.disable_buttons()
                self.highlight_buttons(check[1])
            else:
                print("Player1 wins")
                self.input_label.configure(text="Player 1 wins", bg="Lime")
                self.disable_buttons()
                self.highlight_buttons(check[1])
                
                
        if self.counter_pressed == 9 and check == None:
            print("Tie")
            self.input_label.configure(text="Tie", bg="salmon")
            self.disable_buttons()
            
    def disable_buttons(self):
        for i in self.button_list:
            i.configure(state="disabled")
    
    def highlight_buttons(self, buttons_positions):
        for i in buttons_positions:
            self.button_list[i].configure(fg="sky blue", state="normal", command=self.passing)
    
    def passing(self):
        pass
        
class Game():
    def __init__(self, button_list=None):
        self.list_lookup = self.ls_get_lookup()
        self.button_list = button_list
    
    def set_button_list(self, arg):
        self.button_list = arg
        
    def ls_get_lookup(self):
        pattern_1 = [(1,2),(3,6),(4,8)]         #position 0
        pattern_2 = [(4,7),(0,2)]               #position 1
        pattern_3 = [(1,0),(5,8),(4,6)]         #position 2
        pattern_4 = [(0,6),(4,5)]               #position 3
        pattern_5 = [(1,7),(3,5),(2,6),(0,8)]   #position 4
        pattern_6 = [(2,8),(3,4)]               #position 5
        pattern_7 = [(3,0),(7,8),(4,2)]         #position 6
        pattern_8 = [(6,8),(1,4)]               #position 7
        pattern_9 = [(6,7),(2,5),(0,4)]         #position 8
                        
        list_lookup_pattern =   [pattern_1, pattern_2, pattern_3,
                                pattern_4, pattern_5, pattern_6,
                                pattern_7, pattern_8, pattern_9]
                        
        return list_lookup_pattern
        
    def test_check(self, table): 
        """table stack of pressed button data"""
        position = table[-1][0] # starts from 0
        flag = table[-1][1]    #variable for sought sign
        loop = len(self.list_lookup[position])
        print("ssss", self.list_lookup[position])
        tmp_list = []
        for i in range(loop):
            for j in range(2):
                #check if tk buttons are same as flag
                if self.button_list[self.list_lookup[position][i][j]].cget("text") == flag:
                    tmp_answer = True
                    tmp_list.append(tmp_answer)
            if len(tmp_list) == 2:
                # print("Correct")
                win_positions = self.list_lookup[position][i]
                win_positions += (position,)
                print("win_positions ", win_positions)
                return True, win_positions
            else:
                tmp_list = []
        
if __name__ == "__main__":
    root = Tk()
    app = Gui(root)
    root.mainloop()
