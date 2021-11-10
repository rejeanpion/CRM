from tkinter import *
from tkinter import ttk
import csv
from tkinter import messagebox
import mysql.connector
from tkinter import colorchooser
from configparser import ConfigParser

root = Tk()
root.title('Rejean Pion - Certifications')
root.iconbitmap('RP_Logo.ico')
root.geometry('1400x800')

# Connect to MySQL
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "Mesbusiness@2021",
    database = "certification",)

# Check to see if connection to MySQL was created
# print(mydb)

# Create a cursor and initialize it
cur = mydb.cursor()

# Create database -- run once
# cur.execute("CREATE DATABASE certification")

# Test to see if database was created
#cur.execute("SHOW DATABASES")
#for db in cur:
#    print(db)

# Drop the table
# cur.execute("DROP TABLE clients")

# Create a table
def create_table():
    cur.execute("CREATE TABLE IF NOT EXISTS courses (course_id VARCHAR(10),\
        course_name VARCHAR(255),\
        company VARCHAR(255),\
        streamer VARCHAR(255),\
        cursus VARCHAR(255),\
        specialization VARCHAR(5),\
        start_date VARCHAR(50),\
        end_date VARCHAR(50),\
        length VARCHAR(10),\
        grade VARCHAR(10),\
        credential_id VARCHAR(50),\
        credential_url VARCHAR(255))")

# show table
'''cur.execute("SELECT * FROM courses")
print(cur.description)
for item in cur.description:
    print(item)'''

