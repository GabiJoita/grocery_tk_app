""" Use this app to add you favourite products on a grocery list"""

import tkinter as tk
import csv
import customtkinter as cst
from tkinter import messagebox
from list_data import MyDbList


def add_product():
    """ create a function to put products
        inside your listbox, manually,
        than save the list in a csv file
     """
    product = product_entry.get()
    list_prod.insert(tk.END, f'{product} lei')
    product_entry.delete(0, tk.END)
    if product:
        with open('grocery_list.csv', 'a', newline="") as fr:
            writer = csv.writer(fr)
            writer.writerow([product])
    else:
        messagebox.showerror(message='please, enter a product')


def prod_categories():
    categories = ['fruits', 'food', 'drinks']


def total_price():
    """ now use indexing to take the price
        from our list and calculate the total sum
        of all products
     """
    total = 0
    for item in list_prod.get(0, tk.END):
        price = float(item.split()[-2])
        total += price
    return total


def show_total_price():
    """ open another window in your project
        to show the total price
    """
    s_tot = total_price()
    top = tk.Toplevel()
    top.configure(bg='#857EFF')
    top.geometry('200x100')
    label = tk.Label(top, text='', textvariable=index, bg='#857EFF')
    label.pack()
    index.set(s_tot)


def delete_product():
    """ clear the listbox and add
        new products
    """
    prod_del = list_prod.curselection()
    for items in prod_del[::-1]:
        list_prod.delete(items)


def import_data():
    """ create a function to open a data list
        from sqlite
    """
    db = MyDbList()
    all_prod = db.query_all()
    for product in all_prod:
        list_prod.insert(tk.END, f'{product[0]} {product[1]}'
                                 f' {product[2]} {product[3]} {product[4]}')


if __name__ == "__main__":
    root = tk.Tk()
    root.title('grocery list')
    root.geometry('600x500')
    root.config(background='#1B0A6B')
    index = tk.IntVar()

    product_text = tk.Label(root, text='enter a product:', background='#1B0A6B', foreground='white')
    product_text.grid(row=0, column=0, padx=10, pady=10)

    product_entry = tk.Entry(root, width=30)
    product_entry.grid(row=0, column=1, padx=10, pady=10)

    product_button = cst.CTkButton(root, text='add product',
                                   corner_radius=32, width=10, height=25, command=add_product)
    product_button.grid(row=0, column=3)

    import_button = cst.CTkButton(root, text='import data', corner_radius=32, width=10, height=25,
                                  command=import_data)
    import_button.grid(row=1, column=3, padx=5, pady=5)

    list_frame = tk.Frame(root)
    list_frame.grid(row=2, column=1, padx=10, pady=5, sticky='nsew')

    scrollbar = tk.Scrollbar(list_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    list_prod = tk.Listbox(list_frame, selectmode=tk.EXTENDED,
                           width=50, height=18, yscrollcommand=scrollbar.set)
    list_prod.pack(side=tk.LEFT, fill=tk.BOTH)

    scrollbar.config(command=list_prod.yview)

    delete_button = cst.CTkButton(root, text='delete', corner_radius=32, width=15,
                                  height=30, border_width=2, command=delete_product)
    delete_button.grid(row=5, column=1)

    total_button = cst.CTkButton(root, text='total price', corner_radius=32, width=15, height=30,
                                 command=show_total_price)
    total_button.grid(row=2, column=3)

    root.mainloop()
