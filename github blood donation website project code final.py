import tkinter as tk
from tkinter import messagebox
import json, os, webbrowser

FILE = "blood_data.json"
PASS_FILE = "admin_pass.json"
ADMIN_USER = "ssss"

VALID_BLOOD_GROUPS = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

# ------------------ LOAD PASSWORD ------------------
if os.path.exists(PASS_FILE):
    try:
        with open(PASS_FILE, "r") as f:
            ADMIN_PASS = json.load(f).get("password", "3333")
    except:
        ADMIN_PASS = "3333"
else:
    ADMIN_PASS = "3333"

# ------------------ LOAD DATA ------------------
if os.path.exists(FILE):
    try:
        with open(FILE, "r") as f:
            data = json.load(f)
    except:
        data = []
else:
    data = []

# ------------------ SAVE ------------------
def save():
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

def save_pass(p):
    with open(PASS_FILE, "w") as f:
        json.dump({"password": p}, f)

# ------------------ PLACEHOLDER FUNCTION ------------------
def add_placeholder(entry, text):
    entry.insert(0, text)
    entry.config(fg="grey")

    def on_focus_in(e):
        if entry.get() == text:
            entry.delete(0, tk.END)
            entry.config(fg="black")

    def on_focus_out(e):
        if entry.get() == "":
            entry.insert(0, text)
            entry.config(fg="grey")

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

# ------------------ ROOT ------------------
root = tk.Tk()
root.title("Blood Donor App")
root.geometry("650x750")
root.configure(bg="#ffe5b4")

def clear():
    for w in root.winfo_children():
        w.destroy()

# ------------------ HOME ------------------
def home():
    clear()
    frame = tk.Frame(root, bg="#ffe5b4")
    frame.pack(expand=True)

    tk.Label(frame, text="🩸 Blood Donor App", font=("Arial", 28, "bold"), bg="#ffe5b4").pack(pady=20)

    tk.Button(frame, text="User Access", font=("Arial", 16), bg="#ffcc99", width=20, command=user_page).pack(pady=10)
    tk.Button(frame, text="Admin Login", font=("Arial", 16), bg="#ffb366", width=20, command=admin_login).pack(pady=10)

# ------------------ USER PAGE ------------------
def user_page():
    clear()

    frame = tk.Frame(root, bg="#fff2cc")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="User Portal", font=("Arial", 24), bg="#fff2cc").pack(pady=10)

    entry = tk.Entry(frame, font=("Arial", 16))
    add_placeholder(entry, "Search Blood Group")
    entry.pack(pady=10)

    result = tk.Text(frame, height=12, font=("Arial", 14))
    result.pack(padx=10, pady=10)

    def search():
        result.delete("1.0", tk.END)
        bg = entry.get().upper()

        if bg not in VALID_BLOOD_GROUPS:
            result.insert(tk.END, "Enter valid blood group\n")
            return

        found = False
        for r in data:
            if r['blood_group'].upper() == bg:
                found = True
                result.insert(tk.END, f"Name: {r['name']}\n")
                result.insert(tk.END, f"Blood Group: {r['blood_group']}\n")
                result.insert(tk.END, f"Phone: {r['phone']}\n")
                result.insert(tk.END, f"Address: {r['address']}\n")
                result.insert(tk.END, "----------------------\n")

        if not found:
            result.insert(tk.END, "No donors found\n")

    def google():
        webbrowser.open(f"https://www.google.com/search?q={entry.get()}+blood+donors+near+me")

    tk.Button(frame, text="Search", font=("Arial", 16), bg="#99ccff", command=search).pack(pady=5)
    tk.Button(frame, text="Search Nearby", font=("Arial", 16), bg="#ff9999", command=google).pack(pady=5)
    tk.Button(frame, text="Register Yourself", font=("Arial", 16), bg="#99ff99", command=register_page).pack(pady=5)

    tk.Button(frame, text="Back", command=home).pack(pady=10)

