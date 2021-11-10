from tkinter import *
from tkinter import ttk
import csv
from tkinter import messagebox
import mysql.connector
from tkinter import colorchooser
from configparser import ConfigParser

root = Tk()
root.title('Rejean Pion - Accounting 2022')
root.iconbitmap('RP.ico')
root.geometry('1000x800')

# Connect to MySQL
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "Mesbusiness@2021",
    database = "accounting",)

# Check to see if connection to MySQL was created
# print(mydb)

# Create a cursor and initialize it
cur = mydb.cursor()

# Create database -- run once
# cur.execute("CREATE DATABASE accounting")

# Test to see if database was created
#cur.execute("SHOW DATABASES")
#for db in cur:
#    print(db)

# Drop the table
# cur.execute("DROP TABLE clients")

# Create a table
def create_table():
    cur.execute("CREATE TABLE IF NOT EXISTS expenses (id INT(10),\
        date VARCHAR(50),\
        detail VARCHAR(255),\
        category VARCHAR(50),\
        subcategory VARCHAR(50),\
        amount INT(10),\
        level VARCHAR(10))")

# show table
'''cur.execute("SELECT * FROM expenses")
print(cur.description)
for item in cur.description:
    print(item)'''

# Import data in a list -- run once to import data
'''with open('expenses.csv', newline='') as file:
    reader = csv.reader(file)
    data = list(reader)

# Import csv Record into the Database -- run once
for item in data:
    print(item)
    cur.execute("INSERT INTO expenses (id, date, detail, category, subcategory, amount, level) VALUES (%s, %s, %s, %s, %s, %s, %s)", (item))
     
# Commit the changes
mydb.commit()'''

# Query the database to see on screen if the data is in our table
def display_database():
    # Clear the Treeview
    for record in my_tree.get_children():
        my_tree.delete(record)

    # Create a database or connect to it
    mydb.connect()

    cur.execute("SELECT * FROM expenses")
    records = cur.fetchall()
    # for record in records:
    #    print(record)

    # Commit the changes
    # mydb.commit()

    # Add our data form records to the screen
    global count
    count = 0

    for record in records:
	    if count % 2 == 0:
		    my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6]), tags=('evenrow',))
	    else:
		    my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6]), tags=('oddrow',))
	    # increment counter
	    count += 1

# Read our config file and get colors
parser = ConfigParser()
parser.read("treebase.ini")
saved_primary_color = parser.get('colors', 'primary_color')
saved_secondary_color = parser.get('colors', 'secondary_color')
saved_highlight_color = parser.get('colors', 'highlight_color')

def primary_color():
    # Pick Color
    primary_color = colorchooser.askcolor()[1]
    # Update Treeview
    if primary_color:
        # Create Stripped Row Tags
        my_tree.tag_configure('evenrow', background=primary_color)

        # Config file
        parser = ConfigParser()
        parser.read("treebase.ini")
        # Set the color change
        parser.set('colors', 'primary_color', primary_color)
        # Save the config file
        with open('treebase.ini', 'w') as configfile:
            parser.write(configfile)

def secondary_color():
    # Pick Color
    secondary_color = colorchooser.askcolor()[1]
    # Update Treeview
    if secondary_color:
        # Create Stripped Row Tags
        my_tree.tag_configure('oddrow', background=secondary_color)

        # Config file
        parser = ConfigParser()
        parser.read("treebase.ini")
        # Set the color change
        parser.set('colors', 'secondary_color', secondary_color)
        # Save the config file
        with open('treebase.ini', 'w') as configfile:
            parser.write(configfile)

def highlight_color():
    # Pick Color
    highlight_color = colorchooser.askcolor()[1]
    # Update Selected Color
    if highlight_color:
        style.map('Treeview',
        background=[('selected', highlight_color)])
        # Config file
        parser = ConfigParser()
        parser.read("treebase.ini")
        # Set the color change
        parser.set('colors', 'highlight_color', highlight_color)
        # Save the config file
        with open('treebase.ini', 'w') as configfile:
            parser.write(configfile)

