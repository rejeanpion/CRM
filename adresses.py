from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from tkinter import colorchooser
from configparser import ConfigParser

root = Tk()
root.title('TreeView Database Template')
root.iconbitmap('RP_Logo.ico')
root.geometry("1100x650")

# Query the database to see on screen if the data is in our table
def query_database():
    # Clear the Treeview
    for record in my_tree.get_children():
        my_tree.delete(record)

    # Create a database or connect to it
    conn = sqlite3.connect('addresses_crm.db')

    # Create a cursor instance
    cur = conn.cursor()

    cur.execute("SELECT rowid, * FROM addresses")
    records = cur.fetchall()
    # print(records)

    # Add our data form records to the screen
    global count
    count = 0

    for record in records:
	    if count % 2 == 0:
		    my_tree.insert(parent='', index='end', iid=count, text='', values=(record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8]), tags=('evenrow',))
	    else:
		    my_tree.insert(parent='', index='end', iid=count, text='', values=(record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8]), tags=('oddrow',))
	    # increment counter
	    count += 1

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()

# Read our config file and get colors
parser = ConfigParser()
parser.read("treebase.ini")
saved_primary_color = parser.get('colors', 'primary_color')
saved_secondary_color = parser.get('colors', 'secondary_color')
saved_highlight_color = parser.get('colors', 'highlight_color')

def search_records():
    lookup_record = search_entry.get()
    # close the search box
    search.destroy()

    # Clear the Treeview
    for record in my_tree.get_children():
        my_tree.delete(record)
    
    # Create a database or connect to it
    conn = sqlite3.connect('addresses_crm.db')

    # Create a cursor instance
    cur = conn.cursor()

    cur.execute("SELECT rowid, * FROM addresses WHERE l_name like ?", (lookup_record,))
    records = cur.fetchall()
 
    # Add our data form records to the screen
    global count
    count = 0

    for record in records:
	    if count % 2 == 0:
		    my_tree.insert(parent='', index='end', iid=count, text='', values=(record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8]), tags=('evenrow',))
	    else:
		    my_tree.insert(parent='', index='end', iid=count, text='', values=(record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8]), tags=('oddrow',))
	    # increment counter
	    count += 1

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()



def lookup_records():
    global search_entry, search
    search = Toplevel(root)
    search.title("Lookup Records")
    search.geometry("400x200")
    search.iconbitmap('RP_Logo.ico')

    # Create label frame
    search_frame = LabelFrame(search, text="Last Name")
    search_frame.pack(padx=10, pady=10)

    # Add entry box
    search_entry = Entry(search_frame, font=("Helvetica", 18))
    search_entry.pack(padx=20, pady=20)

    # Add button
    search_button = Button(search, text="Search Records", command=search_records)
    search_button.pack(padx=20, pady=20)

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

# Search Menu
search_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Search", menu=search_menu)
# Drop down search menu
search_menu.add_command(label="Search", command=lookup_records)
search_menu.add_separator()
search_menu.add_command(label="Reset", command=query_database)

'''# Add Fake Data
data = [
    [1, "John", "Elder", "123 Elder St.", "Las Vegas", "NV", "US", "89137"],
	[2, "Mary", "Smith", "435 West Lookout", "Chicago", "IL", "US", "60610"],
	[3, "Tim", "Tanaka", "246 Main St.", "New York", "NY", "US", "12345"],
	[4, "Erin", "Erinton", "333 Top Way.", "Los Angeles", "CA", "US", "90210"],
	[5, "Bob", "Bobberly", "876 Left St.", "Memphis", "TN", "US", "34321"],
	[6, "Steve", "Smith", "1234 Main St.", "Miami", "FL", "US", "12321"],
	[7, "Tina", "Browne", "654 Street Ave.", "Chicago", "IL", "US", "60611"],
	[8, "Mark", "Lane", "12 East St.", "Nashville", "TN", "US", "54345"],
	[9, "John", "Smith", "678 North Ave.", "St. Louis", "MO", "US", "67821"],
	[10, "Mary", "Todd", "9 Elder Way.", "Dallas", "TX", "US", "88948"],
	[11, "John", "Lincoln", "123 Elder St.", "Las Vegas", "NV", "US", "89137"],
	[12, "Mary", "Bush", "435 West Lookout", "Chicago", "IL", "US", "60610"],
	[13, "Tim", "Reagan", "246 Main St.", "New York", "NY", "US", "12345"],
	[14, "Erin", "Smith", "333 Top Way.", "Los Angeles", "CA", "US", "90210"],
	[15, "Bob", "Field", "876 Left St.", "Memphis", "TN", "US", "34321"],
	[16, "Steve", "Target", "1234 Main St.", "Miami", "FL", "US", "12321"],
	[17, "Tina", "Walton", "654 Street Ave.", "Chicago", "IL", "US", "60611"],
	[18, "Mark", "Erendale", "12 East St.", "Nashville", "TN", "US", "54345"],
	[19, "John", "Nowerton", "678 North Ave.", "St. Louis", "MO", "US", "67821"],
	[20, "Mary", "Hornblower", "9 Elder Way.", "Dallas", "TX", "US", "88948"]
]'''


