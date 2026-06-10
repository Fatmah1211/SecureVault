import tkinter as tk
from tkinter import ttk
import random
import string
import pyperclip
from password_utils import generate_password, check_strength, check_hibp

class GeneratorScreen(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.build_ui()

    def build_ui(self):
        # --- Title ---
        tk.Label(self, text="Password Generator", font=("Arial", 16, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(20, 10)
        )

        # --- Length label + slider ---
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

        # --- Live character count ---
        self.char_count_label = tk.Label(
            self, text="Length: 12 characters", fg="gray", font=("Arial", 9)
        )
        self.char_count_label.grid(row=3, column=0, columnspan=2)

        # --- Checkboxes ---
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

        # --- Generate + Clear buttons side by side ---
        btn_frame = tk.Frame(self)
        btn_frame.grid(row=7, column=0, columnspan=2, pady=10)

        tk.Button(btn_frame, text="Generate Password", command=self.on_generate).pack(
            side="left", padx=10
        )
        tk.Button(btn_frame, text="Clear", command=self.clear_all, fg="red").pack(
            side="left", padx=10
        )

        # --- Output field ---
        tk.Label(self, text="Generated Password:").grid(row=8, column=0, sticky="w", padx=20)
        self.output_var = tk.StringVar()
        tk.Entry(self, textvariable=self.output_var, state="readonly", width=35).grid(
            row=9, column=0, columnspan=2, padx=20, pady=5
        )

        # --- Strength indicator ---
        tk.Label(self, text="Password Strength:").grid(row=10, column=0, sticky="w", padx=20)
        self.strength_label = tk.Label(self, text="—", font=("Arial", 11, "bold"))
        self.strength_label.grid(row=10, column=1, sticky="w")

        # --- Copy button ---
        tk.Button(self, text="Copy Password", command=self.copy_password).grid(
            row=11, column=0, columnspan=2, pady=(5, 15)
        )

        # --- Divider ---
        tk.Label(self, text="─────────────────────────────", fg="gray").grid(
            row=12, column=0, columnspan=2
        )

        # --- HIBP section ---
        tk.Label(self, text="Check if a password was leaked:", font=("Arial", 11, "bold")).grid(
            row=13, column=0, columnspan=2, pady=(10, 5)
        )

        self.check_input_var = tk.StringVar()
        tk.Entry(self, textvariable=self.check_input_var, width=35).grid(
            row=14, column=0, columnspan=2, padx=20
        )

        tk.Button(self, text="Check Password", command=self.check_breach).grid(
            row=15, column=0, columnspan=2, pady=8
        )

        self.breach_result_label = tk.Label(self, text="", font=("Arial", 10))
        self.breach_result_label.grid(row=16, column=0, columnspan=2)

    def update_length_label(self, val):
        length = int(float(val))
        self.length_label.config(text=str(length))
        self.char_count_label.config(text=f"Length: {length} characters")

    def on_generate(self):
        length = self.length_var.get()
        password = generate_password(
            length=length,
            use_digits=self.use_digits.get(),
            use_symbols=self.use_symbols.get(),
            use_upper=self.use_upper.get()
        )
        self.output_var.set(password)

        # Strength check
        strength = check_strength(password)
        colors = {"Weak": "red", "Medium": "orange", "Strong": "green"}
        self.strength_label.config(text=strength, fg=colors[strength])

    def clear_all(self):
        self.output_var.set("")
        self.strength_label.config(text="—", fg="black")
        self.check_input_var.set("")
        self.breach_result_label.config(text="")
        self.length_var.set(12)
        self.length_label.config(text="12")
        self.char_count_label.config(text="Length: 12 characters")
        self.use_digits.set(True)
        self.use_symbols.set(True)
        self.use_upper.set(True)

    def copy_password(self):
        password = self.output_var.get()
        if password:
            pyperclip.copy(password)

    def check_breach(self):
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