def default_colors():
    # Reset to original colors
    parser = ConfigParser()
    parser.read("treebase.ini")
    parser.set('colors', 'primary_color', 'lightblue')
    parser.set('colors', 'secondary_color', 'white')
    parser.set('colors', 'highlight_color', '#347083')
    # Save the config file
    with open('treebase.ini', 'w') as configfile:
        parser.write(configfile)
    # Reset the current display
    my_tree.tag_configure('oddrow', background='white')
    my_tree.tag_configure('evenrow', background='lightblue')
    style.map('Treeview',
        background=[('selected', '#347083')])

# Add Menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Configure our Color Menu
option_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Options", menu=option_menu)

# Drop down color menu
option_menu.add_command(label="Primary Color", command=primary_color)
option_menu.add_command(label="Secondary Color", command=secondary_color)
option_menu.add_command(label="Highlight Color", command=highlight_color)
option_menu.add_separator()
option_menu.add_command(label="Default Colors", command=default_colors)
option_menu.add_separator()
option_menu.add_command(label="Exit", command=root.quit)

# Create Functions

# Function to clear the entry boxes
def clear_record():
    id_box.delete(0, END)
    date_box.delete(0, END)
    detail_box.delete(0, END)
    category_box.delete(0, END)
    subcategory_box.delete(0, END)
    amount_box.delete(0, END)
    level_box.delete(0, END)

# Function to Select a Record
def select_record(event):  # Actually that event is just there because the function
    # is looking for it but does not do anything -- could be any word or letter
    
    # Clear entry boxes
    clear_record()
    # Grab record number
    selected = my_tree.focus()
    # Grab record values
    values = my_tree.item(selected, 'values')
    # print(values)

    # Output to entry boxes
    id_box.insert(0, values[0])
    date_box.insert(0, values[1])
    detail_box.insert(0, values[2])  
    category_box.insert(0, values[3]) 
    subcategory_box.insert(0, values[4])
    amount_box.insert(0, values[5])
    level_box.insert(0, values[6])

# Clear the Treeview
def clear_treeview():
    my_tree.delete(*my_tree.get_children())

# Create Bindings Click Function
def clicker(event):
    select_record()

# Add Expense
def add_expense():
    sql_command =f"""INSERT INTO expenses
                 (id, date, detail, category, subcategory, amount, level)
                  VALUES (%s, %s, %s, %s, %s, %s, %s)"""

    cur.execute(sql_command, (id_box.get(), date_box.get(),
                             detail_box.get(), category_box.get(),
                              subcategory_box.get(), amount_box.get(), level_box.get()))

    # Commit the changes to the database
    mydb.commit()
    # Clear the old entry
    clear_record()
    # Refresh the Data Frame
    display_database()

# Edit Expense
def edit_expense():
# Update the Database
    sql_command = f"""UPDATE expenses
                  SET date = %s, detail = %s,
                      category = %s, subcategory = %s,
                      amount = %s, level = %s
                  WHERE id = %s"""

    cur.execute(sql_command, (date_box.get(),
                          detail_box.get(), category_box.get(),
                          subcategory_box.get(), amount_box.get(),
                          level_box.get(), id_box.get()))

    # Commit the changes to the database
    mydb.commit()
    # Clear the old entry
    clear_record()
    # Refresh the Data Frame
    display_database()

# Delete Expense
def delete_expense():
# Delete from Database
    sql_command = f"DELETE FROM expenses WHERE id =" + id_box.get()

    cur.execute(sql_command)
  
    # Commit the changes
    mydb.commit()
    # Clear entry boxes
    clear_record()
    # Refresh the Data Frame
    display_database()
    # Add a little message box
    messagebox.showinfo("Deleted!", "Your Record Has Been Deleted!")

# Delete All Expenses
def delete_all():
# Add a little message box
    response = messagebox.askyesno("WOAH!!!!", "This Will Delete ALL OF YOUR RECORDS!\nAre You Sure?")

    # Add condition on response
    if response == 1:
        # Clear the Treeview
        for record in my_tree.get_children():
            my_tree.delete(record)

        # Delete Everything From The Table
        cur.execute("DROP TABLE expenses")

        # Create a new empty table
        create_table()
        # Commit the changes
        mydb.commit()
        # Clear entry boxes -- just in case
        clear_record()
        # Add a little message box
        messagebox.showinfo("Deleted!", "All of Your Record Has Been Deleted!")

