import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
import os

# ---------- Database Connection ----------
conn = sqlite3.connect("campusbuzz.db")
cursor = conn.cursor()

# ---------- Function to View Event Details ----------
def show_event_details(event_id):
    cursor.execute("SELECT * FROM events WHERE id=?", (event_id,))
    event = cursor.fetchone()

    if not event:
        messagebox.showerror("Error", "Event not found!")
        return

    # Event Detail Window
    detail_window = tk.Toplevel()
    detail_window.title("Event Details")
    detail_window.geometry("550x650")
    detail_window.config(bg="#f0f0f0")

    # Heading
    tk.Label(detail_window, text=event[1], font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#1E90FF").pack(pady=10)
    tk.Label(detail_window, text=f"Category: {event[2]}", font=("Arial", 12), bg="#f0f0f0").pack()
    tk.Label(detail_window, text=f"Date: {event[3]}", font=("Arial", 12), bg="#f0f0f0").pack()
    tk.Label(detail_window, text=f"Fee: ₹{event[6]:.2f}", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)

    # ---------- Image ----------
    if event[5] and os.path.exists(event[5]):
        try:
            img = Image.open(event[5])
            img = img.resize((350, 220))
            photo = ImageTk.PhotoImage(img)
            img_label = tk.Label(detail_window, image=photo, bg="#f0f0f0")
            img_label.image = photo
            img_label.pack(pady=10)
        except Exception as e:
            tk.Label(detail_window, text=f"Error loading image: {e}", font=("Arial", 10), fg="red", bg="#f0f0f0").pack(pady=10)
    else:
        tk.Label(detail_window, text="No Image Available", font=("Arial", 12, "italic"), bg="#f0f0f0", fg="gray").pack(pady=10)

    # ---------- Description ----------
    tk.Label(detail_window, text="Description:", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(anchor="w", padx=20)
    desc_text = tk.Text(detail_window, font=("Arial", 12), wrap="word", width=55, height=10)
    desc_text.pack(padx=20, pady=5)
    desc_text.insert(tk.END, event[4])
    desc_text.config(state="disabled")

# ---------- Main Window ----------
def view_all_events():
    root = tk.Tk()
    root.title("View All Events - CampusBuzz")
    root.geometry("850x550")
    root.config(bg="#f0f0f0")

    # Heading
    tk.Label(root, text="All Events", font=("Arial", 20, "bold"), fg="#1E90FF", bg="#f0f0f0").pack(pady=10)

    # ---------- Frame for Table ----------
    frame = tk.Frame(root, bg="#f0f0f0")
    frame.pack(pady=10)

    # Treeview (Table)
    columns = ("ID", "Name", "Category", "Date", "Fee")
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=12)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor="center")
    tree.pack(side="left", fill="both")

    # Scrollbar
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # ---------- Fetch Data ----------
    cursor.execute("SELECT id, name, category, date, fee FROM events")
    rows = cursor.fetchall()

    if not rows:
        tk.Label(root, text="No events found!", font=("Arial", 12, "italic"), bg="#f0f0f0", fg="gray").pack(pady=20)
    else:
        for row in rows:
            tree.insert("", tk.END, values=row)

    # ---------- View Details Button ----------
    def on_view_details():
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select an event to view details!")
            return
        event_id = tree.item(selected)['values'][0]
        show_event_details(event_id)

    view_btn = tk.Button(root, text="View Details", font=("Arial", 12, "bold"), bg="#1E90FF", fg="white", width=15, command=on_view_details)
    view_btn.pack(pady=15)

    root.mainloop()


# ---------- Run When File Executed Directly ----------
if __name__ == "__main__":
    view_all_events()
