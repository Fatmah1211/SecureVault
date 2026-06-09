import tkinter as tk
from tkinter import ttk
import random
import string

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
            command=lambda val: self.length_label.config(text=str(int(float(val))))
        )
        self.length_slider.grid(row=2, column=0, columnspan=2, padx=20, pady=5)

        # --- Checkboxes ---
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)
        self.use_upper = tk.BooleanVar(value=True)

        tk.Checkbutton(self, text="Include Numbers (0-9)", variable=self.use_digits).grid(
            row=3, column=0, sticky="w", padx=20
        )
        tk.Checkbutton(self, text="Include Symbols (!@#...)", variable=self.use_symbols).grid(
            row=4, column=0, sticky="w", padx=20
        )
        tk.Checkbutton(self, text="Include Uppercase (A-Z)", variable=self.use_upper).grid(
            row=5, column=0, sticky="w", padx=20
        )

        # --- Generate button (placeholder for now) ---
        tk.Button(self, text="Generate Password", state="disabled").grid(
            row=6, column=0, columnspan=2, pady=10
        )

        # --- Output field ---
        tk.Label(self, text="Generated Password:").grid(row=7, column=0, sticky="w", padx=20)
        self.output_var = tk.StringVar()
        tk.Entry(self, textvariable=self.output_var, state="readonly", width=35).grid(
            row=8, column=0, columnspan=2, padx=20, pady=5
        )
