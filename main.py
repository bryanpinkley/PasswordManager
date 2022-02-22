from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

FONT = ("Arial", 10, "normal")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)

    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = (website_entry.get()).lower()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
         }
     }

    if len(website) < 1 or len(email) < 1 or len(password) < 1:
        messagebox.showinfo(title="Error", message="Please fill in all fields.")
    else:
        try:
            with open("data.json", "r") as file:
                # How to read json
                data = json.load(file)
        except FileNotFoundError:
            with open("data.json", "w") as file:
                # How to write new json
                json.dump(new_data, file, indent=4)
        else:
            # How to update json
            data.update(new_data)
            with open("data.json", "w") as file:
                # How to write updated json
                json.dump(data, file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)
            website_entry.focus()


# ---------------------------- SEARCH PASSWORD ------------------------------- #
def find_password():
    try:
        website = (website_entry.get()).lower()
        with open("data.json", "r") as file:
            data = json.load(file)
            search_email = data[website]["email"]
            search_password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {search_email} \nPassword: {search_password}")
            pyperclip.copy(search_password)
    except KeyError:
        messagebox.showinfo(title="No Website Found", message="This website does not exist in the file.")
    except FileNotFoundError:
        messagebox.showinfo(title="No File Found", message="The data file does not exist.")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

# Logo Image
canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=2, row=1)

# Website Label
website_label = Label(text="Website:", font=FONT)
website_label.grid(column=1, row=2)

# Website Entry
website_entry = Entry(width=25)
website_entry.grid(column=2, row=2)
website_entry.focus()

# Email Label
email_label = Label(text="Email/Username:", font=FONT)
email_label.grid(column=1, row=3)

# Email Entry
email_entry = Entry(width=42)
email_entry.grid(column=2, row=3, columnspan=2)
email_entry.insert(0, "sample@email.com")

# Password Label
password_label = Label(text="Password:", font=FONT)
password_label.grid(column=1, row=4)

# Password Entry
password_entry = Entry(width=25)
password_entry.grid(column=2, row=4)

# Password Button
password_button = Button(text="Generate Password", command=generate_password)
password_button.grid(column=3, row=4)

# Search Button
password_button = Button(text="Search", width=16, command=find_password)
password_button.grid(column=3, row=2)

# Add Button
add_button = Button(text="Add", width=42, command=save)
add_button.grid(column=2, row=5, columnspan=2)

window.mainloop()