# Create a database or connect to it
conn = sqlite3.connect('addresses_crm.db')
# Create a cursor instance
cur = conn.cursor()

# Create a table -- if not exists
def create_table():
    cur.execute("""CREATE TABLE if not exists addresses (
        id Integer,
        f_name TEXT,
        l_name TEXT,
        address TEXT,
        city TEXT,
        state TEXT,
        country TEXT,
        zipcode TEXT)
        """)

# Create the first table
create_table()
# Commit the changes
conn.commit()
# Close the connection  
conn.close()

# Add dummy data to the table -- only one time
# Create a database or connect to it
conn = sqlite3.connect('addresses_crm.db')
# Create a cursor instance
cur = conn.cursor()

'''for record in data:
    print(record)
    cur.execute("INSERT INTO addresses VALUES (:id, :f_name, :l_name, :address, :city, :state, :country, :zipcode)", 
        {
        'id': record[0],
        'f_name': record[1],
        'l_name': record[2],      
        'address': record[3],
        'city': record[4],
        'state': record[5],
        'country': record[6],
        'zipcode': record[7]
        }
        )
 # Commit the changes
conn.commit()
# Close the connection
conn.close()'''

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

# Change Selected Color
style.map('Treeview',
    background=[('selected', saved_highlight_color)])

# Create a Treeview Frame
tree_frame = Frame(root)
tree_frame.pack(pady=10)

# Create a Treeview Scrollbar
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

# Create the Treeview
my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
my_tree.pack()

# Configure the Scroolbar
tree_scroll.config(command=my_tree.yview)

# Define Our Columns
my_tree['columns'] = ("ID", "First Name", "Last Name", "Address", "City", "State", "Country", "Zipcode")

# Format Our Columns
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("ID", anchor=CENTER, width=80)
my_tree.column("First Name", anchor=W, width=140)
my_tree.column("Last Name", anchor=W, width=140)
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
data_frame.pack(fill="x", expand="yes", padx=20)

id_label = Label(data_frame, text="ID")
id_label.grid(row=0, column=0, padx=10, pady=10)
id_entry = Entry(data_frame)
id_entry.grid(row=0, column=1, padx=10, pady=10)

fn_label = Label(data_frame, text="First Name")
fn_label.grid(row=0, column=2, padx=10, pady=10)
fn_entry = Entry(data_frame)
fn_entry.grid(row=0, column=3, padx=10, pady=10)

ln_label = Label(data_frame, text="Last Name")
ln_label.grid(row=0, column=4, padx=10, pady=10)
ln_entry = Entry(data_frame)
ln_entry.grid(row=0, column=5, padx=10, pady=10)

address_label = Label(data_frame, text="Address")
address_label.grid(row=0, column=6, padx=10, pady=10)
address_entry = Entry(data_frame)
address_entry.grid(row=0, column=7, padx=10, pady=10)

city_label = Label(data_frame, text="City")
city_label.grid(row=1, column=0, padx=10, pady=10)
city_entry = Entry(data_frame)
city_entry.grid(row=1, column=1, padx=10, pady=10)

state_label = Label(data_frame, text="State")
state_label.grid(row=1, column=2, padx=10, pady=10)
state_entry = Entry(data_frame)
state_entry.grid(row=1, column=3, padx=10, pady=10)

country_label = Label(data_frame, text="Country")
country_label.grid(row=1, column=4, padx=10, pady=10)
country_entry = Entry(data_frame)
country_entry.grid(row=1, column=5, padx=10, pady=10)

