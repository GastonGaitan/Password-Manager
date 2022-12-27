from tkinter import *
from tkinter import messagebox
import re
import random
import json

# Generate password and storing it into the password entry #
def generate_password():
    password_entry.delete(0, END)
    lower_case = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    upper_case = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    special = ['@', '#', '$', '%', '^', '&', '+', '=', '!', '?', '.']
    numbers = ['1','2','3','3','4','5','6','7','8','9']
    list_of_lists = [lower_case, upper_case, special, numbers]
    new_password = []
    for i in range(random.randint(2,3)):
        for list in list_of_lists:
            new_password.append(random.choice(list))
    new_password = ''.join(new_password)
    password_entry.insert(0, new_password)


# Clean notification label
def clean_notification_label():
    notification.config(text="")

# Save info
def write():
    website = website_entry.get()
    email = emailusername_entry.get()
    password = password_entry.get()

    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    try:
        # If the file data.json exists, I open it in reading mode and store its data structure in a data_file
        with open('data.json','r') as data_file:
            data = json.load(data_file)
            print(f'The file already exists. Data taken from data.json: {data}')
    except FileNotFoundError:
        # If the data.json file does not exist, I open it in write mode and store the content extracted in new_data dict
        with open('data.json', 'w') as data_file:
            json.dump(new_data, data_file, indent=4)
            print(f'The file does not exist. Next content has been dumped: {new_data}')
    else:
        # data.update adds new data to the file
        data.update(new_data)
        print(data)
        with open('data.json', 'w') as data_file:
            json.dump(data, data_file, indent=4)
    finally: 
        notification.config(text=f'A password for\n{website_entry.get()}\nhas been added.')


# Check before saving info
def checkandwrite():

    clean_notification_label()    

    website_regex = r"www\..*?\.com.*"
    website = website_entry.get()

    password_regex = r"^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=!\?]).*$"
    password = password_entry.get()

    valid_website = re.fullmatch(website_regex, website)
    valid_password = re.fullmatch(password_regex, password)

    if valid_website and valid_password:
        write()
    else:
        if not valid_website:
            clean_notification_label()
            notification.config(text="Invalid website direction.")
        else:
            if not valid_password:
                notification.config(text="Invalid password.\nPassword requirements:\n• Uppercase letters: A-Z.\n• Lowercase letters: a-z.\n• Numbers: 0-9.\n• Any of the special\n characters: @#$%^&+=!?.")

# Search password

def search():
    try:
        with open('data.json', 'r') as data_file:
            data = json.load(data_file)
            website_to_search = website_entry.get()
            if website_to_search in data:
                notification.config(text=f"{website_to_search}\nEmail: {data[website_to_search]['email']}\nPassword: {data[website_to_search]['password']}")
            else:
                respuesta = messagebox.showinfo("Warning", "No details for the website exists.")
                popup = Label(window, text=respuesta)
    except FileNotFoundError:
        respuesta = messagebox.showinfo("Warning", "No data file found.")
        popup = Label(window, text=respuesta)
            
# Window setup
window = Tk()
window.title("Password Manager")
window.config(padx=35, pady=35)
window.resizable(False, False)

# Canvas Image
canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=0, sticky='w')

#Labels
website_label = Label(text="Website:", font=("Arial", 12, 'bold'))
website_label.grid(row=1, column=0, sticky='e')

emailusername_label = Label(text="Email/Username:", font=("Arial",12,'bold'))
emailusername_label.grid(column=0, row=2, sticky='e')

password_label = Label(text="Password:", font=("Arial",12,"bold"))
password_label.grid(column=0, row=3, sticky='e')

space = Label(text='')
space.grid(column=1, row=4, columnspan=2)

notification = Label()
notification.grid(row=0,column=1, sticky="W")

# Entrys
website_entry = Entry(width=35)
website_entry.grid(column=1, row=1, columnspan=2, sticky='w')
website_entry.focus()

emailusername_entry = Entry(width=53)
emailusername_entry.grid(column=1, row=2, columnspan=2, sticky='w')
emailusername_entry.insert(END, "email@hotmail.com")

password_entry = Entry(width=29)
password_entry.grid(column=1, row=3, sticky='w')


# Buttons
website_search = Button(text="Search", font=("Arial",10,"bold"), command=search, width=11, bg='gray', fg='white')
website_search.grid(row=1, column=2, sticky='e')

generate_password_button = Button(text="Generate Password",font=("Arial",10,"bold"), command=generate_password, height=1, fg='white', bg='black')
generate_password_button.grid(column=2, row=3, sticky='e')

add_button = Button(text="Add", font=("Arial",12,"bold"), width=31, command=checkandwrite, fg='white', bg='gray')
add_button.grid(column=1, row=5, columnspan=2)

window.mainloop()