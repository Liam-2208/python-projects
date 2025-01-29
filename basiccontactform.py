import tkinter as tk
from tkinter import messagebox

window = tk.Tk()
window.title("Contact Form")

def buttonClick():
    name = entry_name.get()
    messagebox.showinfo("showinfo", "Thank you for your submission " +  name + "!" )   

submit_button = tk.Button(window, command= buttonClick, text="Submit")
submit_button.grid(row=3, column=1)

label_name = tk.Label(window, text="Name:")
label_name.grid(row=0, column=0, pady=5,)
entry_name = tk.Entry(window, width=30)
entry_name.grid(row=0, column=1, pady=5,)



label_email = tk.Label(window, text="Email:")
label_email.grid(row=1, column=0, pady=5,)
entry_email = tk.Entry(window, width=30)
entry_email.grid(row=1, column=1, pady=5,)

label_message = tk.Label(window, text="Message:")
label_message.grid(row=2, column=0)
text_message = tk.Text(window, height=5, width=30)
text_message.grid(row=2, column=1, pady=5)


window.mainloop()
