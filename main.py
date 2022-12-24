from tkinter import *
import re
import random
# Generate password and storing it into the password entry #
def generate_password():
    password_entry.delete(0, END)
    lower_case = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    upper_case = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    special = ['@', '#', '$', '%', '^', '&', '+', '=', '!', '?', '.']
    numbers = ['1','2','3','3','4','5','6','7','8','9']
    list_of_lists = [lower_case, upper_case, special, numbers]
    new_password = []
    for i in range(3):
        for list in list_of_lists:
            new_password.append(random.choice(list))
    new_password = ''.join(new_password)
    password_entry.insert(0, new_password)

# Check entrys and save password #

def clean_notification_label():
    notification.config(text="")

def write():
    password_file = open("password.txt", "a")
    password_file.write(f'Website: {website_entry.get()} | Email/User: {emailusername_entry.get()} | Password: {password_entry.get()}\n')
    notification.config(text=f'A password for\n{website_entry.get()}\nhas been added.')

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
# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=35, pady=35)
window.resizable(False, False)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
# I will have to select the x and y position inside the canvas
# Notice that the image will be centered because I had put the half of width and height
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=0)

website_label = Label(text="Website:", font=("Arial", 12, 'bold'))
website_label.grid(row=1, column=0)

website_entry = Entry(width=52)
website_entry.grid(column=1, row=1, columnspan=2)
website_entry.focus()

emailusername_label = Label(text="Email/Username:", font=("Arial",12,'bold'))
emailusername_label.grid(column=0, row=2)

emailusername_entry = Entry(width=52)
emailusername_entry.grid(column=1, row=2, columnspan=2)
emailusername_entry.insert(END, "email@hotmail.com") 

password_label = Label(text="Password", font=("Arial",12,"bold"))
password_label.grid(column=0, row=3)

password_entry = Entry(width=25)
password_entry.grid(column=1, row=3)

generate_password_button = Button(text="Generate Password",font=("Arial",12,"bold"), command=generate_password)
generate_password_button.grid(column=2, row=3)

add_button = Button(text="Add", font=("Arial",12,"bold"), width=31, command=checkandwrite)
add_button.grid(column=1, row=4, columnspan=2)

notification = Label()
notification.grid(row=0,column=1, sticky="W")

window.mainloop()