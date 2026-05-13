import customtkinter as ctk
from tkinter import messagebox

# ================= LOCAL DATA STORAGE (Memory Only) =================

tickets_db = []

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ================= FUNCTIONS =================
def add_ticket():
    try:
        # Validate ID is an integer
        tid = int(entry_id.get())
        
        # Check if ID already exists
        if any(t['id'] == tid for t in tickets_db):
            messagebox.showerror("Error", f"Ticket ID {tid} already exists!")
            return

        new_ticket = {
            "id": tid,
            "passenger": entry_passenger.get(),
            "train": entry_train.get(),
            "from": entry_from.get(),
            "to": entry_to.get(),
            "date": entry_date.get(),
            "class": entry_class.get()
        }
        
        tickets_db.append(new_ticket)
        messagebox.showinfo("Success", "Ticket Booked Successfully (In-Memory)!")
        clear_fields()
    except ValueError:
        messagebox.showerror("Error", "Ticket ID must be a number!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def view_tickets():
    output.delete("1.0", "end")
    if not tickets_db:
        output.insert("end", "No tickets found in the system.")
        return

    for t in tickets_db:
        output.insert(
            "end",
            f"ID:{t['id']}  Passenger:{t['passenger']}  Train:{t['train']}  "
            f"From:{t['from']}  To:{t['to']}  Date:{t['date']}  Class:{t['class']}\n"
        )
        output.insert("end", "-" * 80 + "\n\n")

def search_ticket():
    try:
        tid = int(entry_id.get())
        found = next((t for t in tickets_db if t['id'] == tid), None)
        
        output.delete("1.0", "end")
        if found:
            output.insert(
                "end",
                f"Ticket ID  : {found['id']}\n"
                f"Passenger  : {found['passenger']}\n"
                f"Train No   : {found['train']}\n"
                f"From       : {found['from']}\n"
                f"To         : {found['to']}\n"
                f"Travel Date: {found['date']}\n"
                f"Seat Class : {found['class']}\n"
            )
        else:
            output.insert("end", "Ticket Not Found")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid Ticket ID to search.")

def update_ticket():
    try:
        tid = int(entry_id.get())
        for t in tickets_db:
            if t['id'] == tid:
                t['passenger'] = entry_passenger.get()
                t['train'] = entry_train.get()
                t['from'] = entry_from.get()
                t['to'] = entry_to.get()
                t['date'] = entry_date.get()
                t['class'] = entry_class.get()
                messagebox.showinfo("Success", "Ticket Updated Successfully!")
                return
        messagebox.showerror("Error", "Ticket ID not found!")
    except ValueError:
        messagebox.showerror("Error", "Ticket ID must be a number!")

def cancel_ticket():
    try:
        tid = int(entry_id.get())
        global tickets_db
        initial_len = len(tickets_db)
        tickets_db = [t for t in tickets_db if t['id'] != tid]
        
        if len(tickets_db) < initial_len:
            messagebox.showinfo("Success", "Ticket Cancelled Successfully!")
            clear_fields()
        else:
            messagebox.showerror("Error", "Ticket ID not found!")
    except ValueError:
        messagebox.showerror("Error", "Ticket ID must be a number!")

def clear_fields():
    for e in [
        entry_id, entry_passenger, entry_train,
        entry_from, entry_to, entry_date, entry_class
    ]:
        e.delete(0, "end")

# ================= UI LAYOUT =================
app = ctk.CTk()
app.geometry("1000x620")
app.title("Railway Dashboard")

# Sidebar
sidebar = ctk.CTkFrame(app, width=220, corner_radius=0, fg_color="#0F172A")
sidebar.pack(side="left", fill="y")

ctk.CTkLabel(
    sidebar,
    text=" Railway App",
    font=("Segoe UI", 20, "bold"),
    text_color="#00F5D4"
).pack(pady=30)

def side_btn(text, cmd, color):
    return ctk.CTkButton(
        sidebar,
        text=text,
        command=cmd,
        fg_color=color,
        hover_color="#1f2937",
        corner_radius=10
    )

side_btn("  Add Ticket", add_ticket, "#7C3AED").pack(pady=10, padx=20)
side_btn("  View Tickets", view_tickets, "#06B6D4").pack(pady=10, padx=20)
side_btn("  Search", search_ticket, "#22C55E").pack(pady=10, padx=20)
side_btn("  Update", update_ticket, "#F59E0B").pack(pady=10, padx=20)
side_btn("  Cancel Ticket", cancel_ticket, "#EF4444").pack(pady=10, padx=20)
side_btn("  Clear", clear_fields, "#64748B").pack(pady=10, padx=20)

# Main Area
main = ctk.CTkFrame(app, fg_color="#020617")
main.pack(fill="both", expand=True)

ctk.CTkLabel(
    main,
    text="RAILWAY TICKET RESERVATION SYSTEM",
    font=("Segoe UI", 34, "bold"),
    text_color="#E2E8F0"
).pack(pady=20)

# Form Card
card = ctk.CTkFrame(main, corner_radius=20, fg_color="#0F172A")
card.pack(pady=10, padx=40, fill="x")

def create_entry(label):
    frame = ctk.CTkFrame(card, fg_color="#0F172A")
    frame.pack(pady=6, fill="x", padx=20)
    
    ctk.CTkLabel(
        frame,
        text=label,
        text_color="#94A3B8",
        width=160,
        anchor="w"
    ).pack(side="left")
    
    entry = ctk.CTkEntry(
        frame,
        width=250,
        fg_color="#1E293B",
        text_color="white",
        corner_radius=8,
        border_color="#7C3AED"
    )
    entry.pack(side="right")
    return entry

entry_id = create_entry("Ticket ID")
entry_passenger = create_entry("Passenger Name")
entry_train = create_entry("Train No")
entry_from = create_entry("From Station")
entry_to = create_entry("To Station")
entry_date = create_entry("Travel Date (YYYY-MM-DD)")
entry_class = create_entry("Seat Class")

# Buttons Row
btn_frame = ctk.CTkFrame(main, fg_color="#020617")
btn_frame.pack(pady=12)

ctk.CTkButton(btn_frame, text="Add", command=add_ticket, fg_color="#7C3AED").grid(row=0, column=0, padx=10)
ctk.CTkButton(btn_frame, text="Search", command=search_ticket, fg_color="#22C55E").grid(row=0, column=1, padx=10)
ctk.CTkButton(btn_frame, text="Update", command=update_ticket, fg_color="#F59E0B").grid(row=0, column=2, padx=10)
ctk.CTkButton(btn_frame, text="Cancel", command=cancel_ticket, fg_color="#EF4444").grid(row=0, column=3, padx=10)
ctk.CTkButton(btn_frame, text="View", command=view_tickets, fg_color="#06B6D4").grid(row=0, column=4, padx=10)

# Output Box
output = ctk.CTkTextbox(
    main,
    height=160,
    fg_color="#0F172A",
    text_color="#E2E8F0",
    corner_radius=15,
    border_color="#334155",
    font=("Segoe UI", 14)
)
output.pack(padx=40, pady=10, fill="both", expand=True)

app.mainloop()
