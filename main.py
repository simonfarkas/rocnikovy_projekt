import tkinter as tk
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="postgres"
)

cur = conn.cursor()

# cur.execute("""
#     CREATE TABLE users (
#         id SERIAL PRIMARY KEY,
#         email VARCHAR(50) NOT NULL,
#         password VARCHAR(50) NOT NULL,
#         balance FLOAT NOT NULL DEFAULT 0
#     )
# """)
#
# cur.execute("""
#     CREATE TABLE transactions (
#         id SERIAL PRIMARY KEY,
#         amount FLOAT NOT NULL,
#         type VARCHAR(50) NOT NULL,
#         user_id INTEGER REFERENCES users(id)
#     )
# """)

# conn.commit()

user_id = 0
zostatok = 0
transakcie = []

# login funkcia
def handle_login():
    email = email_input.get()
    password = password_input.get()
    cur.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
    user = cur.fetchone()
    if user:
        # ziskanie id uzivatela
        global user_id
        global zostatok
        user_id = user[0]

        # ziskanie zostatku z databazy
        cur.execute("SELECT balance FROM users WHERE id=%s", (user_id,))
        zostatok = cur.fetchone()
        # FIX: zostatok je furt 0 aj ked v databaze je ina hodnota
        zostatok = zostatok[0]
        print(zostatok)

        # schovanie prihlasovacieho okna a zobrazenie hlavnej stranky
        login_label.pack_forget()
        email_label.pack_forget()
        email_input.pack_forget()
        password_label.pack_forget()
        password_input.pack_forget()
        login_button.pack_forget()
        register_button.pack_forget()
        error_label.pack_forget()
        zostatok_label.pack()
        button_vklad.pack()
        vklad_input.pack()
        button_vyber.pack()
        vyber_input.pack()
        view_transactions_button.pack()
        change_details_button.pack()

    else:
        error_label.config(text="Chyba: Nespravne udaje")

# register funkcia
def handle_register():
    email = email_input.get()
    password = password_input.get()
    # kontrola ci uzivatel uz existuje
    cur.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cur.fetchone()
    if user:
        error_label.config(text="Chyba: Uzivatel uz existuje")
    else:
        cur.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
        conn.commit()
        error_label.config(text="Registracia uspesna")


# funkcia na vklad penazi
def vklad():
    global zostatok
    ciastka = float(vklad_input.get())
    zostatok += ciastka
    transakcie.append((ciastka, "Vklad"))
    zostatok_label.config(text=f"Zostatok: {zostatok:.2f} eur")

# funkcia na vyber penazi
def vyber():
    global zostatok
    ciastka = float(vyber_input.get())
    if ciastka <= zostatok:
        zostatok -= ciastka
        transakcie.append((ciastka, "Vyber"))
        zostatok_label.config(text=f"Zostatok: {zostatok:.2f} eur")
    else:
        error_label.config(text="Chyba: Nedostatok prostriedkov")

# zoznam transakcii
def zoznam_transakcii():
    transakcie_window = tk.Toplevel(window)
    transakcie_window.geometry("400x400")
    tk.Label(transakcie_window, text="Historia transakcii").pack()
    for transaction in transakcie:
        tk.Label(transakcie_window, text=f"{transaction[1]} - {transaction[0]:.2f} eur").pack()

# zmena udajov
def show_change_details():
    change_window = tk.Toplevel(window)
    change_window.geometry("400x400")
    tk.Label(change_window, text="Upravit udaje").pack()
    tk.Label(change_window, text="Novy email").pack()
    novy_email = tk.Entry(change_window)
    novy_email.pack()
    tk.Label(change_window, text="Nove heslo").pack()
    nove_heslo = tk.Entry(change_window, show="*")
    nove_heslo.pack()
    tk.Button(change_window, text="Ulozit", command=lambda: save_changes(novy_email.get(), nove_heslo.get())).pack()

# ulozenie zmien
def save_changes(new_email, new_password):
    email_label.config(text=f"Email: {new_email}")
    password_label.config(text=f"Password: {new_password}")


window = tk.Tk()
window.geometry("400x400")

# prihlasenie
login_label = tk.Label(text="Prihlasenie")
login_label.pack()

email_label = tk.Label(text="Email")
email_label.pack()

email_input = tk.Entry()
email_input.pack()

password_label = tk.Label(text="Heslo")
password_label.pack()

password_input = tk.Entry(show="*")
password_input.pack()

login_button = tk.Button(text="Prihlasenie", command=handle_login)
login_button.pack()

register_button = tk.Button(text="Registracia", command=handle_register)
register_button.pack()

error_label = tk.Label(fg="red")
error_label.pack()

# hlavna stranka
button_vklad = tk.Button(text="Vklad", command=vklad)
vklad_input = tk.Entry()
button_vyber = tk.Button(text="Vyber", command=vyber)
vyber_input = tk.Entry()

view_transactions_button = tk.Button(text="Historia transakcii", command=zoznam_transakcii)
change_details_button = tk.Button(text="Upravit udaje", command=show_change_details)

zostatok_label = tk.Label(text=f"Zostatok: {zostatok:.2f} eur")

window.mainloop()
