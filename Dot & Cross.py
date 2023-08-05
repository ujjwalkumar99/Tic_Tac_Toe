import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk

# Function to check if someone has won
def check_winner(board, player):
    # Check rows, columns, and diagonals for a win
    for i in range(3):
        if all(board[i][j] == player for j in range(3)):
            return True

    for j in range(3):
        if all(board[i][j] == player for i in range(3)):
            return True

    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True

    return False

# Function to handle the button click
def on_click(event):
    global current_player, board, winner

    if not winner:
        col = event.x // cell_size
        row = event.y // cell_size

        if not board[row][col]:
            if current_player == 'O':
                canvas.create_image(col * cell_size + cell_size//2, row * cell_size + cell_size//2, anchor=tk.CENTER, image=dot_icon, tags=f"move_{row}_{col}")
                board[row][col] = 'O'
            else:
                canvas.create_image(col * cell_size + cell_size//2, row * cell_size + cell_size//2, anchor=tk.CENTER, image=cross_icon, tags=f"move_{row}_{col}")
                board[row][col] = 'X'

            if check_winner(board, current_player):
                show_winner(current_player)
                return

            if all(board[i][j] for i in range(3) for j in range(3)):
                show_winner("Draw")
                return

            current_player = 'X' if current_player == 'O' else 'O'  # Switch player for the next move

def show_winner(player):
    global winner
    if player == "Draw":
        result_label.config(text="It's a Draw!", font=("Arial", 24, "bold"), background=current_bg_color)
    else:
        result_label.config(text=f"Player {player} wins!", font=("Arial", 24, "bold"), background=current_bg_color)
    winner = player

def play_again():
    global board, current_player, winner
    for i in range(3):
        for j in range(3):
            canvas.delete(f"move_{i}_{j}")
            board[i][j] = ''

    winner = None
    current_player = 'X'
    result_label.config(text="", background=current_bg_color)

def change_bg_color(color):
    global current_bg_color
    root.configure(bg=color)
    canvas.configure(bg=color)  # Set canvas background to the same color
    result_box.configure(bg=color)  # Set result box background to the same color
    current_bg_color = color
    result_label.config(background=current_bg_color)

def about():
    messagebox.showinfo("About", "Tic Tac Toe Game\nVersion 1.0\nCreated by UK")

def main():
    global root, canvas, cell_size, board, current_player, winner, dot_icon, cross_icon, result_label, result_box, play_again_button, current_bg_color

    root = tk.Tk()
    root.title("Tic Tac Toe")
    root.geometry("345x470")
    current_bg_color = "yellow"
    root.configure(bg=current_bg_color)  # Set yellow background

    cell_size = 325 // 3  # Adjust cell size to fit the board properly

    cross_icon = Image.open("cross_icon.png").resize((int(cell_size*0.8), int(cell_size*0.8)), Image.LANCZOS)
    cross_icon = ImageTk.PhotoImage(cross_icon)

    dot_icon = Image.open("dot_icon.png").resize((int(cell_size*0.8), int(cell_size*0.8)), Image.LANCZOS)
    dot_icon = ImageTk.PhotoImage(dot_icon)

    board = [['' for _ in range(3)] for _ in range(3)]
    current_player = 'X'
    winner = None

    # Create the tic-tac-toe board canvas
    canvas = tk.Canvas(root, width=cell_size * 3, height=cell_size * 3, bg=current_bg_color, highlightthickness=0)
    canvas.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
    canvas.bind("<Button-1>", on_click)

    # Draw the tic-tac-toe lines with increased width
    for i in range(1, 3):
        canvas.create_line(i * cell_size, 0, i * cell_size, cell_size * 3, fill="black", width=8)
        canvas.create_line(0, i * cell_size, cell_size * 3, i * cell_size, fill="black", width=8)

    # Create result label box
    result_box = tk.Frame(root, bg=current_bg_color, width=325, height=50)
    result_box.grid(row=1, column=0, columnspan=3, padx=10, pady=5)

    result_label = ttk.Label(result_box, text="", foreground="black", font=("Arial", 24, "bold"), background=current_bg_color)
    result_label.pack(expand=True, fill="both")

    # Set initial 'X' and 'O' icons on the board according to the board cells
    for i in range(3):
        for j in range(3):
            if board[i][j] == 'X':
                canvas.create_image(j * cell_size + cell_size//2, i * cell_size + cell_size//2, anchor=tk.CENTER, image=cross_icon, tags=f"move_{i}_{j}")
            elif board[i][j] == 'O':
                canvas.create_image(j * cell_size + cell_size//2, i * cell_size + cell_size//2, anchor=tk.CENTER, image=dot_icon, tags=f"move_{i}_{j}")

    # Create play again button
    play_again_button = ttk.Button(root, text="Play Again", style="GameButton.TButton", command=play_again)
    play_again_button.grid(row=2, column=0, columnspan=3, padx=10, pady=5)

    # Menu Bar
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    # Help Menu
    help_menu = tk.Menu(menubar, tearoff=0)
    help_menu.add_command(label="About", command=about)
    menubar.add_cascade(label="Help", menu=help_menu)

    # Settings Menu
    settings_menu = tk.Menu(menubar, tearoff=0)
    settings_menu.add_command(label="Yellow", command=lambda: change_bg_color("yellow"))
    settings_menu.add_command(label="White", command=lambda: change_bg_color("white"))
    settings_menu.add_command(label="Light Blue", command=lambda: change_bg_color("lightblue"))
    menubar.add_cascade(label="Settings", menu=settings_menu)

    root.mainloop()

if __name__ == "__main__":
    main()
