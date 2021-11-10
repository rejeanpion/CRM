from tkinter import *
from tkinter import ttk
import csv
from tkinter import messagebox
import mysql.connector
from tkinter import colorchooser
from configparser import ConfigParser

root = Tk()
root.title('Rejean Pion - CRM Template')
root.iconbitmap('RP_Logo.ico')
root.geometry('1200x800')

# Connect to MySQL
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "Mesbusiness@2021",
    database = "template",)

# Check to see if connection to MySQL was created
# print(mydb)

# Create a cursor and initialize it
cur = mydb.cursor()

# Create database -- run once
# cur.execute("CREATE DATABASE template")

# Test to see if database was created
#cur.execute("SHOW DATABASES")
#for db in cur:
#    print(db)

# Drop the table
# cur.execute("DROP TABLE clients")

# Create a table
def create_table():
    cur.execute("CREATE TABLE IF NOT EXISTS clients (user_id INT AUTO_INCREMENT PRIMARY KEY,\
        f_name VARCHAR(255),\
        l_name VARCHAR(255),\
        email VARCHAR(255),\
        phone VARCHAR(255),\
        price INT(10),\
        address VARCHAR(255),\
        city VARCHAR(50),\
        state VARCHAR(50),\
        country VARCHAR(255),\
        zipcode INT(10))")

# show table
'''cur.execute("SELECT * FROM clients")
print(cur.description)
for item in cur.description:
    print(item)'''

# Import data in a list -- run once to import data
'''with open('crm_data.csv', newline='') as file:
    reader = csv.reader(file)
    data = list(reader)
#for item in data:
    #print(item)

# Import csv Record into the Database -- run once
for item in data:
    print(item)
    cur.execute("INSERT INTO clients (user_id, f_name, l_name, email, phone, price, address, city, state, country, zipcode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (item))
    # cur.execute("INSERT INTO clients (f_name, l_name, email, phone, price, address, city, state, country, zipcode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (item))
     
 # Commit the changes
mydb.commit()'''

# Query the database to see on screen if the data is in our table
def query_database():
    # Clear the Treeview
    for record in my_tree.get_children():
        my_tree.delete(record)

    # Create a database or connect to it
    mydb.connect()

    cur.execute("SELECT * FROM clients")
    records = cur.fetchall()
    #for record in records:
    #    print(record)

    # Commit the changes
    # mydb.commit()

    # Add our data form records to the screen
    global count
    count = 0

    for record in records:
	    if count % 2 == 0:
		    my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9], record[10]), tags=('evenrow',))
	    else:
		    my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9], record[10]), tags=('oddrow',))
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

# Functions

# Function to clear the entry boxes
def clear_record():
    user_id_box.delete(0, END)
    f_name_box.delete(0, END)
    l_name_box.delete(0, END)
    email_box.delete(0, END)
    phone_box.delete(0, END)
    price_box.delete(0, END)
    address_box.delete(0, END)
    city_box.delete(0, END)
    state_box.delete(0, END)
    country_box.delete(0, END)
    zipcode_box.delete(0, END)

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
    user_id_box.insert(0, values[0])
    f_name_box.insert(0, values[1])
    l_name_box.insert(0, values[2])   
    email_box.insert(0, values[3])
    phone_box.insert(0, values[4])
    price_box.insert(0, values[5])
    address_box.insert(0, values[6])
    city_box.insert(0, values[7])
    state_box.insert(0, values[8])
    country_box.insert(0, values[9])
    zipcode_box.insert(0, values[10])

# Clear the Treeview
def clear_treeview():
    my_tree.delete(*my_tree.get_children())

# Create Bindings Click Function
def clicker(event):
    select_record()


# Function to add a Record to the Database
def add_client():
    sql_command ="INSERT INTO clients (f_name, l_name, email, phone, price, address, city, state, country, zipcode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (f_name_box.get(), l_name_box.get(), email_box.get(), phone_box.get(), price_box.get(), address_box.get(), city_box.get(), state_box.get(), country_box.get(), zipcode_box.get())
    cur.execute(sql_command, values)

    # Commit the changes to the database
    mydb.commit()
    # Clear the old entry
    clear_record()
    # Refresh the Data Frame
    query_database()

# Function to Edit Record 
def edit_client():
# Update the Database
    sql_command = f"""UPDATE clients
                  SET f_name = %s, l_name = %s,
                      email = %s, phone = %s,
                      price = %s, address = %s,
                      city = %s, state = %s,
                      country = %s, zipcode = %s
                  WHERE user_id = %s"""

    cur.execute(sql_command, (f_name_box.get(), l_name_box.get(),
                          email_box.get(), phone_box.get(),
                          price_box.get(), address_box.get(),
                          city_box.get(), state_box.get(),
                          country_box.get(), zipcode_box.get(),
                          user_id_box.get()))

    # Commit the changes to the database
    mydb.commit()
    # Clear the old entry
    clear_record()
    # Refresh the Data Frame
    query_database()

