import tkinter as tk
from tkinter import messagebox as mess
from PIL import Image, ImageTk
import subprocess

def login():
    username = username_entry_main.get()
    password = password_entry_main.get()

    # Check if the entered username and password are correct
    if username == "admin" and password == "admin123":
        mess.showinfo("Login Successful", "Welcome, " + username + "!")
        open_main_script()
    else:
        mess.showerror("Login Failed", "Invalid username or password")

def open_main_script():
    # Hide the login window
    main_window.deiconify()
    # Close the login window
    login_window.withdraw()

    # Run the main.py script using subprocess
    subprocess.run(["python", "main.py"])

# Create the login window
login_window = tk.Tk()
login_window.geometry("1280x720")
login_window.title("SKSU Facial Recognition-Based Attendance System")

# Load the background image
bg_image = Image.open('sksu_bg.jpg')  # Replace 'path_to_your_image.jpg' with the actual path
bg_image = ImageTk.PhotoImage(bg_image)

# Create a label to display the background image
bg_label = tk.Label(login_window, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

# Add a login form to the login window
login_label_main = tk.Label(login_window, text="Login", font=('arial', 20, 'bold'), bg="SystemButtonFace")
login_label_main.pack(pady=20)

username_label_main = tk.Label(login_window, text="Username:", font=('arial', 12), bg="SystemButtonFace")
username_label_main.pack(pady=5)

username_entry_main = tk.Entry(login_window, font=('arial', 12))
username_entry_main.pack(pady=5)

password_label_main = tk.Label(login_window, text="Password:", font=('arial', 12), bg="SystemButtonFace")
password_label_main.pack(pady=5)

password_entry_main = tk.Entry(login_window, show="*", font=('arial', 12))
password_entry_main.pack(pady=10)

login_button_main = tk.Button(login_window, text="Login", command=login, font=('arial', 12, 'bold'), bg="SystemButtonFace")
login_button_main.pack(pady=20)

main_label = tk.Label(login_window, text="Welcome to the Login Window", font=('arial', 20, 'bold'), bg="SystemButtonFace")
main_label.pack(pady=50)

# Create the main window but keep it hidden initially
main_window = tk.Tk()
main_window.geometry("1280x720")
main_window.title("SKSU Facial Recognition-Based Attendance System")
main_window.withdraw()

# ... (add other components as needed)

# Start the login window
login_window.mainloop()
