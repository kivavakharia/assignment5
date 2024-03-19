"""
a5.py

Starting point of the Assignment 5 module.
"""

# Kiva Vakharia
# 23234227
# kvakhari@uci.edu

import tkinter as tk
from gui import MainApp

def main():
    """Run the Graphical User Interface."""
    root = tk.Tk()
    root.title("ICS 32 Distributed Social Messenger")
    root.config(bg="#FFCAD4")
    root.geometry("950x500")
    MainApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
