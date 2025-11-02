import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import sqlite3
import subprocess
import os
import sys

# ---------------- Student ID from login ----------------
try:
    student_id = int(sys.argv[1])  # Passed from login
except IndexError:
    student_id = 1  # Default student_id for testing

# ---------------- Database Connection ----------------
conn = sqlite3.connect("campusbuzz.db")
cursor = conn.cursor()

# Fetch student name for personalized greeting
cursor.execute("SELECT name FROM students WHERE id=?", (student_id,))
student = cursor.fetchone()
student_name = student[0] if student else f"Student #{student_id}"

# ---------------- Register for Event with Payment Simulation ----------------
def register_event(event_id, fee):
    pay = messagebox.askyesno("Payment", f"Do you want to pay ₹{fee:.2f} to register?")
    if not pay:
        messagebox.showinfo("Cancelled", "Registration cancelled.")
        return

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            event_id INTEGER
        )
    """)
    conn.commit()

    cursor.execute("SELECT * FROM registrations WHERE student_id=? AND event_id=?", (student_id, event_id))
    if cursor.fetchone():
        messagebox.showinfo("Already Registered", "You have already registered for this event.")
        return

    cursor.execute("INSERT INTO registrations (student_id, event_id) VALUES (?, ?)", (student_id, event_id))
    conn.commit()
    messagebox.showinfo("Registered", f"Successfully registered for the event! Fee: ₹{fee:.2f}")

# ---------------- View Event Details ----------------
def view_event_details(event):
    details_window = tk.Toplevel(root)
    details_window.title(f"Event Details - {event[1]}")
    details_window.geometry("500x500")

    tk.Label(details_window, text=event[1], font=("Arial", 18, "bold")).pack(pady=10)
    tk.Label(details_window, text=f"Category: {event[2]}", font=("Arial", 12)).pack()
    tk.Label(details_window, text=f"Date: {event[3]}", font=("Arial", 12)).pack()
    tk.Label(details_window, text=f"Fee: ₹{event[6]:.2f}", font=("Arial", 12, "bold"), fg="#1E90FF").pack(pady=5)

    # Event Image
    if event[5] and os.path.exists(event[5]):
        img = Image.open(event[5])
        img = img.resize((300, 200))
        photo = ImageTk.PhotoImage(img)
        img_label = tk.Label(details_window, image=photo)
        img_label.image = photo
        img_label.pack(pady=10)
    else:
        tk.Label(details_window, text="No Image Available", fg="gray").pack(pady=10)

    # Description
    tk.Label(details_window, text="Description:", font=("Arial", 12, "bold")).pack(anchor="w", padx=20)
    desc_box = tk.Text(details_window, wrap="word", height=8, width=55, font=("Arial", 10))
    desc_box.insert("1.0", event[4] if event[4] else "No description available.")
    desc_box.config(state="disabled", bg="#F8F8F8")
    desc_box.pack(padx=20, pady=10)

# ---------------- My Registrations ----------------
def my_registrations():
    reg_window = tk.Toplevel()
    reg_window.title("My Registrations")
    reg_window.geometry("500x400")
    
    tk.Label(reg_window, text=f"{student_name}'s Registered Events", font=("Arial", 16, "bold")).pack(pady=10)
    
    frame = tk.Frame(reg_window)
    frame.pack(fill="both", expand=True)
    
    tree = ttk.Treeview(frame, columns=("Event Name", "Category", "Date", "Fee"), show="headings")
    for col in ("Event Name", "Category", "Date", "Fee"):
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.pack(side="left", fill="both", expand=True)
    
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    
    cursor.execute("""
        SELECT e.name, e.category, e.date, e.fee
        FROM events e
        JOIN registrations r ON e.id = r.event_id
        WHERE r.student_id=?
    """, (student_id,))
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)

# ---------------- Main Window ----------------
root = tk.Tk()
root.title("CampusBuzz - Student Dashboard")
root.geometry("900x600")

# Top Banner
top_frame = tk.Frame(root, bg="#E6F0FF", height=60)
top_frame.pack(side="top", fill="x")

welcome_label = tk.Label(
    top_frame,
    text=f"Welcome {student_name} 🎓! Ready to explore and register for exciting campus events?",
    font=("Arial", 14, "bold"), bg="#E6F0FF"
)
welcome_label.pack(pady=15)

# Scrollable Frame for Events
canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Fetch Events
cursor.execute("SELECT * FROM events")
events = cursor.fetchall()

for event in events:
    frame = tk.Frame(scrollable_frame, bd=2, relief="groove", padx=10, pady=10)
    frame.pack(pady=10, padx=20, fill="x")
    
    # Event Image
    if event[5] and os.path.exists(event[5]):
        img = Image.open(event[5])
        img = img.resize((150, 100))
        photo = ImageTk.PhotoImage(img)
        img_label = tk.Label(frame, image=photo)
        img_label.image = photo
        img_label.pack(side="left", padx=10)
    else:
        tk.Label(frame, text="No Image", width=20, height=6).pack(side="left", padx=10)
    
    # Event Info
    info_frame = tk.Frame(frame)
    info_frame.pack(side="left", padx=10)
    
    tk.Label(info_frame, text=event[1], font=("Arial", 14, "bold")).pack(anchor="w")
    tk.Label(info_frame, text=f"Category: {event[2]}").pack(anchor="w")
    tk.Label(info_frame, text=f"Date: {event[3]}").pack(anchor="w")
    tk.Label(info_frame, text=f"Fee: ₹{event[6]:.2f}").pack(anchor="w")

    # Buttons side by side
    btn_frame = tk.Frame(info_frame)
    btn_frame.pack(pady=5)
    
    tk.Button(btn_frame, text="Register", bg="#32CD32", fg="white", font=("Arial", 10, "bold"),
              command=lambda e_id=event[0], f=event[6]: register_event(e_id, f)).pack(side="left", padx=5)
    
    tk.Button(btn_frame, text="View Details", bg="#1E90FF", fg="white", font=("Arial", 10, "bold"),
              command=lambda e=event: view_event_details(e)).pack(side="left", padx=5)

# Bottom Buttons
def go_to_login():
    subprocess.Popen(["python", "Login.py"])
    root.destroy()

bottom_frame = tk.Frame(root)
bottom_frame.pack(side="bottom", fill="x", pady=10)

tk.Button(bottom_frame, text="My Registrations", bg="#1E90FF", fg="white", font=("Arial", 12, "bold"),
          command=my_registrations).pack(side="left", padx=20)

tk.Button(bottom_frame, text="Logout", bg="#FF4500", fg="white", font=("Arial", 12, "bold"),
          command=go_to_login).pack(side="right", padx=20)

root.mainloop()
