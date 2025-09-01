import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sys
import os

from print import print_ticket

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def on_enter(event):
    event.widget.config(bg="#FF3545")
def on_leave(event):
    event.widget.config(bg="#FF2545")


def clear_fields():
    input_customer_name.delete(0, tk.END)
    input_costume_number_1.delete(0, tk.END)
    input_costume_size_1.delete(0, tk.END)
    input_costume_number_2.delete(0, tk.END)
    input_costume_size_2.delete(0, tk.END)
    input_costume_number_3.delete(0, tk.END)
    input_costume_size_3.delete(0, tk.END)

def gather_data():

    customer_data_1 = {
        "customer": input_customer_name.get(),
        "costume_number": input_costume_number_1.get(),
        "costume_size": input_costume_size_1.get(),
    }

    customer_data_2 = {
        "customer": input_customer_name.get(),
        "costume_number": input_costume_number_2.get(),
        "costume_size": input_costume_size_2.get(),
    }

    customer_data_3 = {
        "customer": input_customer_name.get(),
        "costume_number": input_costume_number_3.get(),
        "costume_size": input_costume_size_3.get(),
    }

    data = [customer_data_1, customer_data_2, customer_data_3]
    # print(data)

    
    if customer_data_1["customer"].strip() and customer_data_1["costume_number"].strip() and customer_data_1["costume_size"].strip():
        for item in data:
            if item["customer"].strip() and item["costume_number"].strip() and item["costume_size"].strip():
                # print(item["customer"], item["costume_number"], item["costume_size"])
                print_ticket(item["customer"].strip(), item["costume_number"].strip(), item["costume_size"].strip())
                clear_fields()
            continue
            
        messagebox.showinfo("Success", f'Costume Ticket Printing...')


    else:
        messagebox.showinfo("Fail", f'Customer info not present')


# Window Setup
window = tk.Tk()
window.title("Basic Printing Terminal")
window.geometry("540x700")
window.configure(bg="#333333")

style = ttk.Style(window)
style.configure('Padded.TEntry', padding=(10, 5, 10, 5))

### Inner Window Content

pos_1 = (0,0,0,0)
logo_image = Image.open(resource_path("pc-logo.png"))
image_resized = logo_image.resize((500, 100), Image.LANCZOS)
image_header = ImageTk.PhotoImage(image_resized)

logo_label = tk.Label(window, image=image_header)
logo_label.grid(row=pos_1[0], column=pos_1[1], columnspan=2, padx=(20,5), pady=20, )

# Customer Name 
pos_2 = (1, 0, 1, 1)
label_customer_name = ttk.Label(window, text="Customer Name: ", font=("Helvetica", 16, "bold"), justify="left", anchor='w', foreground="#ffffff", background="#333333")
label_customer_name.grid(row=pos_2[0], column=pos_2[1], padx=16, pady=(30, 40), sticky='w')
input_customer_name = ttk.Entry(window, font=("Helvetica", 16), style='Padded.TEntry')
input_customer_name.grid(row=pos_2[2], column=pos_2[3], padx=16, pady=(30, 40) )


# Costume Number 1
pos_3 = (2, 0, 2, 1)
label_costume_number_1 = ttk.Label(window, text="Costume Number: ", font=("Helvetica", 16, "bold"), justify="left", anchor='w', foreground="#ffffff", background="#333333")
label_costume_number_1.grid(row=pos_3[0], column=pos_3[1], padx=16, pady=(25, 5), sticky='w' )
input_costume_number_1 = ttk.Entry(window, font=("Helvetica", 16), style='Padded.TEntry')
input_costume_number_1.grid(row=pos_3[2], column=pos_3[3], padx=16, pady=(25, 5) )


# Costume Size 1
pos_4 = (3, 0, 3, 1)
label_costume_size_1 = ttk.Label(window, text="Costume Size: ", font=("Helvetica", 16, "bold"), justify="left", anchor='w', foreground="#ffffff", background="#333333")
label_costume_size_1.grid(row=pos_4[0], column=pos_4[1], padx=16, pady=(5, 5), sticky='w' )
input_costume_size_1 = ttk.Entry(window, width=20, font=("Helvetica", 16), style='Padded.TEntry')
input_costume_size_1.grid(row=pos_4[2], column=pos_4[3], padx=16, pady=(5, 5) )


# Costume Number 2
pos_5 = (4, 0, 4, 1)
label_costume_number_2 = ttk.Label(window, text="Costume Number: ", font=("Helvetica", 16, "bold"), justify="left", anchor='w', foreground="#ffffff", background="#333333")
label_costume_number_2.grid(row=pos_5[0], column=pos_5[1], padx=16, pady=(25, 5), sticky='w' )
input_costume_number_2 = ttk.Entry(window, font=("Helvetica", 16), style='Padded.TEntry')
input_costume_number_2.grid(row=pos_5[2], column=pos_5[3], padx=16, pady=(25, 5) )


# Costume Size 2
pos_6 = (5, 0, 5, 1)
label_costume_size_2 = ttk.Label(window, text="Costume Size: ", font=("Helvetica", 16, "bold"), justify="left", anchor='w', foreground="#ffffff", background="#333333")
label_costume_size_2.grid(row=pos_6[0], column=pos_6[1], padx=16, pady=(5, 5), sticky='w' )
input_costume_size_2 = ttk.Entry(window, width=20, font=("Helvetica", 16), style='Padded.TEntry')
input_costume_size_2.grid(row=pos_6[2], column=pos_6[3], padx=16, pady=(5, 5) )


# Costume Number 3
pos_7 = (6, 0, 6, 1)
label_costume_number_3 = ttk.Label(window, text="Costume Number: ", font=("Helvetica", 16, "bold"), justify="left", anchor='w', foreground="#ffffff", background="#333333")
label_costume_number_3.grid(row=pos_7[0], column=pos_7[1], padx=16, pady=(25, 5), sticky='w' )
input_costume_number_3 = ttk.Entry(window, font=("Helvetica", 16), style='Padded.TEntry')
input_costume_number_3.grid(row=pos_7[2], column=pos_7[3], padx=16, pady=(25, 5) )


# Costume Size 3
pos_8 = (7, 0, 7, 1)
label_costume_size_3 = ttk.Label(window, text="Costume Size: ", font=("Helvetica", 16, "bold"), justify="left", anchor='w', foreground="#ffffff", background="#333333")
label_costume_size_3.grid(row=pos_8[0], column=pos_8[1], padx=16, pady=(5, 5), sticky='w' )
input_costume_size_3 = ttk.Entry(window, width=20, font=("Helvetica", 16), style='Padded.TEntry')
input_costume_size_3.grid(row=pos_8[2], column=pos_8[3], padx=16, pady=(5, 5) )


# Submit Button
pos_9 = (8, 1,)
submit_button = tk.Button(window, command=gather_data, text="Print Ticket", font=("Helvetica", 20, "bold"), pady=8, justify="center", foreground="#ffffff", background="#e45e22", activebackground="#0ac203", activeforeground="#FFFFFF")
submit_button.grid(row=pos_9[0], rowspan=2, column=pos_9[1], padx=20, pady=60, sticky="nsew")
# submit_button.bind("<Enter>", on_enter)
# submit_button.bind("<Leave>", on_leave)



# Main Program Loop
window.mainloop()