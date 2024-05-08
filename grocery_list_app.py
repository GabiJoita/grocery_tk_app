""" Use this app to add you favourite products on a grocery list"""

import tkinter as tk
import csv
import pandas as pd
import customtkinter as cst
from customtkinter import *
from tkinter import messagebox
from list_data import MyDbList


def add_product():
    """ create a function to put products
        inside your listbox, manually,
        than save the list in a csv file
     """
    product = product_entry.get()
    price = price_entry.get()
    list_prod.insert(tk.END, f'{product} {price} lei')
    product_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    if product:
        with open('grocery_list.csv', 'a', newline="") as fr:
            writer = csv.writer(fr)
            writer.writerow([product, price])
    else:
        messagebox.showerror(message='please, enter a product')


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


def prod_categories():
    categories = []
    for item in list_prod.get(0, tk.END):
        data = item.split()
        data_cat = {
            'id': data[0],
            'name': data[1],
            'category': data[2],
            'price': float(data[3]),
            'value': data[4]
        }
        categories.append(data_cat)
    df_cat = pd.DataFrame(categories)
    print(df_cat.groupby('category'))
    return df_cat.groupby('category')


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


def show_categories():
    s_cat = prod_categories()
    price_cat = ''
    for cat in s_cat:
        price_cat += f"{cat[0]}: {cat[1]['price'].sum()}\n"
        print(cat[1])
    top = tk.Toplevel()
    top.configure(bg='#857EFF')
    top.geometry('200x100')
    label = tk.Label(top, text='', textvariable=index, bg='#857EFF')
    label.pack()
    index.set(price_cat)


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

    product_entry = CTkEntry(root, width=200)
    product_entry.grid(row=0, column=1, padx=10, pady=10)

    price_text = tk.Label(root, text='enter a price:', background='#1B0A6B', foreground='white')
    price_text.grid(row=1, column=0, padx=10, pady=10)

    price_entry = CTkEntry(root, width=200)
    price_entry.grid(row=1, column=1, padx=10, pady=10)

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

    list_prod = tk.Listbox(list_frame, bg="#383838", fg="#56F203", selectmode=tk.EXTENDED,
                           width=50, height=18, yscrollcommand=scrollbar.set)
    list_prod.pack(side=tk.LEFT, fill=tk.BOTH)

    scrollbar.config(command=list_prod.yview)

    delete_button = cst.CTkButton(root, text='delete', corner_radius=32, width=15,
                                  height=30, border_width=2, command=delete_product)
    delete_button.grid(row=5, column=1)

    total_button = cst.CTkButton(root, text='total price', corner_radius=32, width=15, height=30,
                                 command=show_total_price)
    total_button.grid(row=2, column=3)

    categories_button = cst.CTkButton(root, text='show categories', corner_radius=32, width=15, height=30,
                                      command=show_categories)
    categories_button.grid(row=3, column=3)

    root.mainloop()
