from tkinter import *
from tkinter import ttk
import tkinter as tk
import csv
from tkinter import messagebox
import mysql.connector
from tkinter import colorchooser
from configparser import ConfigParser

# root window
root = tk.Tk()
root.geometry('800x500')
root.title('Accounting Demo')
root.iconbitmap('RP.ico')

# create a notebook
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

# create frames
frame1 = ttk.Frame(notebook, width=700, height=480)
frame2 = ttk.Frame(notebook, width=700, height=480)
frame3 = ttk.Frame(notebook, width=700, height=480)

frame1.pack(fill='both', expand=True)
frame2.pack(fill='both', expand=True)
frame3.pack(fill='both', expand=True)

# add frames to notebook

notebook.add(frame1, text='Spa Activities')
notebook.add(frame2, text='Expenses')
notebook.add(frame3, text='Budget')


# Creating a list of Expenses Categories
categories = ["Choose a category...", "ADVERTISEMENT", "DONATION", "ELECTRICITY", "ENTERTAINMENT", "EQUIPMENT",
                 "FEES", "FOOD", "FURNITURE", "GIFT", "HEALTH", "INTERNET", "LEARNING", "LOAN",
                 "MAINTENANCE", "MATERIAL", "PHONE", "PRODUCT", "RENT",
                 "SALARY", "TRANSFER", "TRANSPORT", "WATER", "WORKER"]

advertisement_cat = ["Choose a subcategory...", "SPA BANNER", "SPA FLYER", "TIA PROPERTY"]

donation_cat = ["Choose a subcategory...", "CHURCH","FUNERAL", "NIEPI"]

electricity_cat = ["Choose a subcategory...", "ELECTRICITY HOUSE", "ELECTRICITY KOS", "ELECTRICITY SPA"]

entertainment_cat = ["Choose a subcategory...", "MOVIE", "STEAM", "YOUTUBE"]

equipment_cat = ["Choose a subcategory...", "COMPUTER", "ELECTRONIC", "MATERIAL",  "PHONE", "SPA EQUIPMENT"]

fees_cat = ["Choose a subcategory...", "ADMIN FEES", "BANK FEES"]

food_cat = ["Choose a subcategory...", "ALCOOL", "FOOD", "GAZ", "RESTAURANT"]

furniture_cat = ["Choose a subcategory...", "A/C"]

gift_cat = ["Choose a subcategory...", "FAMILY"]

health_cat = ["Choose a subcategory...", "DENTIST", "EQUIPMENT", "EXERCICE", "INSURANCE", "MEDECINE", "TEST"]

internet_cat = ["Choose a subcategory...", "INTERNET KOS", "INTERNET HOUSE", "INTERNET SPA"]

learning_cat = ["Choose a subcategory...", "BOOK", "ONLINE COURSE"]

loan_cat = ["Choose a subcategory...", "LOAN", "PCX", "SCOOPY", "OTHER"]

maintenance_cat = ["Choose a subcategory...", "A/C", "ELECTRICS", "ELECTRONICS", "GAZ", "MATERIAL", "MOTORBIKE", 
                    "WORKER"]

material_cat = ["Choose a subcategory...", "HOUSE MATERIAL", "SPA MATERIAL"]

phone_cat = ["Choose a subcategory...", "PHONE", "PULSA", "REPAIR"]

product_cat = ["Choose a subcategory...", "OFFICE PRODUCT", "SALON PRODUCT", "SPA PRODUCT"]

rent_cat = ["Choose a subcategory...", "RENT HOUSE", "RENT KOS", "RENT SPA"]

salary_cat = ["Choose a subcategory...", "SALARY SPA"]

transfer_cat = ["Choose a subcategory...", "GO-PAY", "GOOGLE PLAY", "MONEY"]

transport_cat = ["Choose a subcategory...", "CLEANING", "LICENCE", "MOTORBIKE REPAIR", "PETROL", "TAXI"]

water_cat = ["Choose a subcategory...", "KOS WATER", "HOUSE WATER", "SPA WATER", "DRINKING WATER"]

workers_cat = ["Choose a subcategory...", "HOUSE", "SPA"]

# Create a box for sub categories
def sub_cat(event):
    choice = cat_box.get()

    if choice == "ADVERTISEMENT":
        sub_box.config(value=advertisement_cat)
        sub_box.current(0)
    if choice == "DONATION":
        sub_box.config(value=donation_cat)
        sub_box.current(0)
    elif choice == "ELECTRICITY":
        sub_box.config(value=electricity_cat)
        sub_box.current(0)
    elif choice == "ENTERTAINMENT":
        sub_box.config(value=entertainment_cat)
        sub_box.current(0)
    elif choice == "EQUIPMENT":
        sub_box.config(value=equipment_cat)
        sub_box.current(0)
    elif choice == "FEES":
        sub_box.config(value=fees_cat)
        sub_box.current(0) 
    elif choice == "FOOD":
        sub_box.config(value=food_cat)
        sub_box.current(0)
    elif choice == "FURNITURE":
        sub_box.config(value=furniture_cat)
        sub_box.current(0)
    elif choice == "GIFT":
        sub_box.config(value=gift_cat)
        sub_box.current(0)
    elif choice == "HEALTH":
        sub_box.config(value=health_cat)
        sub_box.current(0)
    elif choice == "INTERNET":
        sub_box.config(value=internet_cat)
        sub_box.current(0)
    elif choice == "LEARNING":
        sub_box.config(value=learning_cat)
        sub_box.current(0)
    elif choice == "LOAN":
        sub_box.config(value=loan_cat)
        sub_box.current(0)
    elif choice == "MAINTENANCE":
        sub_box.config(value=maintenance_cat)
        sub_box.current(0)
    elif choice == "MATERIAL":
        sub_box.config(value=material_cat)
        sub_box.current(0)
    elif choice == "PHONE":
        sub_box.config(value=phone_cat)
        sub_box.current(0)
    elif choice == "PRODUCT":
        sub_box.config(value=product_cat)
        sub_box.current(0)
    elif choice == "RENT":
        sub_box.config(value=rent_cat)
        sub_box.current(0)
    elif choice == "SALARY":
        sub_box.config(value=salary_cat)
        sub_box.current(0)
    elif choice == "TRANSFER":
        sub_box.config(value=transfer_cat)
        sub_box.current(0)
    elif choice == "TRANSPORT":
        sub_box.config(value=transport_cat)
        sub_box.current(0)
    elif choice == "WATER":
        sub_box.config(value=water_cat)
        sub_box.current(0)
    elif choice == "WORKER":
        sub_box.config(value=workers_cat)
        sub_box.current(0)

# Create a drop box for main categories
cat_box = ttk.Combobox(frame2, value=categories)
cat_box.pack(pady=20)
cat_box.current(0)
# Bind the combobox
cat_box.bind("<<ComboboxSelected>>", sub_cat)

# Create a drop box for main sub categories
sub_box = ttk.Combobox(frame2, value=[" "])
sub_box.pack(pady=20)
sub_box.current(0)




root.mainloop()