# ------------------ REGISTER ------------------
def register_page():
    clear()

    frame = tk.Frame(root, bg="#e6ffe6")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Register Donor", font=("Arial", 24), bg="#e6ffe6").pack(pady=10)

    name = tk.Entry(frame, font=("Arial", 16))
    add_placeholder(name, "Name")
    name.pack(pady=5)

    addr = tk.Entry(frame, font=("Arial", 16))
    add_placeholder(addr, "Address")
    addr.pack(pady=5)

    phone = tk.Entry(frame, font=("Arial", 16))
    add_placeholder(phone, "Phone Number")
    phone.pack(pady=5)

    bg = tk.Entry(frame, font=("Arial", 16))
    add_placeholder(bg, "Blood Group")
    bg.pack(pady=5)

    def submit():
        n = name.get().strip()
        a = addr.get().strip()
        p = phone.get().strip()
        b = bg.get().strip().upper()

        if not n or not a or not p or not b:
            messagebox.showerror("Error", "All fields required")
            return

        if b not in VALID_BLOOD_GROUPS:
            messagebox.showerror("Error", "Invalid Blood Group")
            return

        if not p.isdigit() or len(p) != 10:
            messagebox.showerror("Error", "Phone must be 10 digits")
            return

        data.append({"name": n, "address": a, "phone": p, "blood_group": b})
        save()
        messagebox.showinfo("Success", "Registered Successfully")
        user_page()

    tk.Button(frame, text="Submit", font=("Arial", 16), bg="#66ff66", command=submit).pack(pady=10)
    tk.Button(frame, text="Back", command=user_page).pack()

# ------------------ ADMIN LOGIN ------------------
def admin_login():
    clear()

    frame = tk.Frame(root, bg="#ffd9b3")
    frame.pack(expand=True)

    tk.Label(frame, text="Admin Login", font=("Arial", 24), bg="#ffd9b3").pack(pady=20)

    user = tk.Entry(frame, font=("Arial", 16))
    add_placeholder(user, "Username")
    user.pack(pady=5)

    pwd = tk.Entry(frame, font=("Arial", 16))
    add_placeholder(pwd, "Password")

    def hide_password(e):
        if pwd.get() != "Password":
            pwd.config(show="*")

    pwd.bind("<FocusIn>", hide_password)
    pwd.pack(pady=5)

    def login():
        if user.get() == ADMIN_USER and pwd.get() == ADMIN_PASS:
            admin_panel()
        else:
            messagebox.showerror("Error", "Wrong credentials")

    tk.Button(frame, text="Login", font=("Arial", 16), bg="#ffb366", command=login).pack(pady=10)
    tk.Button(frame, text="Back", command=home).pack()

# ------------------ ADMIN PANEL ------------------
def admin_panel():
    clear()

    frame = tk.Frame(root, bg="#003366")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Admin Dashboard", font=("Arial", 24), bg="#003366", fg="yellow").pack(pady=10)

    table = tk.Frame(frame, bg="#003366")
    table.pack()

    headers = ["Name", "Blood Group", "Address", "Phone", "Actions"]

    for i, h in enumerate(headers):
        tk.Label(table, text=h, font=("Arial", 14, "bold"), bg="#003366", fg="yellow", width=15).grid(row=0, column=i)

    def refresh():
        for widget in table.winfo_children()[len(headers):]:
            widget.destroy()

        for i, r in enumerate(data, start=1):
            tk.Label(table, text=r['name'], bg="#003366", fg="white").grid(row=i, column=0)
            tk.Label(table, text=r['blood_group'], bg="#003366", fg="white").grid(row=i, column=1)
            tk.Label(table, text=r['address'], bg="#003366", fg="white").grid(row=i, column=2)
            tk.Label(table, text=r['phone'], bg="#003366", fg="white").grid(row=i, column=3)

            action = tk.Frame(table, bg="#003366")
            action.grid(row=i, column=4)

            tk.Button(action, text="Delete", bg="#ff6666",
                      command=lambda rec=r: delete_record(rec)).pack(side="left")

    def delete_record(rec):
        global data
        data = [r for r in data if r != rec]
        save()
        refresh()

    # -------- CHANGE PASSWORD --------
    def change_password():
        win = tk.Toplevel(root)
        win.title("Change Password")

        old = tk.Entry(win, font=("Arial", 14))
        add_placeholder(old, "Old Password")

        new = tk.Entry(win, font=("Arial", 14))
        add_placeholder(new, "New Password")

        def hide_old(e):
            if old.get() != "Old Password":
                old.config(show="*")

        def hide_new(e):
            if new.get() != "New Password":
                new.config(show="*")

        old.bind("<FocusIn>", hide_old)
        new.bind("<FocusIn>", hide_new)

        old.pack(pady=5)
        new.pack(pady=5)

        def update():
            global ADMIN_PASS
            if old.get() != ADMIN_PASS:
                messagebox.showerror("Error", "Wrong Old Password")
                return

            ADMIN_PASS = new.get()
            save_pass(ADMIN_PASS)
            messagebox.showinfo("Success", "Password Changed")
            win.destroy()

        tk.Button(win, text="Update Password", command=update).pack(pady=10)

    refresh()

    tk.Button(frame, text="Change Password", command=change_password).pack(pady=5)
    tk.Button(frame, text="Logout", command=home).pack(pady=10)

# ------------------ START ------------------
home()
root.mainloop()
