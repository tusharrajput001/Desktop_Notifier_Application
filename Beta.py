import sqlite3
import threading
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from plyer import notification
from tkinter import ttk
import datetime as dt

# -------------------------------------- Window 1  ------------------------------------------------------------

window = Tk()
window.title("NOTIFIER FOR DESKTOP 🔔")
window.geometry("700x600")
window.config(bg="black")
conn = sqlite3.connect("NotifierDatabase.db")
c = conn.cursor()
# --------------------- DARK MODE & LIGHT MODE SWITCH -----------------------------------------------------------


is_on = True


def switch():
    global is_on
    # Determine is on or off
    if is_on:
        on_button.config(image=off, bg="#D5B4B4")
        is_on = False
        window.config(bg="#D5B4B4")
        t_label.config(bg="#D5B4B4", fg="black")
        title.config(bg="#E4D0D0")
        name.config(bg="#D5B4B4", fg="black")
        name_txt.config(bg="#E4D0D0")
        m_label.config(bg="#D5B4B4", fg="black")
        msg.config(bg="#E4D0D0")
        time_label.config(bg="#D5B4B4", fg="black")
        time_entry.config(bg="#E4D0D0")
        date_label.config(bg="#D5B4B4", fg="black")
        date_entry.config(bg="#E4D0D0")
        name_txt.config(bg="#E4D0D0")
        name.config(bg="#D5B4B4", fg="black")
        but.config(bg="#CCD5AE", fg="black")
        my_rec_btn.config(bg="#CCD5AE", fg="black")

    else:
        on_button.config(image=on, pady=50, bg="black")
        is_on = True
        window.config(bg="black")
        t_label.config(bg="black", fg="#FF8D55")
        title.config(bg="grey")
        name.config(bg="black", fg="#FF8D55")
        name_txt.config(bg="grey")
        m_label.config(bg="black", fg="#FF8D55")
        msg.config(bg="grey")
        time_label.config(bg="black", fg="#FF8D55")
        time_entry.config(bg="grey")
        date_label.config(bg="black", fg="#FF8D55")
        date_label.config(bg="black")
        date_entry.config(bg="grey")
        name_txt.config(bg="grey")
        name.config(bg="black", fg="#FF8D55")
        but.config(bg="#C69749")
        my_rec_btn.config(bg="#C69749")


# Define Our Images
on = PhotoImage(file="on.png")
off = PhotoImage(file="off.png")
# Create A Button
on_button = Button(window, image=on, bd=0, command=switch)
on_button.config(bg="black")

off_button = Button(window, image=off, command=switch)
off_button.config(bg="#D5B4B4")

on_button.place(x=600, y=92)


# ------------------------------------------ FUNCTIONS --------------------------------------

def check_notification():
    get_title = title.get()
    get_msg = msg.get()
    not_date = date_entry.get()
    not_time = time_entry.get()

    try:
        date_time_str = f"{not_date} {not_time}"
        date_time = dt.datetime.strptime(date_time_str, "%Y-%m-%d %H:%M")
        current_time = dt.datetime.now()

        if date_time > current_time:
            time_difference = (date_time - current_time).total_seconds()

            # Schedule notification in a separate thread to avoid blocking the GUI
            threading.Timer(time_difference, show_notification, args=[get_title, get_msg]).start()
            messagebox.showinfo("Notification Set", f"Notification set for {date_time}")
            c.execute('''
                CREATE TABLE IF NOT EXISTS NotifierData (
                    name_txt TEXT,
                    title TEXT,
                    msg TEXT,
                    date_entry TEXT,
                    time_entry TEXT
                )
            ''')
            # Insert the notification into the database
            c.execute("insert into NotifierData values(:name_txt, :title, :msg, :date_entry, :time_entry)",
                      {
                          'name_txt': name_txt.get(),
                          'title': title.get(),
                          'msg': msg.get(),
                          'date_entry': date_entry.get(),
                          'time_entry': time_entry.get()
                      })

            conn.commit()
        else:
            messagebox.showwarning("Invalid Time", "Please enter a future date and time.")
    except ValueError:
        messagebox.showerror("Invalid Format", "Please enter the date and time in the format YYYY-MM-DD HH:MM.")


def show_notification(get_title, get_msg):
    try:
        notification.notify(
            title=get_title,
            message=get_msg,
            app_icon="ico.ico",
            timeout=20  # Notification will be visible for 10 seconds
        )
    except Exception as e:
        print(f"Error displaying notification: {e}")


def validate_input():
    text = name_txt.get()
    if text.isalpha():  # isalpha return true if all alphabets are correct
        return True
    else:
        return False


##<<<<<<<<<<<<<<<<<--------------------------- GUI ------------------------------------------------>>>>>>>>>>>>


# ---------------NAVBAR---------------

Photo_Open = Image.open("navbar.png")
photo_final = ImageTk.PhotoImage(Photo_Open)
img_label = Label(window, image=photo_final)
img_label.place(x=-2)

