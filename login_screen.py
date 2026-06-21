import tkinter as tk
from tkinter import messagebox
import password_utils as vu
import vault_screen

# ── Cyber-Sec Design Tokens ─────────────────────────────────────────
BG          = "#080c10"   # near-black, terminal void
PANEL       = "#0d1318"   # slightly lifted panel
FIELD       = "#111922"   # input field background
BORDER      = "#1c2730"   # hairline borders / dividers
BORDER_LIT  = "#1fd9a8"   # active border glow
ACCENT      = "#1fd9a8"   # signal green — primary accent
ACCENT_DIM  = "#13301f"   # accent used as a quiet fill
TEXT_MAIN   = "#e6f1ee"   # near-white, slight green cast
TEXT_MUTED  = "#5b7269"   # muted green-grey for secondary text
TEXT_GHOST  = "#33433d"   # faint labels / placeholders
DANGER      = "#ff5d6c"   # error red
MONO        = "Consolas"  # monospace for terminal feel
SANS        = "Segoe UI"  # clean sans for body text

root = tk.Tk()
root.title("SecureVault - Password Manager")

window_width = 420
window_height = 600

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
root.resizable(False, False)
root.configure(bg=BG)

# ── Top accent rule — the signature element ─────────────────────────
tk.Frame(root, bg=ACCENT, height=3).pack(fill="x", side="top")

# ── Header block ─────────────────────────────────────────────────────
header = tk.Frame(root, bg=BG)
header.pack(fill="x", pady=(34, 18))

brand_row = tk.Frame(header, bg=BG)
brand_row.pack()
tk.Label(brand_row, text="⛨", font=(SANS, 20), bg=BG, fg=ACCENT).pack(side="left", padx=(0, 8))
tk.Label(brand_row, text="SECUREVAULT", font=(MONO, 22, "bold"), bg=BG, fg=TEXT_MAIN).pack(side="left")

tk.Label(header, text="ENCRYPTED CREDENTIAL STORE", font=(MONO, 9), bg=BG, fg=TEXT_MUTED).pack(pady=(4, 0))

# thin divider under header
tk.Frame(root, bg=BORDER, height=1).pack(fill="x", padx=40, pady=(14, 0))

# --- Tab buttons ---
tab_frame = tk.Frame(root, bg=BG)
tab_frame.pack(pady=(22, 0))

def show_login():
    login_frame.pack(pady=4)
    register_frame.pack_forget()
    login_tab_btn.config(bg=ACCENT, fg=BG)
    register_tab_btn.config(bg=PANEL, fg=TEXT_MUTED)
    clear_errors()
    root.bind("<Return>", lambda event: login_clicked())

def show_register():
    register_frame.pack(pady=4)
    login_frame.pack_forget()
    register_tab_btn.config(bg=ACCENT, fg=BG)
    login_tab_btn.config(bg=PANEL, fg=TEXT_MUTED)
    clear_errors()
    root.bind("<Return>", lambda event: register_clicked())

def clear_errors(event=None):
    login_error_label.config(text="")
    reg_error_label.config(text="")

login_tab_btn = tk.Button(tab_frame, text="LOGIN", width=16, font=(MONO, 10, "bold"),
                           bg=ACCENT, fg=BG, relief="flat", bd=0, cursor="hand2",
                           activebackground=ACCENT, activeforeground=BG, command=show_login)
login_tab_btn.grid(row=0, column=0, padx=(0, 2))

register_tab_btn = tk.Button(tab_frame, text="REGISTER", width=16, font=(MONO, 10, "bold"),
                              bg=PANEL, fg=TEXT_MUTED, relief="flat", bd=0, cursor="hand2",
                              activebackground=PANEL, activeforeground=TEXT_MAIN, command=show_register)
register_tab_btn.grid(row=0, column=1, padx=(2, 0))

# ── Helper to build a labeled, underline-style field ────────────────
def build_field(parent, label_text):
    wrap = tk.Frame(parent, bg=BG)
    wrap.pack(pady=(16, 0))
    tk.Label(wrap, text=label_text, font=(MONO, 9, "bold"), bg=BG, fg=TEXT_MUTED, anchor="w").pack(fill="x")
    field_box = tk.Frame(wrap, bg=FIELD, highlightthickness=1, highlightbackground=BORDER, highlightcolor=BORDER_LIT)
    field_box.pack(fill="x", pady=(6, 0))
    return wrap, field_box

