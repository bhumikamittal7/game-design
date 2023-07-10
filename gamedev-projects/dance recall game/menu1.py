import tkinter as tk
from tkinter import ttk

import os
import pygame
import cv2
import tkinter as tk
from tkinter import messagebox
from pygame import mixer
import random
def freestyle():
    stream = open("freemode.py")
    read_file = stream.read()
    exec(read_file)
def level1():
    stream = open("level1.py")
    read_file = stream.read()
    exec(read_file)
def level2():
    stream = open("level2.py")
    read_file = stream.read()
    exec(read_file)

window = tk.Tk()
window.title("Dance Recall")
window.geometry("400x300")


style = ttk.Style()
style.configure("TButton",
                font=("Arial", 12),
                padding=10)


title_frame = ttk.Frame(window)
title_frame.pack(pady=20)


title_label = ttk.Label(title_frame, text="Dance Recall", font=("Arial", 16))
title_label.pack()


button_frame = ttk.Frame(window)
button_frame.pack(pady=20)


button1 = ttk.Button(button_frame, text="Free Style",command=freestyle)
button1.grid(row=0, column=0, padx=10)

button2 = ttk.Button(button_frame, text="Level 1", command=level1)
button2.grid(row=0, column=1, padx=10)

button3 = ttk.Button(button_frame, text="Level 2",command=level2)
button3.grid(row=0, column=2, padx=10)


window.mainloop()