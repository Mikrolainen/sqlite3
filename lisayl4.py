import ttkbootstrap as ttk
from tkinter import messagebox
from ttkbootstrap.tableview import Tableview
from ttkbootstrap import Style
from ttkbootstrap.constants import *
import sqlite3

conn= sqlite3.connect("epood_mkohava.db")

my_w = ttk.Window()
my_w.geometry("700x700")  # width and height
colors = my_w.style.colors

style = Style(theme='darkly')

l1 = [
    {"text": "id", "stretch": False},
    {"text": "First name", "stretch": False},
    {"text": "Last name", "stretch": False},
    {"text": "email", "stretch": True},
    {"text": "mark","stretch":True},
    {"text": "model", "stretch": False},
    {"text": "year", "stretch": False},
    {"text": "price", "stretch": False}
]  # Columns with Names and style 
# Data rows as list
    
r_set = []

query= conn.execute("SELECT * from mkohava")
for row in query:
    r_set.append(row)

dv = ttk.tableview.Tableview(
    master=my_w,
    paginated=True,
    coldata=l1,
    rowdata=r_set,
    searchable=True,
    bootstyle=SUCCESS,
    pagesize=10,
    height=10,
    stripecolor=(colors.dark, None),
)

def lisa_andmed():
    # Küsime kasutajalt sisendid
    eesnimi = eesnimi_entry.get()
    perenimi = perenimi_entry.get()
    email = email_entry.get()
    automark = automark_entry.get()
    automudel = automudel_entry.get()
    aasta = aasta_entry.get()
    hind = hind_entry.get()
    
    dv.insert_row("end", values=[len(r_set) + 1, eesnimi, perenimi, email, automark, automudel, aasta, hind])
    dv.load_table_data()

def kustuta_andmed():
    selected_rows = dv.get_rows(selected=True)
    for row in selected_rows:
        db_id = row.values[0]  # Assuming the primary key 'id' is the first column in the row
        print("Püütud kustutada rida id-ga:", db_id)
        query = "DELETE FROM mkohava WHERE id = ?"
        print("Päring:", query)
        try:
            cursor = conn.cursor()
            cursor.execute(query, (db_id,))
            conn.commit()  # Commit the transaction
            print("Kustutamine õnnestus.")
            # Laadi tabel uuesti pärast kustutamist
            laadi_andmed_uuesti()
        except Exception as e:
            print("Kustutamine ebaõnnestus:", e)

def laadi_andmed_uuesti():
    # Eemaldame kõik olemasolevad read tabelist
    dv.delete_rows()

    # Laeme andmed andmebaasist uuesti
    r_set.clear()
    query = conn.execute("SELECT * from mkohava")
    for row in query:
        r_set.append(row)
    
    # Laeme andmed tabelisse
    for row in r_set:
        dv.insert_row("end", values=row)
    
    # Laeme tabeli uuesti
    dv.load_table_data()


ttk.Label(my_w, text="Eesnimi:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
eesnimi_entry = ttk.Entry(my_w)
eesnimi_entry.grid(row=1, column=0, padx=10, pady=5, columnspan=1)
ttk.Label(my_w, text="Perenimi:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
perenimi_entry = ttk.Entry(my_w)
perenimi_entry.grid(row=2, column=0, padx=10, pady=5, columnspan=1)
ttk.Label(my_w, text="Email:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
email_entry = ttk.Entry(my_w,)
email_entry.grid(row=3, column=0, padx=10, pady=5, columnspan=1)
ttk.Label(my_w, text="Auto mark:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
automark_entry = ttk.Entry(my_w)
automark_entry.grid(row=4, column=0, padx=10, pady=5, columnspan=1)
ttk.Label(my_w, text="Auto mudel:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
automudel_entry = ttk.Entry(my_w)
automudel_entry.grid(row=5, column=0, padx=10, pady=5, columnspan=1)
ttk.Label(my_w, text="Aasta:").grid(row=6, column=0, padx=10, pady=5, sticky="w")
aasta_entry = ttk.Entry(my_w)
aasta_entry.grid(row=6, column=0, padx=10, pady=5, columnspan=1)
ttk.Label(my_w, text="Hind:").grid(row=7, column=0, padx=10, pady=5, sticky="w")
hind_entry = ttk.Entry(my_w)
hind_entry.grid(row=7, column=0, padx=10, pady=5, columnspan=1)
lisa_button = ttk.Button(my_w, text="Lisa andmed", command=lisa_andmed)
lisa_button.grid(row=8, column=0, columnspan=2, padx=10, pady=5, sticky="w")
kustuta_button = ttk.Button(my_w, text="Kustuta rida", command=kustuta_andmed)
kustuta_button.grid(row=9, column=0, columnspan=2, padx=10, pady=5, sticky="w")


dv.grid(row=0, column=0, padx=10, pady=5, sticky="w")
dv.autofit_columns() # Fit in current view 
dv.load_table_data() # Load all data rows 
my_w.mainloop()