# Search Button
def search_expense():
    # Create the command function to search now 
    def search_now():
        selected = drop.get()
        command = ""
        if selected == "Search by...":
            no_select = Label(button_frame, text="Please select a search category")
            no_select.grid(row=1, column=1, padx=10)
        elif selected == "Date":
            command = "SELECT * FROM expenses WHERE date = %s"
        elif selected == "Detail":
            command = "SELECT * FROM expenses WHERE detail = %s"
        elif selected == "Category":
            command = "SELECT * FROM expenses WHERE category = %s"
        elif selected == "Subcategory":
            command = "SELECT * FROM expenses WHERE subcategory = %s"
        elif selected == "Level":
            command = "SELECT * FROM expenses WHERE level = %s"
        

        search = search_box.get()
        research = (search, )
        result = cur.execute(command, research)
        result = cur.fetchall()

        if not result:
            result_not_found = Label(button_frame, text="Record Not Found...")
            result_not_found.grid(row=1,column=1, padx=10)

        count = 0
        # Clear the Treeview
        for record in my_tree.get_children():
            my_tree.delete(record)
        # Show the result in the Treeview
        for record in result:
	        if count % 2 == 0:
		        my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6]), tags=('evenrow',))
	        else:
		         my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6]), tags=('oddrow',))
	    # increment counter
	        count += 1

    # Create the Search Box
    search_box = Entry(button_frame)
    search_box.grid(row=1, column =1, padx=10)
    # Create a submit button
    submit_button = Button(button_frame, text="Submit", command=search_now)
    submit_button.grid(row=1, column=2, padx=10)
    # Drop Down Box
    drop = ttk.Combobox(button_frame, value=["Search by...", "Date", "Detail", "Category", "Subcategory", "Level"])
    drop.current(0)
    drop.grid(row=1, column=3, padx=10)

# Create a Label
title_label = Label(root, text="ACCOUNTING", font=('Helvetica', 16))
title_label.pack(fill="x", expand="yes", padx=20)

# Add Some Style
style = ttk.Style()

# Pick a Theme
style.theme_use("default")   

# create a notebook
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

# create frames
spa_frame = ttk.Frame(notebook, width=900, height=750)
expenses_frame = ttk.Frame(notebook, width=900, height=750)
revenues_frame = ttk.Frame(notebook, width=900, height=750)
budget_frame = ttk.Frame(notebook, width=900, height=750)

spa_frame.pack(fill='both', expand=True)
expenses_frame.pack(fill='both', expand=True)
revenues_frame.pack(fill='both', expand=True)
budget_frame.pack(fill='both', expand=True)

# add frames to notebook
notebook.add(spa_frame, text='Spa Activities')
notebook.add(expenses_frame, text='Expenses')
notebook.add(revenues_frame, text='Revenues')
notebook.add(budget_frame, text='Budget')

# Configure the Treeview Colors
style.configure("Treeview", 
    background="white",
    foreground="black",
    rowheight=25,
    fieldbackground="white")

# Change Selected Color #347083
style.map('Treeview',
    background=[('selected', saved_highlight_color)])

# Create an Expenses Treeview Frame
tree_frame = Frame(expenses_frame)
tree_frame.pack(pady=10)

# Create a Treeview  Yaxis Scrollbar
tree_scroll_Y = Scrollbar(tree_frame)
tree_scroll_Y.pack(side=RIGHT, fill=Y)

# Create a Treeview  Xaxis Scrollbar
tree_scroll_X = Scrollbar(tree_frame, orient = HORIZONTAL)
tree_scroll_X.pack(side=BOTTOM, fill=X)

# Create the Treeview
my_tree = ttk.Treeview(tree_frame, xscrollcommand=tree_scroll_X.set, yscrollcommand=tree_scroll_Y.set, selectmode="extended")
my_tree.pack()

# Configure the Scroolbars
tree_scroll_Y.config(command=my_tree.yview)
tree_scroll_X.config(command=my_tree.xview)

# Define Our Columns
my_tree['columns'] = ("ID", "Date", "Detail", "Category", "Subcategory", "Amount", "Level")

