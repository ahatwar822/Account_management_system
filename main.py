import mysql.connector
from tkinter import *
import tkinter.messagebox as messagebox
import random

# Function to create a database connection
def create_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="account_manager"
    )
    return connection

# Function to create the 'accounts' table if it doesn't exist
def create_table(cursor):
    cursor.execute("CREATE TABLE IF NOT EXISTS accounts (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), account_number VARCHAR(20) UNIQUE, password VARCHAR(255), amount FLOAT)")

# Function to add a new account
def create_account(cursor, name, password, amount):
    account_number = generate_account_number()
    query = "INSERT INTO accounts (name, account_number, password, amount) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (name, account_number, password, amount))
    connection.commit()
    update_accounts_listbox()  # Update the listbox after creating a new account

# Function to update an existing account
def update_account(cursor, account_number, password, new_amount):
    query = "UPDATE accounts SET amount = %s WHERE account_number = %s AND password = %s"
    cursor.execute(query, (new_amount, account_number, password))
    connection.commit()

# Function to generate a random account number
def generate_account_number():
    return ''.join([str(random.randint(0, 9)) for _ in range(16)])

# Function to update the listbox with account information
def update_accounts_listbox():
    accounts_listbox.delete(0, END)
    cursor.execute("SELECT * FROM accounts")
    accounts = cursor.fetchall()
    for account in accounts:
        accounts_listbox.insert(END, f"Name: {account[1]}, Account Number: {account[2]}, Amount: {account[4]}")

# GUI Functions
def create_account_gui():
    name = entry_name.get()
    password = entry_password.get()
    amount = entry_amount.get()

    if name == "" or password == "" or amount == "":
        messagebox.showerror("Error", "Please fill in all information!")
    else:
        create_account(cursor, name, password, amount)
        messagebox.showinfo("Success", "Account created successfully!")

def update_account_gui():
    account_number = entry_account_number.get()
    password = entry_password.get()
    new_amount = entry_new_amount.get()

    update_account(cursor, account_number, password, new_amount)
    messagebox.showinfo("Success", "Account updated successfully!")

# Main GUI Setup
root = Tk()
root.title("Account Management Program")

# Entry widgets for user input
entry_name = Entry(root, width=30)
entry_name.grid(row=0, column=1, padx=10, pady=5)
label_name = Label(root, text="Name:")
label_name.grid(row=0, column=0, padx=10, pady=5)

entry_password = Entry(root, width=30, show="*")
entry_password.grid(row=1, column=1, padx=10, pady=5)
label_password = Label(root, text="Password:")
label_password.grid(row=1, column=0, padx=10, pady=5)

entry_amount = Entry(root, width=30)
entry_amount.grid(row=2, column=1, padx=10, pady=5)
label_amount = Label(root, text="Amount:")
label_amount.grid(row=2, column=0, padx=10, pady=5)

entry_account_number = Entry(root, width=30)
entry_account_number.grid(row=3, column=1, padx=10, pady=5)
label_account_number = Label(root, text="Account Number:")
label_account_number.grid(row=3, column=0, padx=10, pady=5)

entry_new_amount = Entry(root, width=30)
entry_new_amount.grid(row=4, column=1, padx=10, pady=5)
label_new_amount = Label(root, text="New Amount:")
label_new_amount.grid(row=4, column=0, padx=10, pady=5)


# Listbox to display account information
accounts_listbox = Listbox(root, height=10, width=50)
accounts_listbox.grid(row=8, column=0, columnspan=2, pady=10)
# After the entry widgets, add a Text widget
text_output = Text(root, width=50, height=10)
text_output.grid(row=8, column=0, columnspan=2, pady=10)

# Function to display account details in the Text widget
def display_account_details():
    text_output.delete(1.0, END)  # Clear previous content
    cursor.execute("SELECT * FROM accounts")
    accounts = cursor.fetchall()
    for account in accounts:
        text_output.insert(END, f"Name: {account[1]}\n")
        text_output.insert(END, f"Account Number: {account[2]}\n")
        # text_output.insert(END, f"Password: {account[3]}\n")
        text_output.insert(END, f"Amount: {account[4]}\n")
        text_output.insert(END, "-" * 30 + "\n")

# Buttons for account management actions
btn_create_account = Button(root, text="Create Account", command=create_account_gui)
btn_create_account.grid(row=5, column=0, columnspan=2, pady=10)

btn_update_account = Button(root, text="Update Account", command=update_account_gui)
btn_update_account.grid(row=6, column=0, columnspan=2, pady=10)

btn_exit = Button(root, text="Exit", command=root.destroy)
btn_exit.grid(row=7, column=0, columnspan=2, pady=10)

# Add a button to trigger the display_account_details function
btn_display_details = Button(root, text="Display Account Details", command=display_account_details)
btn_display_details.grid(row=9, column=0, columnspan=2, pady=10)

# Create a database connection and table
connection = create_connection()
cursor = connection.cursor()
create_table(cursor)
update_accounts_listbox()  # Initial update of the listbox

# Start the Tkinter event loop
root.mainloop()
