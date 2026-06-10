import tkinter as tk

root = tk.Tk()
root.title("SecureVault - Password Manager")
root.geometry("400x500")
root.resizable(False, False)
root.configure(bg="#1e1e2e")

# Title
title_label = tk.Label(root, text="SecureVault", font=("Arial", 22, "bold"), bg="#1e1e2e", fg="#cdd6f4")
title_label.pack(pady=30)

# Username
username_label = tk.Label(root, text="Username", font=("Arial", 12), bg="#1e1e2e", fg="#cdd6f4")
username_label.pack()
username_entry = tk.Entry(root, font=("Arial", 12), width=25)
username_entry.pack(pady=8)

# Password
password_label = tk.Label(root, text="Password", font=("Arial", 12), bg="#1e1e2e", fg="#cdd6f4")
password_label.pack()
password_entry = tk.Entry(root, font=("Arial", 12), width=25)
password_entry.pack(pady=8)

# Login button action
def login_clicked():
    print("Login button clicked")

# Login button
login_button = tk.Button(root, text="Login", font=("Arial", 12, "bold"), bg="#89b4fa", fg="#1e1e2e", width=20, command=login_clicked)
login_button.pack(pady=20)

root.mainloop()