# Format Our Columns
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("ID", anchor=W, width=40)
my_tree.column("Date", anchor=W, width=140)
my_tree.column("Detail", anchor=W, width=160)
my_tree.column("Category", anchor=CENTER, width=160)
my_tree.column("Subcategory", anchor=CENTER, width=160)
my_tree.column("Amount", anchor=CENTER, width=100)
my_tree.column("Level", anchor=CENTER, width=60)


# Create Headings
my_tree.heading("#0", text="", anchor=W)
my_tree.heading("ID", text="ID", anchor=W)
my_tree.heading("Date", text="Date", anchor=W)
my_tree.heading("Detail", text="Detail", anchor=W)
my_tree.heading("Category", text="Category", anchor=CENTER)
my_tree.heading("Subcategory", text="Subcategory", anchor=CENTER)
my_tree.heading("Amount", text="Amount", anchor=CENTER)
my_tree.heading("Level", text="Level", anchor=CENTER)


# Create Stripped Row Tags
my_tree.tag_configure('oddrow', background=saved_secondary_color)
my_tree.tag_configure('evenrow', background=saved_primary_color)

# Add Record Entry Boxes
data_frame = LabelFrame(expenses_frame, text="Record")
data_frame.pack(fill="both", expand="yes", padx=20)

# Create Main Form To Enter Clients Data
id_label = Label(data_frame, text="ID").grid(row=0, column =0, sticky=W, padx=10)
date_label = Label(data_frame, text="Date").grid(row=0, column =1, sticky=W, padx=10)
detail_label = Label(data_frame, text="Detail").grid(row=0, column =2, sticky=W, padx=10)
category_label = Label(data_frame, text="Category").grid(row=0, column =3, sticky=W, padx=10)
subcategory_label = Label(data_frame, text="Subcategory").grid(row=0, column =4, sticky=W, padx=10)
amount_label = Label(data_frame, text="Amount").grid(row=2, column =1, sticky=W, padx=10)
level_label = Label(data_frame, text="Level").grid(row=2, column =2, sticky=W, padx=10)

# Create Empty Boxes
id_box = Entry(data_frame)
id_box.grid(row=1, column =0, padx=10)
date_box = Entry(data_frame)
date_box.grid(row=1, column =1, padx=10)
detail_box = Entry(data_frame)
detail_box.grid(row=1, column =2, padx=10)
category_box = Entry(data_frame)
category_box.grid(row=1, column =3, padx=10)
subcategory_box = Entry(data_frame)
subcategory_box.grid(row=1, column =4, padx=10)
amount_box = Entry(data_frame)
amount_box.grid(row=3, column =1, padx=10)
level_box = Entry(data_frame)
level_box.grid(row=3, column =2, padx=10)


# Create Buttons
# Create a Button Frame
button_frame = LabelFrame(expenses_frame, text="Search")
button_frame.pack(fill="x", expand="yes", padx=20)
# Add Button
add_expense_button = Button(data_frame, text="Add Expense", command=add_expense)
add_expense_button.grid(row=4, column=0, padx=10, pady=10)
# Delete Button
delete_expense_button = Button(data_frame, text="Delete Expense", command=delete_expense)
delete_expense_button.grid(row=4, column=2, padx=10, pady=10)
# Delete All Button
delete_all_expenses_button = Button(data_frame, text="Delete All Expenses", command=delete_all)
delete_all_expenses_button.grid(row=4, column=3, padx=10, pady=10)
# Clear Record Button
clear_record_button = Button(data_frame, text="Clear Record", command=clear_record)
clear_record_button.grid(row=3, column=0, padx=10, pady=10)
# Search Button
search_button = Button(button_frame, text="Search",command=search_expense)
search_button.grid(row=1, column=0, padx=10, pady=10)
# Edit Button
edit_expense_button = Button(data_frame, text="Edit Expense", command=edit_expense)
edit_expense_button.grid(row=4, column=1, padx=10, pady=10)
# Reset Treeview Button
reset_treeview_button = Button(button_frame, text="Reset Treeview", command=display_database)
reset_treeview_button.grid(row=1, column=4, padx=10, pady=10)

# Bind the Treeview
my_tree.bind("<ButtonRelease-1>", select_record)

# Run the Database form the start
create_table()
display_database()

root.mainloop()