import sqlite3
import threading
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from plyer import notification
from tkinter import ttk
import datetime as dt
from tkcalendar import DateEntry
import time
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# File to store the state of the water reminder
state_file = 'water_reminder_state.json'

# Function to save the state of the water reminder
def save_state(state):
    with open(state_file, 'w') as f:
        json.dump(state, f)

# Function to load the state of the water reminder
def load_state():
    try:
        with open(state_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return False

# Load the initial state
water_reminder_state = load_state()

# -------------------------------------- Window 1  ------------------------------------------------------------

window = Tk()
window.title("NOTIFIER FOR DESKTOP 🔔")
window.geometry("700x600")
window.config(bg="black")
window.iconbitmap('ico.ico')
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
            # Insert into database
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
            timeout=20
        )

    except Exception as e:
        print(f"Error displaying notification: {e}")

def validate_input():
    text = name_txt.get()
    if text.isalpha():
        return True
    else:
        return False
def send_feedback(email, message):
    try:
        smtp_server = "smtp.gmail.com"  # Replace with your SMTP server
        port = 587  # Replace with your SMTP port
        sender_email = "tushxr0@gmail.com"  # Replace with your email
        password = "djjkbqiiwlbohzyb"  # Replace with your email password

        # Create a secure SSL context
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(sender_email, password)

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = "Feedback from Desktop Notifier"

        body = f"Feedback: {message}"
        msg.attach(MIMEText(body, 'plain'))

        server.sendmail(sender_email, email, msg.as_string())
        server.quit()

        messagebox.showinfo("Feedback Sent", "Your feedback has been sent successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")



def check_birthday_reminders():
    today = dt.datetime.now().date()
    c.execute("SELECT name, birthday FROM BirthdayData")
    birthdays = c.fetchall()
    for birthday in birthdays:
        name, bday = birthdayz
        bday_date = dt.datetime.strptime(bday, "%Y-%m-%d").date()
        if bday_date.month == today.month and bday_date.day == today.day:
            notification.notify(
                title="Birthday Reminder",
                message=f"Today is {name}'s birthday!",
                timeout=10
            )
    threading.Timer(86400, check_birthday_reminders).start()  # Check every day

# Start checking for birthday reminders when the application starts
check_birthday_reminders()
##<<<<<<<<<<<<<<<<<--------------------------- GUI ------------------------------------------------>>>>>>>>>>>>

# ---------------NAVBAR---------------

Photo_Open = Image.open("navbar.png")
photo_final = ImageTk.PhotoImage(Photo_Open)
img_label = Label(window, image=photo_final)
img_label.place(x=-2)

# -------------------------------- Enter name -----------------

name = Label(window, text="Enter name             : ", font="Verdana 15", bg="black", fg="#FF8D55")
name.place(x=12, y=160)

# Entery - name
name_txt = Entry(window, width=20, font=("Verdana", 18), bg="grey")
name_txt.place(x=290, y=160)

# ----------------- TITLE TO NOTIFY ---------------------------

# Label - Title
t_label = Label(window, text="Title to Notify          :", font="Verdana 15", bg="black", fg="#FF8D55")
t_label.place(x=12, y=230)

# ENTRY - Title
title = Entry(window, width=20, font=("Verdana", 18), bg="grey")
title.place(x=290, y=230)

# ------------------------- DISPLAY MESSAGE ------------------

# Label - Message
m_label = Label(window, text="Display Message      :", font="Verdana 15", bg="black", fg="#FF8D55")
m_label.place(x=12, y=300)

# ENTRY - Message
msg = Entry(window, width=20, font=("Verdana", 18), bg="grey")
msg.place(x=290, y=300)

# --------------------  SET DATE  ----------------------
# Date Entry
date_label = Label(window, text="Date(YYYY-MM-DD)   :", font="Verdana 14", bg="black", fg="#FF8D55")
date_label.place(x=12, y=370)

date_entry = DateEntry(window, width=12, font=("Verdana", 18), borderwidth=2, year=dt.date.today().year, date_pattern="yyyy-mm-dd")
date_entry.set_date(dt.date.today())
date_entry.place(x=290, y=370)

# Time Entry
time_label = Label(window, text="Time (HH:MM):", font="Verdana 14", bg="black", fg="#FF8D55")
time_label.place(x=12, y=440)
time_entry = Entry(window, width=20, font=("Verdana", 18), bg="grey")
time_entry.insert(0, dt.datetime.now().strftime("%H:%M"))
time_entry.place(x=290, y=440)

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
    top.iconbitmap('ico.ico')

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

    def Clear_rec():
        Table.delete(*Table.get_children())
        c.execute("DELETE from NotifierData")
        conn.commit()

    # ---------------- CLEAR RECORDS BTN --------------

    clear_records = Button(top, text="CLEAR RECORDS",
                           font=("Verdana", 8, "bold"),
                           fg="black",
                           bg="#C69749",
                           command=Clear_rec)

    clear_records.place(y=320, x=70)
    clear_records.config(padx=5, pady=5)

    # Function to delete specific entry based on title
    def delete_entry():
        search_title = title_search_entry.get()
        c.execute("DELETE from NotifierData WHERE title=?", (search_title,))
        conn.commit()
        messagebox.showinfo("Delete Successful", "Entry deleted successfully!")
        refresh_records()

    # Label and entry for searching by title
    title_search_label = Label(top, text="Title to delete:", font=("Verdana", 10), bg="black", fg="#FF8D55")
    title_search_label.place(x=220, y=320)
    title_search_entry = Entry(top, width=20, font=("Verdana", 10), bg="grey")
    title_search_entry.place(x=360, y=320)

    # Button to delete entry
    delete_entry_btn = Button(top, text="Delete Entry", font=("Verdana", 8, "bold"), fg="black", bg="#C69749", command=delete_entry)
    delete_entry_btn.place(x=530, y=320)

    # Function to refresh records after deletion
    def refresh_records():
        Table.delete(*Table.get_children())
        c.execute("SELECT *, oid FROM NotifierData")
        records = c.fetchall()
        for record in records:
            Table.insert("", "end", values=record)
        conn.commit()

    # ---------------  DATABASE ---------------------
    c.execute("SELECT *, oid FROM NotifierData")
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
# ----------------------- ADVANCE BUTTON ------------------------------------------------
# Create a PhotoImage object for the settings icon
settings_icon = PhotoImage(file="settings.png").subsample(15, 15)  # Adjust subsample values as needed