# -------------------------------- Enter name -----------------

name = Label(window, text="Enter name          : ", font="Verdana 15", bg="black", fg="#FF8D55")
name.place(x=12, y=160)

# Entry - name
name_txt = Entry(window, width=20, font=("Verdana", 18), bg="grey")
name_txt.place(x=290, y=160)

# ----------------- TITLE TO NOTIFY ---------------------------

# Label - Title
t_label = Label(window, text="Title to Notify       :", font="Verdana 15", bg="black", fg="#FF8D55")
t_label.place(x=12, y=250)

# ENTRY - Title
title = Entry(window, width=20, font=("Verdana", 18), bg="grey")
title.place(x=290, y=250)

# ------------------------- DISPLAY MESSAGE ------------------

# Label - Message
m_label = Label(window, text="Display Message   :", font="Verdana 15", bg="black", fg="#FF8D55")
m_label.place(x=12, y=330)

# ENTRY - Message
msg = Entry(window, width=20, font=("Verdana", 18), bg="grey")
msg.place(x=290, y=330)

# --------------------  SET DATE  ----------------------
# Date Entry
date_label = Label(window, text="DATE (YYYY-MM-DD):", font="Verdana 10", bg="black", fg="#FF8D55")
date_label.place(x=20, y=410)
date_entry = Entry(window, width=13, font=("Verdana", 10), bg="grey")
date_entry.insert(0, dt.datetime.now().strftime("%Y-%m-%d"))
date_entry.place(x=180, y=410)

# Time Entry
time_label = Label(window, text="Time (HH:MM):", font="Verdana 10", bg="black", fg="#FF8D55")
time_label.place(x=310, y=410)
time_entry = Entry(window, width=13, font=("Verdana", 10), bg="grey")
time_entry.insert(0, dt.datetime.now().strftime("%H:%M"))
time_entry.place(x=450, y=410)

# ----------------------------- SET NOT. BUTTON -------------------------------------------

but = Button(window, text="SET NOTIFICATION",
             font=("Verdana", 8, "bold"),
             fg="black",
             bg="#C69749",
             command=check_notification)

but.place(x=100, y=500)
but.config(padx=10, pady=10)


# --------------------------------- SHOW RECORDS --------------------------------------------------

def my_records():
    # --- NEW WINDOW OF DB ---
    top = Toplevel()
    top.geometry("625x500")
    top.config(bg="black")
    top.title("DATABASE📅")

    # ---------------NAVBAR---------------

    DbPhoto_Open = Image.open("dbnavbar.png")
    Dbphoto_final = ImageTk.PhotoImage(DbPhoto_Open)
    Dbimg_label = Label(top, image=Dbphoto_final)
    Dbimg_label.pack()

    style = ttk.Style()
    style.configure("Treeview", background="black", foreground="white")
    style.configure("Treeview.Heading", foreground="#FF8D55", background="black", font=("Verdana", 9, "bold"))

    Table = ttk.Treeview(top, columns=("Name", "Title", "Display Message", "Date", "Time", "ID"), show="headings")
    Table.pack()

    Table.heading("ID", text="ID")
    Table.heading("Name", text="Name")
    Table.heading("Title", text="Title")
    Table.heading("Display Message", text="Display Message")
    Table.heading("Date", text="Date")
    Table.heading("Time", text="Time")

    # SETTING OF TABLE

    Table.column("ID", anchor="center", width=103)
    Table.column("Name", anchor="center", width=103)
    Table.column("Title", anchor="center", width=103)
    Table.column("Display Message", anchor="center", width=121)
    Table.column("Date", anchor="center", width=103)
    Table.column("Time", anchor="center", width=103)

    # ---------------------- CLEAR RECORD FUNCTION --------------------

    def clear_rec():
        Table.delete(*Table.get_children())
        c.execute("DELETE from NotifierData")
        conn.commit()

    # ---------------- CLEAR RECORDS BTN --------------

    clear_records = Button(top, text="CLEAR RECORDS",
                           font=("Verdana", 8, "bold"),
                           fg="black",
                           bg="#C69749",
                           command=clear_rec)

    clear_records.place(y=320, x=70)
    clear_records.config(padx=5, pady=5)

    # ---------------  DATABASE ---------------------

    c.execute("select *, oid from NotifierData")
    records = c.fetchall()

    # insert record in table
    for record in records:
        Table.insert("", "end", values=record)

    conn.commit()

    top.resizable(False, False)
    top.mainloop()


# ----------------------- SHOW MY RECORDS BTN ------------------------------------------------
my_rec_btn = Button(window, text="  SHOW RECORDS  ",
                    font=("Verdana", 8, "bold"),
                    fg="black",
                    bg="#C69749",
                    command=my_records,
                    )
my_rec_btn.place(x=450, y=500)
my_rec_btn.config(padx=10, pady=10)

my_rec_btn.place(x=450, y=500)
my_rec_btn.config(padx=10, pady=10)

window.resizable(False, False)

window.mainloop()