def make_entry(field_box, show=None):
    entry = tk.Entry(field_box, font=(SANS, 12), bg=FIELD, fg=TEXT_MAIN,
                      insertbackground=ACCENT, relief="flat", bd=0, show=show)
    entry.pack(fill="x", padx=12, pady=10)
    return entry

# --- Login Frame ---
login_frame = tk.Frame(root, bg=BG, width=320)

login_user_wrap, login_user_box = build_field(login_frame, "USERNAME")
login_user_wrap.configure(width=320)
username_entry = make_entry(login_user_box)
username_entry.bind("<Key>", clear_errors)

login_pass_wrap, login_pass_box = build_field(login_frame, "PASSWORD")
password_entry = make_entry(login_pass_box, show="•")
password_entry.bind("<Key>", clear_errors)

login_error_label = tk.Label(login_frame, text="", font=(SANS, 9), bg=BG, fg=DANGER)
login_error_label.pack(pady=(10, 0))

def login_clicked():
    username = username_entry.get().strip()
    password = password_entry.get()
    if not username or not password:
        login_error_label.config(text="⚠ Username and password are required.")
        return

    success, message = vu.login_user(username, password)
    if success:
        user_id = message  # message variable holds the user_id integer when successful
        root.destroy()
        vault_screen.open_vault(user_id)
    else:
        login_error_label.config(text="⚠ Invalid username or password.")

login_btn = tk.Button(login_frame, text="UNLOCK VAULT", font=(MONO, 11, "bold"),
                       bg=ACCENT, fg=BG, width=28, relief="flat", bd=0, pady=10,
                       cursor="hand2", activebackground="#17b58c", activeforeground=BG,
                       command=login_clicked)
login_btn.pack(pady=(20, 0))

# --- Register Frame ---
register_frame = tk.Frame(root, bg=BG, width=320)

reg_user_wrap, reg_user_box = build_field(register_frame, "USERNAME")
reg_username_entry = make_entry(reg_user_box)
reg_username_entry.bind("<Key>", clear_errors)

reg_pass_wrap, reg_pass_box = build_field(register_frame, "PASSWORD")
reg_password_entry = make_entry(reg_pass_box, show="•")
reg_password_entry.bind("<Key>", clear_errors)

reg_confirm_wrap, reg_confirm_box = build_field(register_frame, "CONFIRM PASSWORD")
reg_confirm_entry = make_entry(reg_confirm_box, show="•")
reg_confirm_entry.bind("<Key>", clear_errors)

reg_error_label = tk.Label(register_frame, text="", font=(SANS, 9), bg=BG, fg=DANGER)
reg_error_label.pack(pady=(10, 0))

def register_clicked():
    username = reg_username_entry.get().strip()
    password = reg_password_entry.get()
    confirm_password = reg_confirm_entry.get()

    if not username or not password or not confirm_password:
        reg_error_label.config(text="⚠ All fields are required.")
        return
    if password != confirm_password:
        reg_error_label.config(text="⚠ Passwords do not match.")
        return

    success, message = vu.register_user(username, password)
    if success:
        messagebox.showinfo("Success", "Account created successfully! Please log in.")
        show_login()
    else:
        reg_error_label.config(text=f"⚠ {message}")

register_btn = tk.Button(register_frame, text="CREATE ACCOUNT", font=(MONO, 11, "bold"),
                          bg=ACCENT, fg=BG, width=28, relief="flat", bd=0, pady=10,
                          cursor="hand2", activebackground="#17b58c", activeforeground=BG,
                          command=register_clicked)
register_btn.pack(pady=(20, 0))

# ── Footer ───────────────────────────────────────────────────────────
footer = tk.Frame(root, bg=BG)
footer.pack(side="bottom", fill="x", pady=(0, 22))
tk.Frame(footer, bg=BORDER, height=1).pack(fill="x", padx=40, pady=(0, 10))
tk.Label(footer, text="🔒 AES-grade local encryption · zero plaintext storage",
          font=(MONO, 8), bg=BG, fg=TEXT_GHOST).pack()

show_login()
root.mainloop()
