"""
a5.py

Starting point of the Assignment 5 module.
"""

# Kiva Vakharia
# 23234227
# kvakhari@uci.edu

import tkinter as tk
import tkinter.font as tkFont


def left_side(root):
    left_frame = tk.Frame(root, width=200, height=400, bg='#F6F4E8', bd=1, relief="solid")
    left_frame.grid(row=0, column=0, padx=10, pady=5, sticky='nsew')

    left_title = tk.Frame(left_frame, bg="white", height=25, bd=1, relief="solid")
    left_title.pack(fill='x', padx=10, pady=5)
    left_title.pack_propagate(False)  # Prevent resizing to fit the label

    label_font = tkFont.Font(family="Georgia", size=12)
    label = tk.Label(left_title, text="CONTACTS", bg="white", font=label_font)
    label.pack()
    left_frame.pack_propagate(False)

    button_font = tkFont.Font(family="Georgia", size=10)
    button = tk.Button(root, text="Add Contact", width=25, font=button_font)
    # TODO: add a command to the button
    button.grid(row=1, column=0, sticky='sw', padx=10, pady=10)


def right_side(root):
    right_frame = tk.Frame(root, width=650, height=400, bg='#F6F4E8')
    right_frame.grid(row=0, column=1, pady=5, sticky='nsew')
    right_frame.grid_propagate(False)

    upper_section = tk.Frame(right_frame, bg='#F6F4E8', width=650, height=350, bd=1, relief="solid")  # Adjust height as needed
    upper_section.pack(fill='both', expand=True, side='top')

    lower_section = tk.Frame(right_frame, bg='#F6F4E8', width=650, height=50, bd=1, relief="solid")  # Adjust height as needed
    lower_section.pack(fill='both', side='bottom')

    button_font = tkFont.Font(family="Georgia", size=9)
    button = tk.Button(lower_section, text="SEND", font=button_font)
    button.grid(row=0, column=1, sticky='e', padx=10, pady=10)

    entry_font = tkFont.Font(family='Georgia', size=12)
    entry = tk.Entry(lower_section, width=60, font=entry_font)
    entry.grid(row=0, column=0, sticky='ew', padx=20) 


def main():
    root = tk.Tk()
    root.title("ICS 32 Distributed Social Messenger")
    root.config(bg="#BACEC1")

    right_side(root)
    left_side(root)

    root.geometry("950x500")
    root.mainloop()

if __name__ == "__main__":
    main()