# Function to delete on client
def delete_client():    
# Delete from Database
    sql_command = f"DELETE FROM clients WHERE user_id =" + user_id_box.get()

    cur.execute(sql_command)
  
    # Commit the changes
    mydb.commit()
    # Clear entry boxes
    clear_record()
    # Refresh the Data Frame
    query_database()
    # Add a little message box
    messagebox.showinfo("Deleted!", "Your Record Has Been Deleted!")

def delete_all():
    # Add a little message box
    response = messagebox.askyesno("WOAH!!!!", "This Will Delete ALL OF YOUR RECORDS!\nAre You Sure?")

    # Add condition on response
    if response == 1:
        # Clear the Treeview
        for record in my_tree.get_children():
            my_tree.delete(record)

        # Delete Everything From The Table
        cur.execute("DROP TABLE clients")

        # Create a new empty table
        create_table()
        # Commit the changes
        mydb.commit()
        # Clear entry boxes -- just in case
        clear_record()
        # Add a little message box
        messagebox.showinfo("Deleted!", "All of Your Record Has Been Deleted!")


# Create the search function
def search_client():
    # Create the command function to search now 
    def search_now():
        selected = drop.get()
        command = ""
        if selected == "Search by...":
            no_select = Label(button_frame, text="Please select a search category")
            no_select.grid(row=1, column=1, padx=10)
        elif selected == "First Name":
            command = "SELECT * FROM clients WHERE f_name = %s"
        elif selected == "Last Name":
            command = "SELECT * FROM clients WHERE l_name = %s"
        elif selected == "Email":
            command = "SELECT * FROM clients WHERE email = %s"
        elif selected == "Price":
            command = "SELECT * FROM clients WHERE price = %s"
        elif selected == "City":
            command = "SELECT * FROM clients WHERE city = %s"
        elif selected == "State":
            command = "SELECT * FROM clients WHERE state = %s"
        elif selected == "Country":
            command = "SELECT * FROM clients WHERE country = %s"

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
		        my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9], record[10]), tags=('evenrow',))
	        else:
		         my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9], record[10]), tags=('oddrow',))
	    # increment counter
	        count += 1

    # Create the Search Box
    search_box = Entry(button_frame)
    search_box.grid(row=1, column =1, padx=10)
    # Create a submit button
    submit_button = Button(button_frame, text="Submit", command=search_now)
    submit_button.grid(row=1, column=2, padx=10)
    # Drop Down Box
    drop = ttk.Combobox(button_frame, value=["Search by...", "First Name", "Last Name", "Email", "Price", "City", "State", "Country"])
    drop.current(0)
    drop.grid(row=1, column=3, padx=10)

# Create a Label
title_label = Label(root, text="CRM template", font=('Helvetica', 16))
title_label.pack(fill="x", expand="yes", padx=20)

# Add Some Style
style = ttk.Style()

# Pick a Theme
style.theme_use("default")   

# Configure the Treeview Colors
style.configure("Treeview", 
    background="white",
    foreground="black",
    rowheight=25,
    fieldbackground="white")

# Change Selected Color #347083
style.map('Treeview',
    background=[('selected', saved_highlight_color)])

# Create a Treeview Frame
tree_frame = Frame(root)
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
my_tree['columns'] = ("ID", "First Name", "Last Name", "Email", "Phone", "Price", "Address", "City", "State", "Country", "Zipcode")

# Format Our Columns
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("ID", anchor=W, width=80)
my_tree.column("First Name", anchor=W, width=140)
my_tree.column("Last Name", anchor=W, width=140)
my_tree.column("Email", anchor=CENTER, width=140)
my_tree.column("Phone", anchor=CENTER, width=140)
my_tree.column("Price", anchor=CENTER, width=140)
my_tree.column("Address", anchor=CENTER, width=140)
my_tree.column("City", anchor=CENTER, width=140)
my_tree.column("State", anchor=CENTER, width=140)
my_tree.column("Country", anchor=CENTER, width=140)
my_tree.column("Zipcode", anchor=CENTER, width=140)

