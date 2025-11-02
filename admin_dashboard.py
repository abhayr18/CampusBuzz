import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import os

# ----------------- Main Window -----------------
root = tk.Tk()
root.title("CampusBuzz - Admin Dashboard")
root.geometry("800x600")
root.resizable(False, False)

# ----------------- Top Banner -----------------
top_frame = tk.Frame(root, bg="#E6F0FF", height=60)
top_frame.pack(side="top", fill="x")

welcome_label = tk.Label(top_frame, text="🎉 Welcome back, Admin! Let’s create something exciting today.",
                         font=("Arial", 14, "bold"), bg="#E6F0FF")
welcome_label.pack(pady=15)

# ----------------- Main Buttons Section -----------------
main_frame = tk.Frame(root, bg="#ffffff")
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

# ---------- Add New Event Section ----------
add_img = Image.open("add_event.png") 
add_img = add_img.resize((150, 150))
add_photo = ImageTk.PhotoImage(add_img)

add_frame = tk.Frame(main_frame, bg="#ffffff")
add_frame.pack(side="left", expand=True, padx=20)

add_label = tk.Label(add_frame, image=add_photo, bg="#ffffff")
add_label.pack(pady=10)

def add_event():
    # Run AddEvent.py
    script_path = os.path.join(os.getcwd(), "AddEvent.py")
    subprocess.Popen(["python", script_path])

add_button = tk.Button(add_frame, text="Add New Event", font=("Arial", 12, "bold"),
                       bg="#32CD32", fg="white", width=18, command=add_event)
add_button.pack(pady=10)

# ---------- View All Events Section ----------
view_img = Image.open("view_events.png")  
view_img = view_img.resize((150, 150))
view_photo = ImageTk.PhotoImage(view_img)

view_frame = tk.Frame(main_frame, bg="#ffffff")
view_frame.pack(side="right", expand=True, padx=20)

view_label = tk.Label(view_frame, image=view_photo, bg="#ffffff")
view_label.pack(pady=10)

def view_events():
    # Run view_all_events.py
    script_path = os.path.join(os.getcwd(), "view_all_events.py")
    subprocess.Popen(["python", script_path])

view_button = tk.Button(view_frame, text="View All Events", font=("Arial", 12, "bold"),
                        bg="#1E90FF", fg="white", width=18, command=view_events)
view_button.pack(pady=10)

# ----------------- Logout Button -----------------
logout_frame = tk.Frame(root, bg="#ffffff")
logout_frame.pack(side="bottom", fill="x", pady=10)

def logout():
    messagebox.showinfo("Logout", "Logging out...")
    subprocess.Popen(["python", "Login.py"])
    root.destroy()

logout_button = tk.Button(logout_frame, text="Logout", font=("Arial", 12, "bold"),
                          bg="#1E90FF", fg="white", width=15, command=logout)
logout_button.pack(pady=10)

# ----------------- Run the GUI -----------------
root.mainloop()
