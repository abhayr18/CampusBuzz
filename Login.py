import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import sqlite3

# ---------------- Main Window ----------------
root = tk.Tk()
root.title("CampusBuzz - Login")
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
heading = tk.Label(form_frame, text="Login to CampusBuzz",
                   font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#1E90FF")
heading.pack(pady=20)

# ---------------- Radio Buttons for Role ----------------
role_var = tk.StringVar(value="Student")
role_frame = tk.Frame(form_frame, bg="#f0f0f0")
role_frame.pack(pady=10)

student_radio = tk.Radiobutton(role_frame, text="Student", variable=role_var, value="Student",
                               font=("Arial", 12), bg="#f0f0f0")
student_radio.pack(side="left", padx=10)

admin_radio = tk.Radiobutton(role_frame, text="Admin", variable=role_var, value="Admin",
                             font=("Arial", 12), bg="#f0f0f0")
admin_radio.pack(side="left", padx=10)

# ---------------- Email & Password ----------------
email_label = tk.Label(form_frame, text="Email:", font=("Arial", 12, "bold"), bg="#f0f0f0")
email_label.pack(pady=5)
email_entry = tk.Entry(form_frame, font=("Arial", 12))
email_entry.pack(pady=5)

password_label = tk.Label(form_frame, text="Password:", font=("Arial", 12, "bold"), bg="#f0f0f0")
password_label.pack(pady=5)
password_entry = tk.Entry(form_frame, font=("Arial", 12), show="*")
password_entry.pack(pady=5)

# ---------------- Login Function ----------------
def login():
    role = role_var.get()
    email = email_entry.get()
    password = password_entry.get()

    if not email or not password:
        messagebox.showerror("Error", "All fields are required!")
        return

    # ---- Admin Login ----
    if role == "Admin":
        if email == "admin@gmail.com" and password == "admin":
            subprocess.Popen(["python", "admin_dashboard.py"])
            root.destroy()
        else:
            messagebox.showerror("Login Failed", "Invalid Admin credentials!")
        return

    # ---- Student Login ----
    try:
        conn = sqlite3.connect("campusbuzz.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM students WHERE email=? AND password=?", (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            student_id, student_name = user
            messagebox.showinfo("Login Success", f"Welcome {student_name}!")

            # Open Student Dashboard with student_id as argument
            subprocess.Popen(["python", "Student_dashboard.py", str(student_id)])
            root.destroy()
        else:
            messagebox.showerror("Login Failed", "Invalid email or password!")

    except Exception as e:
        messagebox.showerror("Error", f"Database Error: {e}")

# ---------------- Login Button ----------------
login_button = tk.Button(form_frame, text="Login", font=("Arial", 12, "bold"),
                         bg="#1E90FF", fg="white", width=15, command=login)
login_button.pack(pady=15)

# ---------------- Register Redirect ----------------
bottom_frame = tk.Frame(form_frame, bg="#f0f0f0")
bottom_frame.pack(pady=10)

tk.Label(bottom_frame, text="Don't have an account?", font=("Arial", 10), bg="#f0f0f0").pack(side="left")

def open_registration():
    subprocess.Popen(["python", "Registration.py"])
    root.destroy()

register_button = tk.Button(bottom_frame, text="Register", font=("Arial", 10, "bold"),
                            bg="#32CD32", fg="white", padx=10, pady=2, command=open_registration)
register_button.pack(side="left", padx=5)

# ---------------- Run GUI ----------------
root.mainloop()
