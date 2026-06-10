import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class VaultScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("SecureVault - Password Vault")
        self.root.geometry("800x500")

        # Title Label
        title = tk.Label(root, text="My Password Vault", font=("Arial", 18, "bold"))
        title.pack(pady=10)

        # Search Bar
        search_frame = tk.Frame(root)
        search_frame.pack(pady=5)
        tk.Label(search_frame, text="Search:").pack(side="left", padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.search_entries)
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side="left", padx=5)
        clear_btn = tk.Button(search_frame, text="Clear", bg="gray", fg="white", command=self.clear_search)
        clear_btn.pack(side="left", padx=5)

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

        # Sample Data
        self.all_data = [
            ("facebook.com", "ayesha123", "••••••"),
            ("gmail.com", "ayesha@gmail.com", "••••••"),
            ("github.com", "ayesha_dev", "••••••"),
        ]
        for item in self.all_data:
            self.tree.insert("", "end", values=item)

        # Buttons Frame
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        add_btn = tk.Button(btn_frame, text="Add Entry", width=15, bg="green", fg="white", command=self.add_entry)
        add_btn.grid(row=0, column=0, padx=10)

        delete_btn = tk.Button(btn_frame, text="Delete Entry", width=15, bg="red", fg="white", command=self.delete_entry)
        delete_btn.grid(row=0, column=1, padx=10)

        copy_btn = tk.Button(btn_frame, text="Copy Password", width=15, bg="blue", fg="white", command=self.copy_password)
        copy_btn.grid(row=0, column=2, padx=10)

        self.show_pass = False
        show_btn = tk.Button(btn_frame, text="Show Password", width=15, bg="orange", fg="white", command=self.toggle_password)
        show_btn.grid(row=0, column=3, padx=10)

    def search_entries(self, *args):
        query = self.search_var.get().lower()
        for item in self.tree.get_children():
            self.tree.delete(item)
        for entry in self.all_data:
            if query in entry[0].lower():
                self.tree.insert("", "end", values=entry)

    def clear_search(self):
        self.search_var.set("")
        for item in self.tree.get_children():
            self.tree.delete(item)
        for entry in self.all_data:
            self.tree.insert("", "end", values=entry)

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
        else:
            messagebox.showwarning("Warning", "Please select an entry to delete!")

    def copy_password(self):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected)
            password = item["values"][2]
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("Copied", "Password copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "Please select an entry first!")

    def add_entry(self):
        popup = tk.Toplevel(self.root)
        popup.title("Add New Entry")
        popup.geometry("300x200")

        tk.Label(popup, text="Website:").grid(row=0, column=0, padx=10, pady=5)
        website_entry = tk.Entry(popup, width=25)
        website_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(popup, text="Username:").grid(row=1, column=0, padx=10, pady=5)
        username_entry = tk.Entry(popup, width=25)
        username_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(popup, text="Password:").grid(row=2, column=0, padx=10, pady=5)
        password_entry = tk.Entry(popup, width=25, show="*")
        password_entry.grid(row=2, column=1, padx=10, pady=5)

        def save():
            website = website_entry.get()
            username = username_entry.get()
            password = password_entry.get()
            if website and username and password:
                self.all_data.append((website, username, password))
                self.tree.insert("", "end", values=(website, username, "••••••"))
                popup.destroy()
            else:
                messagebox.showwarning("Warning", "Please fill all fields!")

        tk.Button(popup, text="Save", bg="green", fg="white", command=save).grid(row=3, column=1, pady=10)

    def show_empty_message(self):
        if not self.tree.get_children():
            tk.Label(self.root, text="No entries found!", font=("Arial", 12), fg="gray").pack(pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = VaultScreen(root)
    root.mainloop()