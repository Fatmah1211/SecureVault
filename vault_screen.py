import tkinter as tk
from tkinter import ttk

class VaultScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("SecureVault - Password Vault")
        self.root.geometry("800x500")
        
        # Title Label
        title = tk.Label(root, text="My Password Vault", font=("Arial", 18, "bold"))
        title.pack(pady=10)
        # Table Frame
        frame = tk.Frame(root)
        frame.pack(pady=10, fill="both", expand=True)

        # Treeview Table
        self.tree = ttk.Treeview(frame, columns=("Website", "Username", "Password"), show="headings")
        self.tree.heading("Website", text="Website")
        self.tree.heading("Username", text="Username")
        self.tree.heading("Password", text="Password")
        self.tree.column("Website", width=200)
        self.tree.column("Username", width=200)
        self.tree.column("Password", width=200)
        self.tree.pack(fill="both", expand=True)