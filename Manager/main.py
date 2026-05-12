from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generator():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = [random.choice(letters) for _ in range(nr_letters)]
    password_list += [random.choice(symbols) for _ in range(nr_symbols)]
    password_list += [random.choice(numbers) for _ in range(nr_numbers)]

    random.shuffle(password_list)

    password_generated = "".join(password_list)
    pyperclip.copy(password_generated)
    password.delete(0, END)
    password.insert(0, password_generated)



# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    new_data = {
        web_site.get(): {
            "email": email.get(),
            "password": password.get()
        }
    }

    if len(web_site.get()) == 0 or len(password.get()) == 0:
        messagebox.showerror("Error", "Please enter all fields")
    else:
        is_ok = messagebox.askokcancel(title=web_site.get(), message=f"These are the details entered: "
                                                                     f"\nEmail: {email.get()}\nPassword: {password.get()}\n "
                                                                     f"Is this okay to save?")

        if is_ok:
            try:
                with open("data.json", "r") as file:
                    data = json.load(file)
                    data.update(new_data)
            except (FileNotFoundError, json.JSONDecodeError):
                with open("data.json", "w") as file:
                    json.dump(new_data, file, indent=4)
            else:
                with open("data.json", "w") as file:
                    json.dump(data, file, indent=4)
            finally:
                web_site.delete(0, END)
                password.delete(0, END)
                web_site.focus()

#---------------------SEARCH_PASSWORD----------------------------------#
def find_password():
    website_name = web_site.get()
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
            if website_name in data:
                email_name = data[website_name]["email"]
                password_name = data[website_name]["password"]
                messagebox.showinfo("Password Manager", f"Email: {email_name}\nPassword: {password_name}")
            else:
                messagebox.showerror("Password Manager", "No details found")
    except (FileNotFoundError,json.JSONDecodeError):
        messagebox.showerror("Error", "No DataFile found")



# ---------------------------- UI SETUP ------------------------------- #

## window
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

## canvas

canvas = Canvas(width=200, height=200)
image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=image)
canvas.grid(column=1, row=0)

## labels

website = Label(text="Website:")
Email_User = Label(text="Email/Username:")
Password = Label(text="Password:")
website.grid(column=0, row=1)
Email_User.grid(column=0, row=2)
Password.grid(column=0, row=3)

## entry

web_site = Entry(width=32)
web_site.focus()
email = Entry(width=35)
email.insert(0, "@gmail.com")
password = Entry(width=32)
web_site.grid(column=1, row=1)
email.grid(column=1, row=2, columnspan=2, sticky="ew")
email.insert(END, "")
password.grid(column=1, row=3, sticky="w")


## buttons

generate = Button(text="Generate Password", width=15, command=password_generator)
add = Button(text="Add", width=36, command=save)
Search = Button(text="Search", width=15, command=find_password)
generate.grid(column=2, row=3)
add.grid(column=1, row=4, columnspan=2, sticky="ew")
Search.grid(column=2, row=1)

window.mainloop()

