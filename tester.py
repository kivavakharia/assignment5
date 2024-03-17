import tkinter as tk
import tkinter.simpledialog as sd

# Initialize a list to store contacts
contact_list = []

# Function to add a new contact
def add_contact():
    # Prompt the user for the contact's name
    name = sd.askstring("New Contact", "Enter the name of the new contact:")
    if name:
        # Add the contact to the list
        contact_list.append(name)
        # Optionally, you can print or do something else with the new contact name
        print("New contact added:", name)

# Create a Tkinter window
window = tk.Tk()


# Button to add a new contact
add_button = tk.Button(window, text="Add Contact", command=add_contact)
add_button.pack()

# Start the Tkinter event loop
window.mainloop()
