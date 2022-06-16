from tkinter import *
from tkinter import messagebox
from random import shuffle, randint, choice
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for char in range(randint(8, 10))]
    password_list += [choice(symbols) for char in range(randint(2, 4))]
    password_list += [choice(numbers) for char in range(randint(2, 4))]

    shuffle(password_list)

    password_text = "".join(password_list)
    password.insert(0, string=password_text)
    pyperclip.copy(password_text)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_data():
    email_text = email.get()
    password_text = password.get()
    website_text = website.get().title()
    new_data = {website_text: {
        "email": email_text,
        "password": password_text
    }}

    if len(email_text) == 0 or len(password_text) == 0 or len(website_text) == 0:
        messagebox.showerror(title="Oops", message="Please don't leave any fields empty")
    else:
        is_ok = messagebox.askokcancel(title=website_text, message=f"These are the details entered:\n Email: {email_text}\n "
                                                                   f"Password: {password_text}")
        if is_ok:
            try:
                with open("data.json", mode="r") as file:
                    data = json.load(file)
            except FileNotFoundError:
                with open("data.json", mode="w") as file:
                    json.dump(new_data, file, indent=4)
            else:
                data.update(new_data)
                with open("data.json", mode="w") as file:
                    json.dump(data, file, indent=4)
            finally:
                password.delete(0, END)
                website.delete(0, END)


# ---------------------------- SEARCH ------------------------------- #
def search_password():
    user_input = website.get().title()
    try:
        with open("data.json", mode="r") as file:
            content = json.load(file)
    except FileNotFoundError:
        messagebox.showerror(title="Oops", message="No Data File Found")
    else:
        if user_input in content:
            website_password = content[user_input]["password"]
            website_email = content[user_input]["email"]
            messagebox.showinfo(title=user_input, message=f"email: {website_email}\npassword:"
                                                          f" {website_password}")
        else:
            messagebox.showinfo(title="Oops", message="No details for this website exists")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
img = PhotoImage(file="logo.png")

canvas.create_image(100, 100, image=img)
canvas.grid(column=1, row=0)

# Labels

website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# Text Fields

website = Entry(width=33)
website.grid(row=1, column=1, pady=10)
website.focus()

email = Entry(width=53)
email.grid(row=2, column=1, columnspan=2)
email.insert(0, "hogweda@gmail.com")

password = Entry(width=33)
password.grid(row=3, column=1, pady=10)

# Buttons
search = Button(text="Search", width=15, command=search_password)
search.grid(row=1, column=2)

generate_password = Button(text="Generate Password", width=15, command=generate_password)
generate_password.grid(row=3, column=2)

add = Button(width=44, text="Add", command=add_data)
add.grid(row=4, column=1, columnspan=2)

window.mainloop()