# Import data in a list -- run once to import data
'''with open('grades.csv', newline='') as file:
    reader = csv.reader(file)
    data = list(reader)

# Import csv Record into the Database -- run once
for item in data:
    print(item)
    cur.execute("INSERT INTO courses (course_id, course_name, company, streamer, cursus, specialization, start_date, end_date, length, grade, credential_id, credential_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (item))

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

    cur.execute("SELECT * FROM courses")
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
		    my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9], record[10], record[11]), tags=('evenrow',))
	    else:
		    my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9], record[10], record[11]), tags=('oddrow',))
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
    course_id_box.delete(0, END)
    course_name_box.delete(0, END)
    company_box.delete(0, END)
    streamer_box.delete(0, END)
    cursus_box.delete(0, END)
    specialization_box.delete(0, END)
    start_date_box.delete(0, END)
    end_date_box.delete(0, END)
    length_box.delete(0, END)
    grade_box.delete(0, END)
    credential_id_box.delete(0, END)
    credential_url_box.delete(0, END)


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
    course_id_box.insert(0, values[0])
    course_name_box.insert(0, values[1])
    company_box.insert(0, values[2])   
    streamer_box.insert(0, values[3])
    cursus_box.insert(0, values[4])
    specialization_box.insert(0, values[5])
    start_date_box.insert(0, values[6])
    end_date_box.insert(0, values[7])
    length_box.insert(0, values[8])
    grade_box.insert(0, values[9])
    credential_id_box.insert(0, values[10])
    credential_url_box.insert(0, values[11])

# Clear the Treeview
def clear_treeview():
    my_tree.delete(*my_tree.get_children())

# Create Bindings Click Function
def clicker(event):
    select_record()

# Function to add a Record to the Database
def add_course():
    sql_command ="INSERT INTO courses (course_name, company, streamer, cursus, specialization, start_date, end_date, length, grade, credential_id, credential_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (course_name_box.get(), company_box.get(), streamer_box.get(), cursus_box.get(), specialization_box.get(), start_date_box.get(), end_date_box.get(), length_box.get(), grade_box.get(), credential_id_box.get(), credential_url_box.get())
    cur.execute(sql_command, values)

    # Commit the changes to the database
    mydb.commit()
    # Clear the old entry
    clear_record()
    # Refresh the Data Frame
    query_database()

# Function to Edit Record 
def edit_course():
# Update the Database
    sql_command = f"""UPDATE courses
                  SET course_name = %s, company = %s,
                      streamer = %s, cursus = %s,
                      specialization = %s, start_date = %s,
                      end_date = %s, length = %s,
                      grade = %s, credential_id = %s, credential_url = %s
                  WHERE course_id = %s"""

    cur.execute(sql_command, (course_name_box.get(), company_box.get(),
                          streamer_box.get(), cursus_box.get(),
                          specialization_box.get(), start_date_box.get(),
                          end_date_box.get(), length_box.get(),
                          grade_box.get(), credential_id_box.get(), credential_url_box.get(),
                          course_id_box.get()))

    # Commit the changes to the database
    mydb.commit()
    # Clear the old entry
    clear_record()
    # Refresh the Data Frame
    query_database()

# Function to delete on client
def delete_course():    
# Delete from Database
    sql_command = f"DELETE FROM courses WHERE course_id =" + course_id_box.get()

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
        cur.execute("DROP TABLE courses")

        # Create a new empty table
        create_table()
        # Commit the changes
        mydb.commit()
        # Clear entry boxes -- just in case
        clear_record()
        # Add a little message box
        messagebox.showinfo("Deleted!", "All of Your Record Has Been Deleted!")

# Create the search function
def search_course():
    # Create the command function to search now 
    def search_now():
        selected = drop.get()
        command = ""
        if selected == "Search by...":
            no_select = Label(button_frame, text="Please select a search category")
            no_select.grid(row=1, column=1, padx=10)
        elif selected == "Course Name":
            command = "SELECT * FROM courses WHERE course_name = %s"
        elif selected == "Company":
            command = "SELECT * FROM courses WHERE company = %s"
        elif selected == "Streamer":
            command = "SELECT * FROM courses WHERE streamer = %s"
        elif selected == "Cursus":
            command = "SELECT * FROM courses WHERE cursus = %s"
        elif selected == "Specialization":
            command = "SELECT * FROM courses WHERE specialization = %s"
        elif selected == "Length":
            command = "SELECT * FROM clients WHERE length = %s"
        elif selected == "Grade":
            command = "SELECT * FROM clients WHERE grade = %s"

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
		        my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9], record[10], record[11]), tags=('evenrow',))
	        else:
		         my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9], record[10], record[11]), tags=('oddrow',))
	    # increment counter
	        count += 1

    # Create the Search Box
    search_box = Entry(button_frame)
    search_box.grid(row=1, column =1, padx=10)
    # Create a submit button
    submit_button = Button(button_frame, text="Submit", command=search_now)
    submit_button.grid(row=1, column=2, padx=10)
    # Drop Down Box
    drop = ttk.Combobox(button_frame, value=["Search by...", "Course Name", "Company", "Streamer", "Cursus", "Specialization", "Length", "Grade"])
    drop.current(0)
    drop.grid(row=1, column=3, padx=10)

# Create a Label
title_label = Label(root, text="GRADES TABLE", font=('Helvetica', 16))
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
my_tree['columns'] = ("Course ID", "Course Name", "Company", "Streamer", "Cursus", "Specialization", "Start Date", "End Date", "Length", "Grade", "Credential ID", "Credential URL")

# Format Our Columns
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("Course ID", anchor=W, width=80)
my_tree.column("Course Name", anchor=W, width=140)
my_tree.column("Company", anchor=W, width=140)
my_tree.column("Streamer", anchor=CENTER, width=140)
my_tree.column("Cursus", anchor=CENTER, width=140)
my_tree.column("Specialization", anchor=CENTER, width=140)
my_tree.column("Start Date", anchor=CENTER, width=140)
my_tree.column("End Date", anchor=CENTER, width=140)
my_tree.column("Length", anchor=CENTER, width=140)
my_tree.column("Grade", anchor=CENTER, width=140)
my_tree.column("Credential ID", anchor=CENTER, width=140)
my_tree.column("Credential URL", anchor=CENTER, width=140)

# Create Headings
my_tree.heading("#0", text="", anchor=W)
my_tree.heading("Course ID", text="Course ID", anchor=W)
my_tree.heading("Course Name", text="Course Name", anchor=W)
my_tree.heading("Company", text="Company", anchor=W)
my_tree.heading("Streamer", text="Streamer", anchor=CENTER)
my_tree.heading("Cursus", text="Cursus", anchor=CENTER)
my_tree.heading("Specialization", text="Specialization", anchor=CENTER)
my_tree.heading("Start Date", text="Start Date", anchor=CENTER)
my_tree.heading("End Date", text="End Date", anchor=CENTER)
my_tree.heading("Length", text="Length", anchor=CENTER)
my_tree.heading("Grade", text="Grade", anchor=CENTER)
my_tree.heading("Credential ID", text="Credential ID", anchor=CENTER)
my_tree.heading("Credential URL", text="Credential URL", anchor=CENTER)

# Create Stripped Row Tags
my_tree.tag_configure('oddrow', background=saved_secondary_color)
my_tree.tag_configure('evenrow', background=saved_primary_color)

# Add Record Entry Boxes
data_frame = LabelFrame(root, text="Record")
data_frame.pack(fill="both", expand="yes", padx=20)

# Create Main Form To Enter Clients Data
course_id_label = Label(data_frame, text="Course ID").grid(row=1, column =0, sticky=W, padx=10)
course_name_label = Label(data_frame, text="Course Name").grid(row=1, column =1, sticky=W, padx=10)
company_label = Label(data_frame, text="Company").grid(row=1, column =2, sticky=W, padx=10)
streamer_label = Label(data_frame, text="Streamer").grid(row=1, column =3, sticky=W, padx=10)
cursus_label = Label(data_frame, text="Cursus").grid(row=1, column =4, sticky=W, padx=10)
specialization_label = Label(data_frame, text="Specialization").grid(row=1, column =5, sticky=W, padx=10)
start_date_label = Label(data_frame, text="Start Date").grid(row=3, column =0, sticky=W, padx=10)
end_date_label = Label(data_frame, text="End Date").grid(row=3, column =1, sticky=W, padx=10)
length_label = Label(data_frame, text="Length").grid(row=3, column =2, sticky=W, padx=10)
grade_label = Label(data_frame, text="Grade").grid(row=3, column =3, sticky=W, padx=10)
Credential_id_label = Label(data_frame, text="Credential ID").grid(row=3, column =4, sticky=W, padx=10)
Credential_url_label = Label(data_frame, text="Credential URL").grid(row=3, column =5, sticky=W, padx=10)

# Create Empty Boxes
course_id_box = Entry(data_frame)
course_id_box.grid(row=2, column =0, padx=10)
course_name_box = Entry(data_frame)
course_name_box.grid(row=2, column =1, padx=10)
company_box = Entry(data_frame)
company_box.grid(row=2, column =2, padx=10)
streamer_box = Entry(data_frame)
streamer_box.grid(row=2, column =3, padx=10)
cursus_box = Entry(data_frame)
cursus_box.grid(row=2, column =4, padx=10)
specialization_box = Entry(data_frame)
specialization_box.grid(row=2, column =5, padx=10)
start_date_box = Entry(data_frame)
start_date_box.grid(row=4, column =0, padx=10)
end_date_box = Entry(data_frame)
end_date_box.grid(row=4, column =1, padx=10)
length_box = Entry(data_frame)
length_box.grid(row=4, column =2, padx=10)
grade_box = Entry(data_frame)
grade_box.grid(row=4, column =3, padx=10)
credential_id_box = Entry(data_frame)
credential_id_box.grid(row=4, column =4, padx=10)
credential_url_box = Entry(data_frame)
credential_url_box.grid(row=4, column =5, padx=10)

# Create Buttons
# Create a Button Frame
button_frame = LabelFrame(root, text="Functions")
button_frame.pack(fill="x", expand="yes", padx=20)
# Add Button
add_client_button = Button(button_frame, text="Add Course", command=add_course)
add_client_button.grid(row=0, column=0, padx=10, pady=10)
# Delete Button
delete_client_button = Button(button_frame, text="Delete Course", command=delete_course)
delete_client_button.grid(row=0, column=1, padx=10, pady=10)
# Delete All Button
delete_all_client_button = Button(button_frame, text="Delete All Courses", command=delete_all)
delete_all_client_button.grid(row=0, column=2, padx=10, pady=10)
# Clear Record Button
clear_record_button = Button(button_frame, text="Clear Record", command=clear_record)
clear_record_button.grid(row=0, column=3, padx=10, pady=10)
# Search Button
search_button = Button(button_frame, text="Search",command=search_course)
search_button.grid(row=1, column=0, padx=10, pady=10)
# Edit Button
edit_client_button = Button(button_frame, text="Edit Course", command=edit_course)
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