zipcode_label = Label(data_frame, text="Zipcode")
zipcode_label.grid(row=1, column=6, padx=10, pady=10)
zipcode_entry = Entry(data_frame)
zipcode_entry.grid(row=1, column=7, padx=10, pady=10)


# Select Record Function
def select_record(event):  # Actually that event is just there because the function
    # is looking for it but does not do anything -- could be any word or letter
    # Clear entry boxes
    clear_entries()
  
    # Grab record number
    selected = my_tree.focus()
    # Grab record values
    values = my_tree.item(selected, 'values')
    # print(values)

    # Output to entry boxes
    id_entry.insert(0, values[0])
    fn_entry.insert(0, values[1])
    ln_entry.insert(0, values[2])   
    address_entry.insert(0, values[3])
    city_entry.insert(0, values[4])
    state_entry.insert(0, values[5])
    country_entry.insert(0, values[6])
    zipcode_entry.insert(0, values[7])

# Create Functions for the Buttons

# Clear Entry boxes Function
def clear_entries():
    id_entry.delete(0, END)
    fn_entry.delete(0, END)
    ln_entry.delete(0, END)
    address_entry.delete(0, END)
    city_entry.delete(0, END)
    state_entry.delete(0, END)
    country_entry.delete(0, END)
    zipcode_entry.delete(0, END)  

# Clear the Treeview
def clear_treeview():
    my_tree.delete(*my_tree.get_children())

# Move Up Function
def move_up():
    rows = my_tree.selection()
    for row in rows:
        my_tree.move(row, my_tree.parent(row), my_tree.index(row)-1)

# Move Down Function
def move_down():
    rows = my_tree.selection()
    for row in reversed(rows):
        my_tree.move(row, my_tree.parent(row), my_tree.index(row)+1)

# Remove ONE Record
def remove_one():
    selected = my_tree.selection()[0]
    my_tree.delete(selected)

    # Create a database or connect to it
    conn = sqlite3.connect('addresses_crm.db')
    # Create a cursor instance
    cur = conn.cursor()
    
    # Delete from Database
  #  cur.execute("DELETE from addresses WHERE oid=" + id_entry.get())
    cur.execute("DELETE from addresses WHERE id=" + id_entry.get())
  
    # Commit the changes
    conn.commit()
    # Close the connection
    conn.close()    
   # Clear entry boxes
    clear_entries()
    # Add a little message box
    messagebox.showinfo("Deleted!", "Your Record Has Been Deleted!")
    

# Remove MANY Records
def remove_many():
    # Add a little message box
    response = messagebox.askyesno("WOAH!!!!", "This Will Delete ALL OF THE SELECTED RECORDS!\nAre You Sure?")

    # Add condition to response
    if response == 1:
        # Designate selections
        many = my_tree.selection()

        # Create List of ID's
        item_to_delete = []
        
        # Add Selection to item_to_delete list
        for record in many:
            item_to_delete.append(my_tree.item(record, 'values')[0])

        # Delete from Treeview
        for record in many:
            my_tree.delete(record)

        # Create a database or connect to it
        conn = sqlite3.connect('addresses_crm.db')
        # Create a cursor instance
        cur = conn.cursor()

        # Delete selected item from the database
        # cur.executemany("DELETE from addresses WHERE id = ?", item_to_delete) -- this works only until the item 9
        cur.executemany("DELETE from addresses WHERE id = ?", [(item,)for item in item_to_delete])
        
        # Commit the changes
        conn.commit()
        # Close the connection
        conn.close()    
        # Clear entry boxes    
        clear_entries()
        # Add a little message box
        messagebox.showinfo("Deleted!", "All of Your SELECTED Records Has Been Deleted!")

# Remove ALL Records
def remove_all():
    # Add a little message box
    response = messagebox.askyesno("WOAH!!!!", "This Will Delete ALL OF YOUR RECORDS!\nAre You Sure?")

    # Add condition on response
    if response == 1:
        # Clear the Treeview
        for record in my_tree.get_children():
            my_tree.delete(record)

        # Connect to the database
        conn = sqlite3.connect('addresses_crm.db')
        # Create a cursor instance
        cur = conn.cursor()

        # Delete Everything From The Table
        cur.execute("DROP TABLE addresses")

        # Create a new empty table
        create_table()
        # Commit the changes
        conn.commit()
        # Close the connection
        conn.close()    
        # Clear entry boxes -- just in case
        clear_entries()
        # Add a little message box
        messagebox.showinfo("Deleted!", "All of Your Record Has Been Deleted!")

