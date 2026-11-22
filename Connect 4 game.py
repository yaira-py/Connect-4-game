import tkinter as tk
import random
from tkinter import messagebox

class ConnectFour:
    def __init__(self,root):
        self.root=root
        self.root.title('Connect Four Game')
        self.root.configure(bg='#1e1e2e')
        self.root.resizable(False,False)

        self.rows,self.cols=6,7
        self.board= [['' for _ in range(self.cols)] for _ in range(self.rows)]
        self.buttons=[]
        self.game_over=False
        self.player_turn = True

        
        self.status=tk.Label(self.root,text= 'your turn - Red 🔴',font=('Arial',13), bg='#1e1e2e',fg='yellow')
        self.status.pack()

        board_frame=tk.Frame(self.root,bg='#1e1e2e')
        board_frame.pack(padx=10,pady=10)


        for r in range(self.rows):
            row=[]
            for c in range(self.cols):
                btn=tk.Button(board_frame,text='',font=('Arial',20),width=3,height=1,bg='white',activebackground='white',command=lambda col=c: self.player_move(col))
                btn.grid(row=r,column=c,padx=4,pady=4)

                row.append(btn)
            self.buttons.append(row)

        tk.Button(self.root,text='🔄 Restart', font=('Arial',12,'bold'),bg='green',fg='white', command=self.restart).pack(pady=10)


    def update_board(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c]=='R':
                    self.buttons[r][c].config(text='⚈',fg='red',bg='white')
                elif self.board[r][c]=='Y':
                    self.buttons[r][c].config(text='⚈',fg='#e6b800',bg='white')
                else:
                    self.buttons[r][c].config(text='',bg='white')


    def drop_piece(self,col,piece):
        for r in range(self.rows-1,-1,-1):
            if self.board[r][col]=='':
                self.board[r][col]=piece
                return True
        return False

    def check_win(self,piece):
        for r in range(self.rows):
            for c in range(self.cols-3):
                if all(self.board[r][c+i]==piece for i in range(4)):
                    return [(r,c+i) for i in range(4)]

        for r in range(self.rows-3):
                for c in range(self.cols):
                    if all(self.board[r+i][c]==piece for i in range(4)):
                        return [(r+i,c) for i in range(4)]

        for r in range(self.rows-3):
                for c in range(self.cols-3):
                    if all(self.board[r+i][c+i]==piece for i in range(4)):
                        return [(r+i,c+i) for i in range(4)]

        for r in range(self.rows):
                for c in range(self.cols-3):
                    if all(self.board[r-i][c+i]==piece for i in range(4)):
                        return [(r-i,c+i) for i in range(4)]

        return None

    def highlight_win(self,cells):
        for r,c in cells:
            self.buttons[r][c].config(bg="lightgreen")

    def end_game(self,win_text,win_cells):
        self.game_over=True
        self.highlight_win(win_cells)
        self.update_board()

        self.root.after(300,lambda: messagebox.showinfo('Game Over',win_text))
    

    def player_move(self,col):
        if self.game_over or not self.player_turn:
            return

        if not self.drop_piece(col,'R'):
            self.status.config(text='column is full')
            return

        self.update_board()
        win_cells=self.check_win('R')
        if win_cells:
            self.status.config(text='you win!🎉')
            self.end_game('you win! 4 connected',win_cells)
            return

        if all(self.board[0][c]!= '' for c in range(self.cols)):
            self.status.config(text='its a Draw')
            self.game_over=True
            return

        self.player_turn=False
        self.status.config(text='Computer is thinking')
        self.root.after(600,self.com_move)
                                

    def com_move(self):
        if self.game_over:
            return

        valid= [c for c in range(self.cols) if self.board[0][c]=='']
        if valid:
            self.drop_piece(random.choice(valid),'Y')
            self.update_board()
            win_cells=self.check_win('Y')

            if win_cells:
                self.status.config(text='Computer win')
                self.end_game('Computer win! 4 connected',win_cells)
                return

            if all(self.board[0][c]!= '' for c in range(self.cols)):
                    self.status.config(text='its a Draw')
                    self.game_over=True
                    return

        self.player_turn=True
        self.status.config(text='your turn - Red 🔴')



    def restart(self):
        self.board= [['' for _  in range(self.cols)] for _ in range(self.rows)]
        self.game_over=False
        self.player_turn=True
        self.update_board()
        self.status.config(text='your turn - Red 🔴')
       






if __name__ =="__main__":
    win=tk.Tk()
    app=ConnectFour(win)
    win.mainloop()
