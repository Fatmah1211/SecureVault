import tkinter as tk

root = tk.Tk()
root.title("SecureVault - Password Manager")
root.geometry("400x570")
root.resizable(False, False)
root.configure(bg="#1e1e2e")

# Title
title_label = tk.Label(root, text="SecureVault", font=("Arial", 22, "bold"), bg="#1e1e2e", fg="#cdd6f4")
title_label.pack(pady=20)

# --- Tab buttons ---
tab_frame = tk.Frame(root, bg="#1e1e2e")
tab_frame.pack()

def show_login():
    login_frame.pack(pady=10)
    register_frame.pack_forget()
    login_tab_btn.config(bg="#89b4fa", fg="#1e1e2e")
    register_tab_btn.config(bg="#313244", fg="#cdd6f4")

def show_register():
    register_frame.pack(pady=10)
    login_frame.pack_forget()
    register_tab_btn.config(bg="#89b4fa", fg="#1e1e2e")
    login_tab_btn.config(bg="#313244", fg="#cdd6f4")

login_tab_btn = tk.Button(tab_frame, text="Login", width=15, font=("Arial", 11, "bold"), bg="#89b4fa", fg="#1e1e2e", relief="flat", command=show_login)
login_tab_btn.grid(row=0, column=0, padx=5)

register_tab_btn = tk.Button(tab_frame, text="Register", width=15, font=("Arial", 11, "bold"), bg="#313244", fg="#cdd6f4", relief="flat", command=show_register)
register_tab_btn.grid(row=0, column=1, padx=5)

# --- Login Frame ---
login_frame = tk.Frame(root, bg="#1e1e2e")
tk.Label(login_frame, text="Username", font=("Arial", 12), bg="#1e1e2e", fg="#cdd6f4").pack()
username_entry = tk.Entry(login_frame, font=("Arial", 12), width=25, bg="#313244", fg="#cdd6f4", insertbackground="white")
username_entry.pack(pady=8, ipady=5)

tk.Label(login_frame, text="Password", font=("Arial", 12), bg="#1e1e2e", fg="#cdd6f4").pack()
password_entry = tk.Entry(login_frame, font=("Arial", 12), width=25, show="*", bg="#313244", fg="#cdd6f4", insertbackground="white")
password_entry.pack(pady=8, ipady=5)

# Login Error Label
login_error_label = tk.Label(login_frame, text="", font=("Arial", 10), bg="#1e1e2e", fg="#f38ba8")
login_error_label.pack(pady=5)

def login_clicked():
    username = username_entry.get().strip()
    password = password_entry.get()
    
    if not username or not password:
        login_error_label.config(text="Username and Password are required!")
    else:
        login_error_label.config(text="")
        print("Login form validation passed!")

tk.Button(login_frame, text="Login", font=("Arial", 12, "bold"), bg="#89b4fa", fg="#1e1e2e", width=20, relief="flat", cursor="hand2", command=login_clicked).pack(pady=10)

# --- Register Frame ---
register_frame = tk.Frame(root, bg="#1e1e2e")
tk.Label(register_frame, text="Username", font=("Arial", 12), bg="#1e1e2e", fg="#cdd6f4").pack()
reg_username_entry = tk.Entry(register_frame, font=("Arial", 12), width=25, bg="#313244", fg="#cdd6f4", insertbackground="white")
reg_username_entry.pack(pady=8, ipady=5)

tk.Label(register_frame, text="Password", font=("Arial", 12), bg="#1e1e2e", fg="#cdd6f4").pack()
reg_password_entry = tk.Entry(register_frame, font=("Arial", 12), width=25, show="*", bg="#313244", fg="#cdd6f4", insertbackground="white")
reg_password_entry.pack(pady=8, ipady=5)

tk.Label(register_frame, text="Confirm Password", font=("Arial", 12), bg="#1e1e2e", fg="#cdd6f4").pack()
reg_confirm_entry = tk.Entry(register_frame, font=("Arial", 12), width=25, show="*", bg="#313244", fg="#cdd6f4", insertbackground="white")
reg_confirm_entry.pack(pady=8, ipady=5)

# Register Error Label
reg_error_label = tk.Label(register_frame, text="", font=("Arial", 10), bg="#1e1e2e", fg="#f38ba8")
reg_error_label.pack(pady=5)


def register_clicked():
    username = reg_username_entry.get().strip()
    password = reg_password_entry.get()
    confirm_password = reg_confirm_entry.get()
    
    if not username or not password or not confirm_password:
        reg_error_label.config(text="All fields are required!")
    elif password != confirm_password:
        reg_error_label.config(text="Passwords do not match!")
    else:
        reg_error_label.config(text="")
        print("Registration validation passed!")

tk.Button(register_frame, text="Register", font=("Arial", 12, "bold"), bg="#a6e3a1", fg="#1e1e2e", width=20, relief="flat", cursor="hand2", command=register_clicked).pack(pady=10)

show_login()
root.mainloop()