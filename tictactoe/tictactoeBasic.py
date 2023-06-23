import tkinter as tk

window = tk.Tk()
window.resizable(False, False)
window.title("Tic Tac Toe")

tk.Label(window, text="Tic Tac Toe", font=('Arial', 25)).pack()

def reset_button(button, value):
    button.configure(text="", bg='white')
    value = None

def create_XO_point(x, y):
    value = None
    button = tk.Button(play_area, text="", width=10, height=5, command=lambda: set_point(x, y, button, value))
    button.grid(row=x, column=y)
    return button, value

current_chr = "X"
X_points = []
O_points = []

def set_point(x, y, button, value):
    global current_chr
    if not value:
        button.configure(text=current_chr, bg='snow', fg='black')
        value = current_chr
        if current_chr == "X":
            X_points.append((x, y))
            current_chr = "O"
        else:
            O_points.append((x, y))
            current_chr = "X"
        check_win()

def check_win():
    winning_possibilities = [
        [(1, 1), (1, 2), (1, 3)],
        [(2, 1), (2, 2), (2, 3)],
        [(3, 1), (3, 2), (3, 3)],
        [(1, 1), (2, 1), (3, 1)],
        [(1, 2), (2, 2), (3, 2)],
        [(1, 3), (2, 3), (3, 3)],
        [(1, 1), (2, 2), (3, 3)],
        [(3, 1), (2, 2), (1, 3)]
    ]

    for possibility in winning_possibilities:
        if all(point in X_points for point in possibility):
            print("X won!")
            reset_points()
            return
        elif all(point in O_points for point in possibility):
            print("O won!")
            reset_points()
            return

    if len(X_points) + len(O_points) == 9:
        print("Draw!")
        reset_points()

def reset_points():
    for button, value in XO_buttons:
        reset_button(button, value)
    X_points.clear()
    O_points.clear()

play_area = tk.Frame(window, width=300, height=300, bg='white')
play_area.pack(pady=10, padx=10)

XO_buttons = []
for x in range(1, 4):
    for y in range(1, 4):
        button, value = create_XO_point(x, y)
        XO_buttons.append((button, value))

window.mainloop()


