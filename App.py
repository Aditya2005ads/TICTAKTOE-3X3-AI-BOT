import tkinter as tk
import numpy as np

def check_winner():
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != "":
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != "":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "":
        return board[0][2]
    return None

def is_draw():
    return all(board[i][j] != "" for i in range(3) for j in range(3))

def minimax(board, depth, is_maximizing):
    winner = check_winner()
    if winner == "X": return -10
    if winner == "O": return 10
    if is_draw(): return 0
    
    if is_maximizing:
        best_score = -float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "O"
                    score = minimax(board, depth + 1, False)
                    board[i][j] = ""
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "X"
                    score = minimax(board, depth + 1, True)
                    board[i][j] = ""
                    best_score = min(score, best_score)
        return best_score

def find_best_move():
    best_score = -float("inf")
    best_move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == "":
                board[i][j] = "O"
                score = minimax(board, 0, False)
                board[i][j] = ""
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    return best_move

def on_click(row, col):
    if board[row][col] == "" and not check_winner():
        board[row][col] = "X"
        buttons[row][col].config(text="X", state="disabled")
        if check_winner() or is_draw():
            end_game()
            return
        ai_move()

def ai_move():
    move = find_best_move()
    if move:
        row, col = move
        board[row][col] = "O"
        buttons[row][col].config(text="O", state="disabled")
    if check_winner() or is_draw():
        end_game()

def end_game():
    winner = check_winner()
    if winner:
        result_label.config(text=f"{winner} Wins!")
    elif is_draw():
        result_label.config(text="It's a Draw!")
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(state="disabled")

def restart_game():
    global board
    board = [["" for _ in range(3)] for _ in range(3)]
    result_label.config(text="")
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text="", state="normal")

root = tk.Tk()
root.title("Tic-Tac-Toe")
board = [["" for _ in range(3)] for _ in range(3)]
buttons = [[None for _ in range(3)] for _ in range(3)]
for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(root, text="", font=("Arial", 24), width=5, height=2,
                                  command=lambda i=i, j=j: on_click(i, j))
        buttons[i][j].grid(row=i, column=j)
result_label = tk.Label(root, text="", font=("Arial", 18))
result_label.grid(row=3, column=0, columnspan=3)
restart_button = tk.Button(root, text="Restart", font=("Arial", 14), command=restart_game)
restart_button.grid(row=4, column=0, columnspan=3)
root.mainloop()
