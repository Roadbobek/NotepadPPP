import tkinter as tk
from tkinter import font

root = tk.Tk()

available_fonts = list(font.families())
print(available_fonts)
available_fonts.sort()
print(available_fonts)