# generator_screen.py
# Member 4 — Password Generator Screen
# Part of SecureVault project
# This screen handles password generation, strength checking,
# clipboard copy, breach detection via HIBP API, and password history.

import tkinter as tk
from tkinter import ttk
from password_utils import generate_password, check_strength, check_hibp


class GeneratorScreen(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.password_visible = False  # tracks show/hide state
        self.password_history = []     # stores last 5 generated passwords
        self.build_ui()

    def build_ui(self):
        # ── Title ──────────────────────────────────────────────────
        tk.Label(self, text="🔐 Password Generator", font=("Arial", 18, "bold"), fg="#2c3e50").grid(
            row=0, column=0, columnspan=2, pady=(20, 10)
        )

        # ── Length slider ──────────────────────────────────────────
        tk.Label(self, text="Password Length:").grid(row=1, column=0, sticky="w", padx=20)

        self.length_var = tk.IntVar(value=12)
        self.length_label = tk.Label(self, text="12")
        self.length_label.grid(row=1, column=1, sticky="w")

        self.length_slider = ttk.Scale(
            self, from_=8, to=32,
            variable=self.length_var,
            orient="horizontal",
            length=250,
            command=self.update_length_label
        )
        self.length_slider.grid(row=2, column=0, columnspan=2, padx=20, pady=5)

        # Live character count below slider
        self.char_count_label = tk.Label(
            self, text="Length: 12 characters", fg="gray", font=("Arial", 9)
        )
        self.char_count_label.grid(row=3, column=0, columnspan=2)

        # ── Character type options ─────────────────────────────────
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)
        self.use_upper = tk.BooleanVar(value=True)

        tk.Checkbutton(self, text="Include Numbers (0-9)", variable=self.use_digits).grid(
            row=4, column=0, sticky="w", padx=20
        )
        tk.Checkbutton(self, text="Include Symbols (!@#...)", variable=self.use_symbols).grid(
            row=5, column=0, sticky="w", padx=20
        )
        tk.Checkbutton(self, text="Include Uppercase (A-Z)", variable=self.use_upper).grid(
            row=6, column=0, sticky="w", padx=20
        )

        # ── Generate + Clear buttons ───────────────────────────────
        btn_frame = tk.Frame(self)
        btn_frame.grid(row=7, column=0, columnspan=2, pady=10)

        tk.Button(btn_frame, text="Generate Password", command=self.on_generate).pack(
            side="left", padx=10
        )
        tk.Button(btn_frame, text="Clear", command=self.clear_all, fg="red").pack(
            side="left", padx=10
        )

        # ── Output field with show/hide toggle ─────────────────────
        tk.Label(self, text="Generated Password:").grid(row=8, column=0, sticky="w", padx=20)

        output_frame = tk.Frame(self)
        output_frame.grid(row=9, column=0, columnspan=2, padx=20, pady=5)

        self.output_var = tk.StringVar()
        self.output_entry = tk.Entry(
            output_frame, textvariable=self.output_var,
            state="readonly", width=28, show="*"
        )
        self.output_entry.pack(side="left")

        self.toggle_btn = tk.Button(
            output_frame, text="Show", width=6, command=self.toggle_password_visibility
        )
        self.toggle_btn.pack(side="left", padx=(5, 0))

        # ── Strength indicator ─────────────────────────────────────
        tk.Label(self, text="Password Strength:").grid(row=10, column=0, sticky="w", padx=20)
        self.strength_label = tk.Label(self, text="—", font=("Arial", 11, "bold"))
        self.strength_label.grid(row=10, column=1, sticky="w")

        # ── Copy + Check breach buttons ────────────────────────────
        action_frame = tk.Frame(self)
        action_frame.grid(row=11, column=0, columnspan=2, pady=(5, 5))

        tk.Button(action_frame, text="Copy Password", command=self.copy_password).pack(
            side="left", padx=10
        )
        tk.Button(
            action_frame, text="Check for Breach",
            command=self.check_generated_password, fg="darkred"
        ).pack(side="left", padx=10)

        # Confirmation message shown after copying
        self.copy_confirm_label = tk.Label(self, text="", font=("Arial", 9), fg="green")
        self.copy_confirm_label.grid(row=12, column=0, columnspan=2, pady=(0, 5))

        # ── Password history (last 5) ──────────────────────────────
        tk.Label(self, text="Recent Passwords:", font=("Arial", 10, "bold")).grid(
            row=13, column=0, sticky="w", padx=20, pady=(5, 2)
        )
        self.history_listbox = tk.Listbox(
            self, height=5, width=40, font=("Courier", 9)
        )
        self.history_listbox.grid(row=14, column=0, columnspan=2, padx=20, pady=(0, 10))

        # ── Divider ────────────────────────────────────────────────
        tk.Label(self, text="─────────────────────────────", fg="gray").grid(
            row=15, column=0, columnspan=2
        )

        # ── HIBP breach check section ──────────────────────────────
        tk.Label(self, text="Check any password for leaks:", font=("Arial", 11, "bold")).grid(
            row=16, column=0, columnspan=2, pady=(10, 5)
        )

        self.check_input_var = tk.StringVar()
        tk.Entry(self, textvariable=self.check_input_var, width=35).grid(
            row=17, column=0, columnspan=2, padx=20
        )

        tk.Button(self, text="Check Password", command=self.check_breach).grid(
            row=18, column=0, columnspan=2, pady=8
        )

        self.breach_result_label = tk.Label(self, text="", font=("Arial", 10))
        self.breach_result_label.grid(row=19, column=0, columnspan=2)

    # ── Methods ────────────────────────────────────────────────────

    def update_length_label(self, val):
        # Updates the length number and character count label as slider moves
        length = int(float(val))
        self.length_label.config(text=str(length))
        self.char_count_label.config(text=f"Length: {length} characters")

    def toggle_password_visibility(self):
        # Toggles between showing and hiding the generated password
        if self.password_visible:
            self.output_entry.config(show="*")
            self.toggle_btn.config(text="Show")
            self.password_visible = False
        else:
            self.output_entry.config(show="")
            self.toggle_btn.config(text="Hide")
            self.password_visible = True

    def on_generate(self):
        # Validates options then generates a password
        if not self.use_digits.get() and not self.use_symbols.get() and not self.use_upper.get():
            self.strength_label.config(text="Select at least one option!", fg="red")
            return

        length = self.length_var.get()
        password = generate_password(
            length=length,
            use_digits=self.use_digits.get(),
            use_symbols=self.use_symbols.get(),
            use_upper=self.use_upper.get()
        )
        self.output_var.set(password)

        # Reset to hidden on each new generation
        self.output_entry.config(show="*")
        self.toggle_btn.config(text="Show")
        self.password_visible = False

        # Update strength indicator
        strength = check_strength(password)
        colors = {"Weak": "#e74c3c", "Medium": "#f39c12", "Strong": "#27ae60"}
        self.strength_label.config(text=strength, fg=colors[strength])

        # Clear previous breach result
        self.breach_result_label.config(text="")

        # Add to history and keep only last 5
        self.password_history.insert(0, password)
        self.password_history = self.password_history[:5]
        self.update_history()

    def update_history(self):
        # Refreshes the history listbox with latest passwords (shown as asterisks)
        self.history_listbox.delete(0, tk.END)
        for pwd in self.password_history:
            self.history_listbox.insert(tk.END, "*" * len(pwd))

    def clear_all(self):
        # Resets all fields and state back to default
        self.output_var.set("")
        self.output_entry.config(show="*")
        self.toggle_btn.config(text="Show")
        self.password_visible = False
        self.strength_label.config(text="—", fg="black")
        self.copy_confirm_label.config(text="")
        self.check_input_var.set("")
        self.breach_result_label.config(text="")
        self.length_var.set(12)
        self.length_label.config(text="12")
        self.char_count_label.config(text="Length: 12 characters")
        self.use_digits.set(True)
        self.use_symbols.set(True)
        self.use_upper.set(True)
        self.password_history = []
        self.history_listbox.delete(0, tk.END)

    def copy_password(self):
        # Copies generated password to clipboard and shows confirmation
        password = self.output_var.get()
        if password:
            self.clipboard_clear()
            self.clipboard_append(password)
            self.update()
            self.copy_confirm_label.config(text="✔ Copied to clipboard!", fg="green")
            self.after(2000, lambda: self.copy_confirm_label.config(text=""))

    def check_generated_password(self):
        # Sends the generated password directly to the breach check
        password = self.output_var.get()
        if not password:
            self.breach_result_label.config(
                text="Generate a password first.", fg="gray"
            )
            return
        self.check_input_var.set(password)
        self.check_breach()

    def check_breach(self):
        # Checks any password against the HaveIBeenPwned API
        password = self.check_input_var.get().strip()

        if not password:
            self.breach_result_label.config(
                text="Please enter a password to check.", fg="gray"
            )
            return

        self.breach_result_label.config(text="Checking...", fg="gray")
        self.update()

        result = check_hibp(password)

        if result == "error":
            self.breach_result_label.config(
                text="API error. Try again later.", fg="orange"
            )
        elif result == "offline":
            self.breach_result_label.config(
                text="No internet connection.", fg="orange"
            )
        elif result == 0:
            self.breach_result_label.config(
                text="✔ This password has not been leaked!", fg="green"
            )
        else:
            self.breach_result_label.config(
                text=f"⚠ WARNING: Found {result} times in data breaches!", fg="red"
            )