# Create the Advance button with the settings icon
advance_btn = Button(window, image=settings_icon, compound="left",
                     font=("Verdana", 8, "bold"), fg="black", bg="black",
                     command=lambda: open_settings_window(), bd=0,
                     highlightthickness=0)  # Set highlightthickness to 0 to remove button border
advance_btn.place(x=32, y=100)  # Move the button to the top-left corner
# advance_btn.config(padx=12, pady=60)

# -------------------------------------- SETTINGS WINDOW --------------------------------------

def open_settings_window():
    settings_window = Toplevel(window)
    settings_window.title("Settings")
    settings_window.geometry("400x500")
    settings_window.config(bg="black")

    def set_reminders():
        medication_reminder = med_var.get()
        water_reminder = water_var.get()
        birthday_reminder = bday_var.get()
        gym_reminder = gym_var.get()

        if water_reminder:
            set_water_reminder()
        if birthday_reminder:
            set_birthday_reminder()

        messagebox.showinfo("Settings Saved", "Your settings have been saved!")

    def set_water_reminder():
        def water_notify():
            while True:
                current_time = time.localtime()
                if current_time.tm_min == 0:
                    notification.notify(
                        title="Water Reminder",
                        message="Time to drink water!",
                        timeout=10
                    )
                    time.sleep(60)
                time.sleep(1)
        threading.Thread(target=water_notify, daemon=True).start()

    if water_reminder_state:
        set_water_reminder()

    def toggle_water_reminder():
        global water_reminder_state
        water_reminder_state = not water_reminder_state
        save_state(water_reminder_state)
        if water_reminder_state:
            set_water_reminder()
            water_reminder_button.config(text="Turn Off Water Reminder")
        else:
            water_reminder_button.config(text="Turn On Water Reminder")

    def set_birthday_reminder():
        def save_birthday():
            name = bday_name_entry.get()
            date = bday_date_entry.get()
            try:
                birthday = dt.datetime.strptime(date, "%Y-%m-%d")
                c.execute('''
                    CREATE TABLE IF NOT EXISTS BirthdayData (
                        name TEXT,
                        birthday DATE
                    )
                ''')
                c.execute("INSERT INTO BirthdayData (name, birthday) VALUES (?, ?)", (name, date))
                conn.commit()
                messagebox.showinfo("Success", "Birthday reminder set successfully!")
            except ValueError:
                messagebox.showerror("Invalid Date", "Please enter the date in the format YYYY-MM-DD")

        bday_window = Toplevel(settings_window)
        bday_window.title("Set Birthday Reminder")
        bday_window.geometry("300x200")
        bday_window.config(bg="black")

        bday_name_label = Label(bday_window, text="Name:", font=("Verdana", 12), bg="black", fg="#FF8D55")
        bday_name_label.pack(pady=10)
        bday_name_entry = Entry(bday_window, font=("Verdana", 12), bg="grey")
        bday_name_entry.pack(pady=5)

        bday_date_label = Label(bday_window, text="Birthday (YYYY-MM-DD):", font=("Verdana", 12), bg="black", fg="#FF8D55")
        bday_date_label.pack(pady=10)
        bday_date_entry = Entry(bday_window, font=("Verdana", 12), bg="grey")
        bday_date_entry.pack(pady=5)

        save_bday_button = Button(bday_window, text="Save", font=("Verdana", 10, "bold"), fg="black", bg="#C69749", command=save_birthday)
        save_bday_button.pack(pady=20)

    med_var = BooleanVar()
    water_var = BooleanVar()
    bday_var = BooleanVar()
    gym_var = BooleanVar()

    water_reminder_button = Button(settings_window,
                                   text="Turn On Water Reminder" if not water_reminder_state else "Turn Off Water Reminder",
                                   command=toggle_water_reminder)
    water_reminder_button.pack(pady=20)

    birthday_reminder_button = Button(settings_window, text="Set Birthday Reminder", font=("Verdana", 10, "bold"), fg="black", bg="#C69749", command=set_birthday_reminder)
    birthday_reminder_button.pack(pady=20)

    feedback_label = Label(settings_window, text="Feedback:", font=("Verdana", 12), bg="black", fg="#FF8D55")
    feedback_label.pack(pady=10)

    feedback_message_label = Label(settings_window, text="Your Message:", font=("Verdana", 10), bg="black", fg="#FF8D55")
    feedback_message_label.pack()

    feedback_message_text = Text(settings_window, width=40, height=5)
    feedback_message_text.pack()

    send_feedback_btn = Button(settings_window, text="Send Feedback", font=("Verdana", 10, "bold"), fg="black", bg="#C69749",
                               command=lambda: send_feedback("tushxr0@gmail.com", feedback_message_text.get("1.0", "end-1c")))
    send_feedback_btn.pack(pady=10)

    settings_window.mainloop()
# Start the GUI
window.resizable(False, False)
window.mainloop()
