import tkinter as tk
import tkinter as tk
from tkinter import ttk
from securevault.database import get_passwords, delete_password
from securevault.encryption import decrypt_password

class VaultScreen:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.real_passwords = {}
        self.root.title("SecureVault - Password Vault")
        self.root.geometry("900x600")
        self.root.config(bg="#1e1e2e")

        # Header
        header = tk.Frame(root, bg="#313244", pady=15)
        header.pack(fill="x")
        tk.Label(header, text="🔐 SecureVault", font=("Arial", 24, "bold"), bg="#313244", fg="#cba6f7").pack()
        tk.Label(header, text="Your passwords, safe and secure", font=("Arial", 11), bg="#313244", fg="#a6adc8").pack()

        # Search Bar
        search_frame = tk.Frame(root, bg="#1e1e2e")
        search_frame.pack(pady=15)
        tk.Label(search_frame, text="🔍", bg="#1e1e2e", fg="#cba6f7", font=("Arial", 13)).pack(side="left", padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.search_entries)
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=35,
                                font=("Arial", 11), bg="#313244", fg="#cdd6f4",
                                insertbackground="white", relief="flat", bd=8)
        search_entry.pack(side="left", padx=5)
        tk.Button(search_frame, text="Clear", bg="#45475a", fg="white",
                  font=("Arial", 10), relief="flat", padx=10,
                  command=self.clear_search).pack(side="left", padx=5)

        # Table Frame
        table_frame = tk.Frame(root, bg="#1e1e2e")
        table_frame.pack(pady=5, fill="both", expand=True, padx=20)

        # Treeview Style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#313244",
                        foreground="#cdd6f4",
                        rowheight=32,
                        fieldbackground="#313244",
                        font=("Arial", 11))
        style.configure("Treeview.Heading",
                        background="#45475a",
                        foreground="#cba6f7",
                        font=("Arial", 12, "bold"),
                        relief="flat")
        style.map("Treeview", background=[("selected", "#585b70")])

        self.tree = ttk.Treeview(table_frame, columns=("Website", "Username", "Password"), show="headings")
        self.tree.heading("Website", text="🌐  Website")
        self.tree.heading("Username", text="👤  Username")
        self.tree.heading("Password", text="🔑  Password")
        self.tree.column("Website", width=250)
        self.tree.column("Username", width=250)
        self.tree.column("Password", width=250)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Sample Data
        self.all_data = []
        # Buttons Row 1
        btn_frame1 = tk.Frame(root, bg="#1e1e2e")
        btn_frame1.pack(pady=8)

        buttons1 = [
            ("➕ Add Entry", "#a6e3a1", "#1e1e2e", self.add_entry),
            ("🗑 Delete", "#f38ba8", "#1e1e2e", self.delete_entry),
            ("📋 Copy", "#89b4fa", "#1e1e2e", self.copy_password),
            ("✏️ Edit", "#89dceb", "#1e1e2e", self.edit_entry),
            ("👁 Show/Hide", "#fab387", "#1e1e2e", self.toggle_password),
        ]
        for text, bg, fg, cmd in buttons1:
            tk.Button(btn_frame1, text=text, bg=bg, fg=fg,
                      font=("Arial", 10, "bold"), relief="flat",
                      padx=12, pady=6, command=cmd).pack(side="left", padx=6)

        # Buttons Row 2
        btn_frame2 = tk.Frame(root, bg="#1e1e2e")
        btn_frame2.pack(pady=5)

        buttons2 = [
            ("🔤 Sort A-Z", "#cba6f7", "#1e1e2e", self.sort_by_website),
            ("🔢 Total Entries", "#a6e3a1", "#1e1e2e", self.count_entries),
            ("💾 Export", "#f9e2af", "#1e1e2e", self.export_entries),
            ("🗑 Clear All", "#f38ba8", "#1e1e2e", self.clear_all_entries),
        ]
        for text, bg, fg, cmd in buttons2:
            tk.Button(btn_frame2, text=text, bg=bg, fg=fg,
                      font=("Arial", 10, "bold"), relief="flat",
                      padx=12, pady=6, command=cmd).pack(side="left", padx=6)

        gen_btn = tk.Button(btn_frame2, text="🔑 Generator", bg="#cba6f7", fg="#1e1e2e",
                  font=("Arial", 10, "bold"), relief="flat",
                  padx=12, pady=6, command=self.open_generator)
        gen_btn.pack(side="left", padx=6)
        about_btn = tk.Button(btn_frame2, text="ℹ️ About", bg="#74c7ec", fg="#1e1e2e",
                  font=("Arial", 10, "bold"), relief="flat",
                  padx=12, pady=6, command=self.show_about)
        about_btn.pack(side="left", padx=6)

        # Footer
        tk.Label(root, text="🔒 All passwords are encrypted and stored locally",
                 bg="#1e1e2e", fg="#585b70", font=("Arial", 9)).pack(pady=8)

    def search_entries(self, *args):
        query = self.search_var.get().lower()
        for item in self.tree.get_children():
            self.tree.delete(item)
        for entry in self.all_data:
            if query in entry[0].lower():
                self.tree.insert("", "end", values=(entry[0], entry[1], "••••••"))

    def clear_search(self):
        self.search_var.set("")
        self.refresh_table()

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for entry in self.all_data:
            self.tree.insert("", "end", values=(entry[0], entry[1], "••••••"))

    def toggle_password(self):
        if not hasattr(self, 'show_pass'):
            self.show_pass = False
        if self.show_pass:
            self.show_pass = False
            for item in self.tree.get_children():
                values = self.tree.item(item)["values"]
                self.tree.item(item, values=(values[0], values[1], "••••••"))
        else:
            self.show_pass = True
            for item in self.tree.get_children():
                values = self.tree.item(item)["values"]
                idx = [d[0] for d in self.all_data].index(values[0])
                self.tree.item(item, values=(values[0], values[1], self.all_data[idx][2]))

    def delete_entry(self):
        selected = self.tree.selection()
        if selected:
            confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this entry?")
            if confirm:
                self.tree.delete(selected)
        else:
            messagebox.showwarning("Warning", "Please select an entry to delete!")

    def copy_password(self):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected)
            website = item["values"][0]
            idx = [d[0] for d in self.all_data].index(website)
            real_password = self.all_data[idx][2]
            self.root.clipboard_clear()
            self.root.clipboard_append(real_password)
            messagebox.showinfo("Copied", "Password copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "Please select an entry first!")

    def add_entry(self):
        popup = tk.Toplevel(self.root)
        popup.title("Add New Entry")
        popup.geometry("350x250")
        popup.config(bg="#1e1e2e")

        tk.Label(popup, text="Add New Password", font=("Arial", 14, "bold"),
                 bg="#1e1e2e", fg="#cba6f7").grid(row=0, columnspan=2, pady=10)

        for i, label in enumerate(["🌐 Website:", "👤 Username:", "🔑 Password:"]):
            tk.Label(popup, text=label, bg="#1e1e2e", fg="#cdd6f4",
                     font=("Arial", 11)).grid(row=i+1, column=0, padx=15, pady=8)

        website_entry = tk.Entry(popup, width=22, font=("Arial", 11),
                                 bg="#313244", fg="#cdd6f4", insertbackground="white", relief="flat", bd=6)
        website_entry.grid(row=1, column=1, padx=10, pady=8)

        username_entry = tk.Entry(popup, width=22, font=("Arial", 11),
                                  bg="#313244", fg="#cdd6f4", insertbackground="white", relief="flat", bd=6)
        username_entry.grid(row=2, column=1, padx=10, pady=8)

        password_entry = tk.Entry(popup, width=22, show="*", font=("Arial", 11),
                                  bg="#313244", fg="#cdd6f4", insertbackground="white", relief="flat", bd=6)
        password_entry.grid(row=3, column=1, padx=10, pady=8)

        def save():
            website = website_entry.get()
            username = username_entry.get()
            password = password_entry.get()
            if website and username and password:
                from securevault.database import save_password
                from securevault.encryption import encrypt_password
                if hasattr(self, 'user_id') and self.user_id:
                    encrypted = encrypt_password(password)
                    save_password(self.user_id, website, username, encrypted, 'General')
                self.all_data.append((website, username, password, 'General'))
                self.refresh_table()
                popup.destroy()
            else:
                messagebox.showwarning("Warning", "Please fill all fields!")

        tk.Button(popup, text="💾 Save", bg="#a6e3a1", fg="#1e1e2e",
                  font=("Arial", 11, "bold"), relief="flat", padx=15, pady=5,
                  command=save).grid(row=4, column=1, pady=12)

    def edit_entry(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an entry to edit!")
            return
        item = self.tree.item(selected)
        old_website = item["values"][0]
        old_username = item["values"][1]
        idx = [d[0] for d in self.all_data].index(old_website)
        old_password = self.all_data[idx][2]

        popup = tk.Toplevel(self.root)
        popup.title("Edit Entry")
        popup.geometry("350x250")
        popup.config(bg="#1e1e2e")

        tk.Label(popup, text="Edit Password", font=("Arial", 14, "bold"),
                 bg="#1e1e2e", fg="#89dceb").grid(row=0, columnspan=2, pady=10)

        for i, label in enumerate(["🌐 Website:", "👤 Username:", "🔑 Password:"]):
            tk.Label(popup, text=label, bg="#1e1e2e", fg="#cdd6f4",
                     font=("Arial", 11)).grid(row=i+1, column=0, padx=15, pady=8)

        website_entry = tk.Entry(popup, width=22, font=("Arial", 11),
                                 bg="#313244", fg="#cdd6f4", insertbackground="white", relief="flat", bd=6)
        website_entry.insert(0, old_website)
        website_entry.grid(row=1, column=1, padx=10, pady=8)

        username_entry = tk.Entry(popup, width=22, font=("Arial", 11),
                                  bg="#313244", fg="#cdd6f4", insertbackground="white", relief="flat", bd=6)
        username_entry.insert(0, old_username)
        username_entry.grid(row=2, column=1, padx=10, pady=8)

        password_entry = tk.Entry(popup, width=22, show="*", font=("Arial", 11),
                                  bg="#313244", fg="#cdd6f4", insertbackground="white", relief="flat", bd=6)
        password_entry.insert(0, old_password)
        password_entry.grid(row=3, column=1, padx=10, pady=8)

        def update():
            new_website = website_entry.get()
            new_username = username_entry.get()
            new_password = password_entry.get()
            if new_website and new_username and new_password:
                self.all_data[idx] = (new_website, new_username, new_password)
                self.refresh_table()
                popup.destroy()
            else:
                messagebox.showwarning("Warning", "Please fill all fields!")

        tk.Button(popup, text="✅ Update", bg="#89dceb", fg="#1e1e2e",
                  font=("Arial", 11, "bold"), relief="flat", padx=15, pady=5,
                  command=update).grid(row=4, column=1, pady=12)

    def sort_by_website(self):
        self.all_data.sort(key=lambda x: x[0].lower())
        self.refresh_table()

    def count_entries(self):
        total = len(self.all_data)
        messagebox.showinfo("Total Entries", f"You have {total} saved password(s) in your vault!")

    def export_entries(self):
        if not self.all_data:
            messagebox.showwarning("Warning", "No entries to export!")
            return
        with open("vault_export.txt", "w") as f:
            f.write("SecureVault Export\n")
            f.write("==================\n")
            for entry in self.all_data:
                f.write(f"Website: {entry[0]}\n")
                f.write(f"Username: {entry[1]}\n")
                f.write(f"Password: {entry[2]}\n")
                f.write("------------------\n")
        messagebox.showinfo("Success", "Passwords exported to vault_export.txt!")

    def clear_all_entries(self):
        if not self.all_data:
            messagebox.showwarning("Warning", "Vault is already empty!")
            return
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to clear ALL entries?")
        if confirm:
            self.all_data.clear()
            self.refresh_table()
            messagebox.showinfo("Done", "All entries cleared!")

    def open_generator(self):
        import importlib
        import generator_screen
        win = tk.Toplevel(self.root)
        win.title("Password Generator")
        win.geometry("420x550")
        win.config(bg="#1e1e2e")
        app = generator_screen.GeneratorScreen(win)
        app.pack(fill="both", expand=True)

    def show_about(self):
        messagebox.showinfo("About SecureVault",
            "SecureVault v1.0\n\nA secure password manager.\nAll passwords stored locally.\n\nDeveloped by Team SecureVault.")

    def show_empty_message(self):
        if not self.tree.get_children():
            tk.Label(self.root, text="No entries found!", font=("Arial", 12),
                     fg="#585b70", bg="#1e1e2e").pack(pady=5)

    def filter_by_category(self, category):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for entry in self.all_data:
            if category == "All" or (len(entry) > 3 and entry[3] == category):
                self.tree.insert("", "end", values=entry)

    def add_category_dropdown(self):
        category_frame = tk.Frame(self.root, bg="#f0f0f0")
        category_frame.pack(pady=5)
        tk.Label(category_frame, text="Category:", bg="#f0f0f0", font=("Arial", 11)).pack(side="left", padx=5)
        self.category_var = tk.StringVar(value="All")
        category_menu = ttk.Combobox(category_frame, textvariable=self.category_var,
            values=["All", "Social Media", "Banking", "Email", "Work", "Other"], width=15)
        category_menu.pack(side="left", padx=5)
        category_menu.bind("<<ComboboxSelected>>", lambda e: self.filter_by_category(self.category_var.get()))
if __name__ == "__main__":
    root = tk.Tk()
    app = VaultScreen(root)
    root.mainloop()
def open_vault(username):
    from securevault.database import get_passwords, save_password, get_connection
    from securevault.encryption import encrypt_password, decrypt_password

    root = tk.Tk()
    app = VaultScreen(root)
    app.username = username

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    app.user_id = user[0] if user else None

    app.all_data = []
    if app.user_id:
        passwords = get_passwords(app.user_id)
        for p in passwords:
            decrypted = decrypt_password(p[3])
            app.all_data.append((p[1], p[2], decrypted, p[4]))
        app.refresh_table()

    def new_add_entry():
        popup = tk.Toplevel(root)
        popup.title("Add New Entry")
        popup.geometry("350x250")
        popup.config(bg="#1e1e2e")
        tk.Label(popup, text="Add New Password", font=("Arial", 14, "bold"), bg="#1e1e2e", fg="#cba6f7").grid(row=0, columnspan=2, pady=10)
        for i, label in enumerate(["Website:", "Username:", "Password:"]):
            tk.Label(popup, text=label, bg="#1e1e2e", fg="#cdd6f4", font=("Arial", 11)).grid(row=i+1, column=0, padx=15, pady=8)
        website_entry = tk.Entry(popup, width=22, font=("Arial", 11), bg="#313244", fg="#cdd6f4", insertbackground="white", relief="flat", bd=6)
        website_entry.grid(row=1, column=1, padx=10, pady=8)
        username_entry = tk.Entry(popup, width=22, font=("Arial", 11), bg="#313244", fg="#cdd6f4", insertbackground="white", relief="flat", bd=6)
        username_entry.grid(row=2, column=1, padx=10, pady=8)
        password_entry = tk.Entry(popup, width=22, show="*", font=("Arial", 11), bg="#313244", fg="#cdd6f4", insertbackground="white", relief="flat", bd=6)
        password_entry.grid(row=3, column=1, padx=10, pady=8)
        def save():
            website = website_entry.get()
            uname = username_entry.get()
            password = password_entry.get()
            if website and uname and password:
                encrypted = encrypt_password(password)
                save_password(app.user_id, website, uname, encrypted, 'General')
                app.all_data.append((website, uname, password, 'General'))
                app.refresh_table()
                popup.destroy()
            else:
                messagebox.showwarning("Warning", "Please fill all fields!")
        tk.Button(popup, text="Save", bg="#a6e3a1", fg="#1e1e2e", font=("Arial", 11, "bold"), relief="flat", padx=15, pady=5, command=save).grid(row=4, column=1, pady=12)

    app.add_entry = new_add_entry
    root.mainloop()