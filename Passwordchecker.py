import re
import math
import hashlib
import requests
import random
import string
import tkinter as tk
from tkinter import messagebox, ttk
import time


def generate_password(length=16):
    if length < 8:
        length = 8

    chars = (
        string.ascii_lowercase +
        string.ascii_uppercase +
        string.digits +
        "!@#$%^&*()-_=+[]{}|;:,.<>?/~"
    )

    password = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
        random.choice("!@#$%^&*()-_=+")
    ]

    password += random.choices(chars, k=length - 4)
    random.shuffle(password)

    return "".join(password)



def entropy(password):
    size = 0

    if re.search(r"[a-z]", password):
        size += 26
    if re.search(r"[A-Z]", password):
        size += 26
    if re.search(r"\d", password):
        size += 10
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        size += 32

    if size == 0:
        return 0

    return round(len(password) * math.log2(size), 2)



def check_breach(password):
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix = sha1[:5]
    suffix = sha1[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"

    try:
        r = requests.get(url)

        if r.status_code != 200:
            return "Breach check failed."

        for line in r.text.splitlines():
            h, count = line.split(":")
            if h == suffix:
                return f"⚠ Found in {count} breaches!"

        return "✔ Not found in breaches"

    except:
        return "Error checking breach database"



def strength_score(password):
    score = 0

    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1

    if re.search(r"[A-Z]", password):
        score += 1
    if re.search(r"[a-z]", password):
        score += 1
    if re.search(r"\d", password):
        score += 1
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1

    return min(score, 6)



def strength_label(score):
    if score <= 2:
        return "WEAK"
    elif score <= 4:
        return "MEDIUM"
    elif score <= 5:
        return "STRONG"
    else:
        return "VERY STRONG"



def animate_meter(target):
    progress["value"] = 0
    root.update()

    for i in range(target + 1):
        progress["value"] = i
        root.update()
        time.sleep(0.15)

   
    if target <= 2:
        progress.configure(style="Red.Horizontal.TProgressbar")
    elif target <= 4:
        progress.configure(style="Yellow.Horizontal.TProgressbar")
    else:
        progress.configure(style="Green.Horizontal.TProgressbar")



def analyze():
    pwd = entry.get()

    if not pwd:
        messagebox.showwarning("Error", "Enter a password first")
        return

    ent = entropy(pwd)
    breach = check_breach(pwd)

    score = strength_score(pwd)
    label = strength_label(score)

    animate_meter(score)

    output_text.set(
        f"Strength: {label}\n"
        f"Entropy: {ent} bits\n"
        f"Breach: {breach}"
    )



def gen_password():
    pwd = generate_password(16)

    entry.delete(0, tk.END)
    entry.config(show="")  # show generated password
    entry.insert(0, pwd)



root = tk.Tk()
root.title("Cyber Password Analyzer")
root.geometry("520x420")
root.configure(bg="black")

title = tk.Label(
    root,
    text="PASSWORD SECURITY ANALYZER",
    fg="green",
    bg="black",
    font=("Courier", 14, "bold")
)
title.pack(pady=10)

entry = tk.Entry(
    root,
    width=40,
    show="*",
    bg="black",
    fg="green",
    insertbackground="green"
)
entry.pack(pady=10)


style = ttk.Style()
style.theme_use("default")

style.configure("Red.Horizontal.TProgressbar", background="red")
style.configure("Yellow.Horizontal.TProgressbar", background="yellow")
style.configure("Green.Horizontal.TProgressbar", background="green")

progress = ttk.Progressbar(
    root,
    length=220,
    mode="determinate",
    maximum=6
)
progress.pack(pady=10)


btn_frame = tk.Frame(root, bg="black")
btn_frame.pack(pady=10)

analyze_btn = tk.Button(
    btn_frame,
    text="ANALYZE",
    command=analyze,
    bg="green",
    fg="black",
    width=18
)
analyze_btn.grid(row=0, column=0, padx=5)

gen_btn = tk.Button(
    btn_frame,
    text="GENERATE",
    command=gen_password,
    bg="green",
    fg="black",
    width=18
)
gen_btn.grid(row=0, column=1, padx=5)

output_text = tk.StringVar()

output_label = tk.Label(
    root,
    textvariable=output_text,
    fg="green",
    bg="black",
    justify="left",
    font=("Courier", 12)
)
output_label.pack(pady=20)

root.mainloop()
