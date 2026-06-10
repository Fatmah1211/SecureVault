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

        # Sample Data for testing
        sample_data = [
            ("facebook.com", "ayesha123", "••••••"),
            ("gmail.com", "ayesha@gmail.com", "••••••"),
            ("github.com", "ayesha_dev", "••••••"),
        ]
        for item in sample_data:
            self.tree.insert("", "end", values=item)

        # Buttons Frame
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        # Add Entry Button
        add_btn = tk.Button(btn_frame, text="Add Entry", width=15, bg="green", fg="white")
        add_btn.grid(row=0, column=0, padx=10)

        # Delete Entry Button
        delete_btn = tk.Button(btn_frame, text="Delete Entry", width=15, bg="red", fg="white", command=self.delete_entry)
        delete_btn.grid(row=0, column=1, padx=10)

        # Copy Password Button
        copy_btn = tk.Button(btn_frame, text="Copy Password", width=15, bg="blue", fg="white", command=self.copy_password)
        copy_btn.grid(row=0, column=2, padx=10)

        # Show/Hide Password Button
        self.show_pass = False
        show_btn = tk.Button(btn_frame, text="Show Password", width=15, bg="orange", fg="white", command=self.toggle_password)
        show_btn.grid(row=0, column=3, padx=10)

    def toggle_password(self):
        if self.show_pass:
            self.show_pass = False
            for item in self.tree.get_children():
                values = self.tree.item(item)["values"]
                self.tree.item(item, values=(values[0], values[1], "••••••"))
        else:
            self.show_pass = True
            for item in self.tree.get_children():
                values = self.tree.item(item)["values"]
                self.tree.item(item, values=(values[0], values[1], values[2]))

    def delete_entry(self):
        selected = self.tree.selection()
        if selected:
            self.tree.delete(selected)

    def copy_password(self):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected)
            password = item["values"][2]
            self.root.clipboard_clear()
            self.root.clipboard_append(password)