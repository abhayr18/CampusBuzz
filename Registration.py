import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import sqlite3  # For database connection

# ---------------- Database Setup ----------------
def create_database():
    conn = sqlite3.connect("campusbuzz.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            urn TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

create_database()  # Run once when GUI starts

# ---------------- GUI Setup ----------------
root = tk.Tk()
root.title("CampusBuzz - Registration")
root.geometry("800x600")
root.resizable(False, False)

# ---------------- Left Frame ----------------
left_frame = tk.Frame(root, width=500, height=600)
left_frame.pack(side="left", fill="both")

# Load image
img = Image.open("campusbuzz.jpg")  
img = img.resize((500, 600))
photo = ImageTk.PhotoImage(img)
image_label = tk.Label(left_frame, image=photo)
image_label.pack(fill="both", expand=True)

# ---------------- Right Frame ----------------
right_frame = tk.Frame(root, width=300, height=600, bg="#f0f0f0")
right_frame.pack(side="right", fill="both")

form_frame = tk.Frame(right_frame, bg="#f0f0f0")
form_frame.place(relx=0.5, rely=0.5, anchor="center")

# Heading
heading = tk.Label(form_frame, text="Register to CampusBuzz",
                   font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#32CD32")
heading.pack(pady=20)

# ---------------- Form Fields ----------------
entries = {}
for field in ["Name", "URN", "Email", "Password", "Confirm Password"]:
    tk.Label(form_frame, text=f"{field}:", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(pady=5)
    show = "*" if "Password" in field else None
    entries[field] = tk.Entry(form_frame, font=("Arial", 12), show=show)
    entries[field].pack(pady=5)

# ---------------- Register Function ----------------
def register():
    name = entries["Name"].get()
    urn = entries["URN"].get()
    email = entries["Email"].get()
    password = entries["Password"].get()
    confirm = entries["Confirm Password"].get()

    # Validation
    if not all([name, urn, email, password, confirm]):
        messagebox.showerror("Error", "All fields are required!")
        return
    if password != confirm:
        messagebox.showerror("Error", "Passwords do not match!")
        return

    try:
        conn = sqlite3.connect("campusbuzz.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, urn, email, password) VALUES (?, ?, ?, ?)",
                       (name, urn, email, password))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"Registration Successful for {name}!")
        
        # Clear fields after registration
        for entry in entries.values():
            entry.delete(0, tk.END)

    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Email or URN already registered!")
    except Exception as e:
        messagebox.showerror("Error", f"Database Error: {e}")

# ---------------- Buttons ----------------
register_button = tk.Button(form_frame, text="Register", font=("Arial", 12, "bold"),
                            bg="#32CD32", fg="white", width=15, command=register)
register_button.pack(pady=20)

bottom_frame = tk.Frame(form_frame, bg="#f0f0f0")
bottom_frame.pack(pady=10)

tk.Label(bottom_frame, text="Already have an account?", font=("Arial", 10), bg="#f0f0f0").pack(side="left")

def go_to_login():
    subprocess.Popen(["python", "Login.py"])
    root.destroy()

login_button = tk.Button(bottom_frame, text="Login", font=("Arial", 10, "bold"),
                         bg="#1E90FF", fg="white", padx=10, pady=2, command=go_to_login)
login_button.pack(side="left", padx=5)

# ---------------- Run GUI ----------------
root.mainloop()
