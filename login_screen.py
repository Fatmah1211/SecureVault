import tkinter as tk

root = tk.Tk()
root.title("SecureVault - Password Manager")
root.geometry("400x500")
root.resizable(False, False)
root.configure(bg="#1e1e2e")

# Title label
title_label = tk.Label(root, text="SecureVault", font=("Arial", 22, "bold"), bg="#1e1e2e", fg="#cdd6f4")
title_label.pack(pady=30)

# Username label and field
username_label = tk.Label(root, text="Username", font=("Arial", 12), bg="#1e1e2e", fg="#cdd6f4")
username_label.pack()
username_entry = tk.Entry(root, font=("Arial", 12), width=25)
username_entry.pack(pady=8)

# Password label and field
password_label = tk.Label(root, text="Password", font=("Arial", 12), bg="#1e1e2e", fg="#cdd6f4")
password_label.pack()
password_entry = tk.Entry(root, font=("Arial", 12), width=25)
password_entry.pack(pady=8)

root.mainloop()