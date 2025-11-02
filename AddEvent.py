import tkinter as tk
from tkinter import filedialog, messagebox
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import sqlite3
import shutil
import os
import re

# ---------- Helpers ----------
def sanitize_filename(name):
    """Return a safe filename from event name keeping original extension later."""
    # remove non-alphanumeric, replace spaces with underscore, lowercase
    s = re.sub(r'[^A-Za-z0-9 _-]', '', name)
    s = s.strip().replace(' ', '_').lower()
    return s if s else "event"

# ---------- Ensure event_images folder exists ----------
if not os.path.exists("event_images"):
    os.makedirs("event_images")

# ---------- Database Setup (robust) ----------
DB_PATH = "campusbuzz.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create events table if not exists (full schema)
cursor.execute("""
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    date TEXT NOT NULL,
    description TEXT,
    image TEXT,
    fee REAL DEFAULT 0
)
""")
conn.commit()

# Check if 'fee' column exists; add if missing (migration)
cursor.execute("PRAGMA table_info(events)")
cols = [row[1] for row in cursor.fetchall()]  # row[1] is column name
if "fee" not in cols:
    try:
        cursor.execute("ALTER TABLE events ADD COLUMN fee REAL DEFAULT 0")
        conn.commit()
    except Exception as e:
        # If ALTER fails for some reason, show warning but continue
        print("Warning: could not alter table to add fee column:", e)

# ---------- Main Window ----------
root = tk.Tk()
root.title("Add New Event - CampusBuzz")
root.geometry("700x650")
root.config(bg="#f0f0f0")

# ---------- Heading ----------
heading = tk.Label(root, text="Add New Event", font=("Arial", 20, "bold"), fg="#1E90FF", bg="#f0f0f0")
heading.pack(pady=20)

# ---------- Form Frame ----------
form_frame = tk.Frame(root, bg="#f0f0f0")
form_frame.pack(pady=10)

# ---------- Event Name ----------
tk.Label(form_frame, text="Event Name:", font=("Arial", 12, "bold"), bg="#f0f0f0").grid(row=0, column=0, sticky="w", pady=5)
event_name_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
event_name_entry.grid(row=0, column=1, pady=5)

# ---------- Category ----------
tk.Label(form_frame, text="Category:", font=("Arial", 12, "bold"), bg="#f0f0f0").grid(row=1, column=0, sticky="w", pady=5)
category_var = tk.StringVar(value="Technical")
category_menu = tk.OptionMenu(form_frame, category_var, "Technical", "Cultural", "Sports", "Workshop", "Seminar", "Other")
category_menu.config(font=("Arial", 12), width=27)
category_menu.grid(row=1, column=1, pady=5)

# ---------- Date ----------
tk.Label(form_frame, text="Event Date:", font=("Arial", 12, "bold"), bg="#f0f0f0").grid(row=2, column=0, sticky="w", pady=5)
date_picker = DateEntry(form_frame, font=("Arial", 12), width=28, background="#1E90FF", foreground="white", date_pattern='yyyy-mm-dd')
date_picker.grid(row=2, column=1, pady=5)

# ---------- Description ----------
tk.Label(form_frame, text="Description:", font=("Arial", 12, "bold"), bg="#f0f0f0").grid(row=3, column=0, sticky="nw", pady=5)
desc_text = tk.Text(form_frame, font=("Arial", 12), width=30, height=5)
desc_text.grid(row=3, column=1, pady=5)

# ---------- Registration Fee ----------
tk.Label(form_frame, text="Registration Fee:", font=("Arial", 12, "bold"), bg="#f0f0f0").grid(row=4, column=0, sticky="w", pady=5)
fee_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
fee_entry.grid(row=4, column=1, pady=5)

# ---------- Image Upload ----------
tk.Label(form_frame, text="Upload Image:", font=("Arial", 12, "bold"), bg="#f0f0f0").grid(row=5, column=0, sticky="w", pady=5)
image_path_var = tk.StringVar()
image_label = tk.Label(form_frame, text="No file chosen", font=("Arial", 10), bg="#f0f0f0", fg="gray")
image_label.grid(row=5, column=1, sticky="w", pady=5)

def upload_image():
    file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        image_path_var.set(file_path)
        image_label.config(text=os.path.basename(file_path), fg="black")

upload_btn = tk.Button(form_frame, text="Choose File", font=("Arial", 10, "bold"), bg="#1E90FF", fg="white", command=upload_image)
upload_btn.grid(row=5, column=1, sticky="e", pady=5)

# ---------- Submit Function ----------
def add_event():
    name = event_name_entry.get().strip()
    category = category_var.get()
    date = date_picker.get_date().strftime("%Y-%m-%d")
    description = desc_text.get("1.0", tk.END).strip()
    image_path = image_path_var.get()
    fee = fee_entry.get().strip()

    if not name or not category or not date or not image_path or not fee:
        messagebox.showerror("Error", "Please fill all required fields!")
        return

    # Validate fee
    try:
        fee_val = float(fee)
    except ValueError:
        messagebox.showerror("Error", "Registration Fee must be a number!")
        return

    # Prepare destination image path (keep original extension, sanitize name)
    original_ext = os.path.splitext(image_path)[1]  # e.g. .jpg
    safe_name = sanitize_filename(name)
    dest_filename = f"{safe_name}{original_ext}"
    dest_path = os.path.join("event_images", dest_filename)

    # If same filename exists, add a number suffix to avoid overwrite
    if os.path.exists(dest_path):
        base, ext = os.path.splitext(dest_filename)
        i = 1
        while os.path.exists(os.path.join("event_images", f"{base}_{i}{ext}")):
            i += 1
        dest_filename = f"{base}_{i}{ext}"
        dest_path = os.path.join("event_images", dest_filename)

    # Copy image
    try:
        shutil.copy(image_path, dest_path)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to copy image: {e}")
        return

    # Insert into DB
    try:
        cursor.execute(
            "INSERT INTO events (name, category, date, description, image, fee) VALUES (?, ?, ?, ?, ?, ?)",
            (name, category, date, description, dest_path, fee_val)
        )
        conn.commit()
        messagebox.showinfo("Success", "Event added successfully!")
        # Clear fields
        event_name_entry.delete(0, tk.END)
        desc_text.delete("1.0", tk.END)
        fee_entry.delete(0, tk.END)
        image_label.config(text="No file chosen", fg="gray")
        image_path_var.set("")
    except Exception as e:
        messagebox.showerror("Database Error", f"{e}")

# ---------- Buttons ----------
submit_btn = tk.Button(root, text="Add Event", font=("Arial", 12, "bold"), bg="#32CD32", fg="white", width=15, command=add_event)
submit_btn.pack(pady=20)

root.mainloop()

# close DB connection when program exits
conn.close()