# Create Headings
my_tree.heading("#0", text="", anchor=W)
my_tree.heading("ID", text="ID", anchor=W)
my_tree.heading("First Name", text="First Name", anchor=W)
my_tree.heading("Last Name", text="Last Name", anchor=W)
my_tree.heading("Email", text="Email", anchor=CENTER)
my_tree.heading("Phone", text="Phone", anchor=CENTER)
my_tree.heading("Price", text="Price", anchor=CENTER)
my_tree.heading("Address", text="Address", anchor=CENTER)
my_tree.heading("City", text="City", anchor=CENTER)
my_tree.heading("State", text="State", anchor=CENTER)
my_tree.heading("Country", text="Country", anchor=CENTER)
my_tree.heading("Zipcode", text="Zipcode", anchor=CENTER)

# Create Stripped Row Tags
my_tree.tag_configure('oddrow', background=saved_secondary_color)
my_tree.tag_configure('evenrow', background=saved_primary_color)

# Add Record Entry Boxes
data_frame = LabelFrame(root, text="Record")
data_frame.pack(fill="both", expand="yes", padx=20)

# Create Main Form To Enter Clients Data
user_id_label = Label(data_frame, text="User ID").grid(row=1, column =0, sticky=W, padx=10)
f_name_label = Label(data_frame, text="First Name").grid(row=1, column =1, sticky=W, padx=10)
l_name_label = Label(data_frame, text="Last Name").grid(row=1, column =2, sticky=W, padx=10)
email_label = Label(data_frame, text="Email").grid(row=1, column =3, sticky=W, padx=10)
phone_label = Label(data_frame, text="Phone").grid(row=1, column =4, sticky=W, padx=10)
price_label = Label(data_frame, text="Price").grid(row=1, column =5, sticky=W, padx=10)
address_label = Label(data_frame, text="Address").grid(row=3, column =0, sticky=W, padx=10)
city_label = Label(data_frame, text="City").grid(row=3, column =1, sticky=W, padx=10)
state_label = Label(data_frame, text="State").grid(row=3, column =2, sticky=W, padx=10)
country_label = Label(data_frame, text="Country").grid(row=3, column =3, sticky=W, padx=10)
zipcode_label = Label(data_frame, text="Zipcode").grid(row=3, column =4, sticky=W, padx=10)


# Create Empty Boxes
user_id_box = Entry(data_frame)
user_id_box.grid(row=2, column =0, padx=10)
f_name_box = Entry(data_frame)
f_name_box.grid(row=2, column =1, padx=10)
l_name_box = Entry(data_frame)
l_name_box.grid(row=2, column =2, padx=10)
email_box = Entry(data_frame)
email_box.grid(row=2, column =3, padx=10)
phone_box = Entry(data_frame)
phone_box.grid(row=2, column =4, padx=10)
price_box = Entry(data_frame)
price_box.grid(row=2, column =5, padx=10)
address_box = Entry(data_frame)
address_box.grid(row=4, column =0, padx=10)
city_box = Entry(data_frame)
city_box.grid(row=4, column =1, padx=10)
state_box = Entry(data_frame)
state_box.grid(row=4, column =2, padx=10)
country_box = Entry(data_frame)
country_box.grid(row=4, column =3, padx=10)
zipcode_box = Entry(data_frame)
zipcode_box.grid(row=4, column =4, padx=10)

# Create Buttons
# Create a Button Frame
button_frame = LabelFrame(root, text="Functions")
button_frame.pack(fill="x", expand="yes", padx=20)
# Add Button
add_client_button = Button(button_frame, text="Add Client", command=add_client)
add_client_button.grid(row=0, column=0, padx=10, pady=10)
# Delete Button
delete_client_button = Button(button_frame, text="Delete Client", command=delete_client)
delete_client_button.grid(row=0, column=1, padx=10, pady=10)
# Delete All Button
delete_all_client_button = Button(button_frame, text="Delete All Clients", command=delete_all)
delete_all_client_button.grid(row=0, column=2, padx=10, pady=10)
# Clear Record Button
clear_record_button = Button(button_frame, text="Clear Record", command=clear_record)
clear_record_button.grid(row=0, column=3, padx=10, pady=10)
# Search Button
search_button = Button(button_frame, text="Search",command=search_client)
search_button.grid(row=1, column=0, padx=10, pady=10)
# Edit Button
edit_client_button = Button(button_frame, text="Edit Client", command=edit_client)
edit_client_button.grid(row=0, column=4, padx=10, pady=10)
# Reset Treeview Button
reset_treeview_button = Button(button_frame, text="Reset Treeview", command=query_database)
reset_treeview_button.grid(row=1, column=4, padx=10, pady=10)

# Bind the Treeview
my_tree.bind("<ButtonRelease-1>", select_record)

# Run the Database form the start
create_table()
query_database()

root.mainloop()