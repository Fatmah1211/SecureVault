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