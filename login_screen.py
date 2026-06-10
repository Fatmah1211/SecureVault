import tkinter as tk

root = tk.Tk()
root.title("SecureVault - Password Manager")
root.geometry("400x500")
root.resizable(False, False)
root.configure(bg="#1e1e2e")

# Title
title_label = tk.Label(root, text="SecureVault", font=("Arial", 22, "bold"), bg="#1e1e2e", fg="#cdd6f4")
title_label.pack(pady=30)

# Username - Now with custom dark background and padding
username_label = tk.Label(root, text="Username", font=("Arial", 12), bg="#1e1e2e", fg="#cdd6f4")
username_label.pack()
username_entry = tk.Entry(root, font=("Arial", 12), width=25, bg="#313244", fg="#cdd6f4", insertbackground="white")
username_entry.pack(pady=8, ipady=5)

# Password — show='*' hides the text while typing!
password_label = tk.Label(root, text="Password", font=("Arial", 12), bg="#1e1e2e", fg="#cdd6f4")
password_label.pack()
password_entry = tk.Entry(root, font=("Arial", 12), width=25, show="*", bg="#313244", fg="#cdd6f4", insertbackground="white")
password_entry.pack(pady=8, ipady=5)

# Login button action
def login_clicked():
    print("Login button clicked")

# Login button - Now with a sleek flat design and hand cursor
login_button = tk.Button(root, text="Login", font=("Arial", 12, "bold"), bg="#89b4fa", fg="#1e1e2e", width=20, relief="flat", cursor="hand2", command=login_clicked)
login_button.pack(pady=20)

root.mainloop()