# Clear Entry boxes Function
def clear_entries():
    id_entry.delete(0, END)
    fn_entry.delete(0, END)
    ln_entry.delete(0, END)
    address_entry.delete(0, END)
    city_entry.delete(0, END)
    state_entry.delete(0, END)
    country_entry.delete(0, END)
    zipcode_entry.delete(0, END)  

# Clear the Treeview
def clear_treeview():
    my_tree.delete(*my_tree.get_children())

# Create Bindings Click Function
def clicker(e):
    select_record()

# Update Record
def update_record():
    # Grab record number
    selected = my_tree.focus()
    # Update Record
    my_tree.item(selected, text="", values=(id_entry.get(), fn_entry.get(), ln_entry.get(), address_entry.get(), city_entry.get(), state_entry.get(), country_entry.get(), zipcode_entry.get()))
    
    # Update the database
    # Create a database or connect to it
    conn = sqlite3.connect('addresses_crm.db')

    # Create a cursor instance
    cur = conn.cursor()

    cur.execute("""UPDATE addresses SET
        f_name = :first,
        l_name = :last,
        address = :address,
        city = :city,
        state = :state,
        country = :country,
        zipcode = :zipcode
        WHERE oid = :oid""",
        {
            'first': fn_entry.get(),
            'last' : ln_entry.get(),
            'address' : address_entry.get(),
            'city' : city_entry.get(),
            'state' : state_entry.get(),
            'country' : country_entry.get(),
            'zipcode' : zipcode_entry.get(),
            'oid' : id_entry.get(),
        })
    # Commit the changes
    conn.commit()
    # Close the connection
    conn.close()    
    # Clear entry boxes
    clear_entries()

# Add new record function
def add_record():
    # Update the database
    # Create a database or connect to it
    conn = sqlite3.connect('addresses_crm.db')

    # Create a cursor instance
    cur = conn.cursor()

    # Add new record
    cur.execute("INSERT INTO addresses VALUES (:id, :f_name, :l_name, :address, :city, :state, :country, :zipcode)",
        {
            'id': id_entry.get(),
            'f_name': fn_entry.get(),
            'l_name' : ln_entry.get(),
            'address' : address_entry.get(),
            'city' : city_entry.get(),
            'state' : state_entry.get(),
            'country' : country_entry.get(),
            'zipcode' : zipcode_entry.get()
        })

    # Commit the changes
    conn.commit()
    # Close the connection
    conn.close()    
    # Clear entry boxes
    clear_entries()
    # Clear the Treeview
    clear_treeview()
    # Run to pull data from database again
    query_database()

# Add Buttons
button_frame = LabelFrame(root, text="Functions")
button_frame.pack(fill="x", expand="yes", padx=20)
# Update
update_button = Button(button_frame, text="Update Record", command=update_record)
update_button.grid(row=0, column=0, padx=10, pady=10)
# Add
add_button = Button(button_frame, text="Add Record", command=add_record)
add_button.grid(row=0, column=1, padx=10, pady=10)
# Remove One
remove_one_button = Button(button_frame, text="Remove ONE", command=remove_one)
remove_one_button.grid(row=0, column=2, padx=10, pady=10)
# Remove Many
remove_many_button = Button(button_frame, text="Remove SELECTED", command=remove_many)
remove_many_button.grid(row=0, column=3, padx=10, pady=10)
# Remove All
remove_all_button = Button(button_frame, text="Remove ALL", command=remove_all)
remove_all_button.grid(row=0, column=4, padx=10, pady=10)
# Move Up
move_up_button = Button(button_frame, text="Move Up", command=move_up)
move_up_button.grid(row=0, column=5, padx=10, pady=10)
# Move Down
move_down_button = Button(button_frame, text="Move Down", command=move_down)
move_down_button.grid(row=0, column=6, padx=10, pady=10)
# Clear Entry
clear_entries_button = Button(button_frame, text="Clear Entry Boxes", command=clear_entries)
clear_entries_button.grid(row=0, column=7, padx=10, pady=10)

# Bind the Treeview
my_tree.bind("<ButtonRelease-1>", select_record)

# Run to pull data from database on start
query_database()

root.mainloop()