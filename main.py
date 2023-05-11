import tkinter as tk
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="postgres"
)

cur = conn.cursor()

# vytvorenie tabuliek v databaze

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
#
# conn.commit()

user_id = 0 # id prihlaseneho uzivatela
zostatok = 0 # zostatok prihlaseneho uzivatela
transakcie = [] # transakcie prihlaseneho uzivatela

# login funkcia
def handle_login():
    email = email_input.get()
    password = password_input.get()

    # kontrola ci uzivatel existuje v databaze
    cur.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
    user = cur.fetchone()

    if user:
        # nastavenie globalnych premennych
        global user_id
        global zostatok
        global transakcie
        user_id = user[0]

        # ziskanie zostatku uzivatela a zobrazenie na obrazovke
        cur.execute("SELECT balance FROM users WHERE id=%s", (user_id,))
        zostatok = cur.fetchone()[0]
        zostatok_label.config(text=f"Zostatok: {zostatok:.2f} €")

        # ziskanie transakcii uzivatela
        cur.execute("SELECT amount, type FROM transactions WHERE user_id=%s", (user_id,))
        transakcie = cur.fetchall()

        # schovanie prihlasovacieho okna
        email_label.pack_forget()
        email_input.pack_forget()
        password_label.pack_forget()
        password_input.pack_forget()
        login_button.pack_forget()
        register_button.pack_forget()
        error_label.pack_forget()
        success_label.pack_forget()

        # zobrazenie hlavnej stranky
        zostatok_label.pack()
        button_vklad.pack()
        vklad_input.pack()
        button_vyber.pack()
        vyber_input.pack()
        view_transactions_button.pack()
        change_details_button.pack()
        logout_button.pack()

        # reset inputov
        email_input.delete(0, tk.END)
        password_input.delete(0, tk.END)
    else:
        # vyhodi chybu ak uzivatel neexistuje
        error_label.config(text="Chyba: Nespravne udaje")

# register funkcia
def handle_register():
    # ziskanie udajov z inputov
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

        # vyhodi spravu ak sa registracia podarila
        success_label.config(text="Registracia uspesna, mozete sa prihlasit")
        error_label.pack_forget()

# logout funkcia
def logout():
    global user_id
    global zostatok
    global transakcie
    user_id = 0
    zostatok = 0
    transakcie = []
    email_label.pack()
    email_input.pack()
    password_label.pack()
    password_input.pack()
    login_button.pack()
    register_button.pack()
    error_label.pack_forget()
    success_label.pack_forget()
    zostatok_label.pack_forget()
    button_vklad.pack_forget()
    vklad_input.pack_forget()
    button_vyber.pack_forget()
    vyber_input.pack_forget()
    view_transactions_button.pack_forget()
    change_details_button.pack_forget()
    logout_button.pack_forget()

# funkcia na vklad penazi
def vklad():
    global zostatok
    ciastka = float(vklad_input.get())
    cur.execute("UPDATE users SET balance=%s WHERE id=%s", (zostatok + ciastka, user_id))
    conn.commit()
    cur.execute("SELECT balance FROM users WHERE id=%s", (user_id,))
    zostatok = cur.fetchone()[0]
    # ulozenie transakcie do databazy
    cur.execute("INSERT INTO transactions (amount, type, user_id) VALUES (%s, %s, %s)", (ciastka, "Vklad", user_id))
    conn.commit()
    zostatok_label.config(text=f"Zostatok: {zostatok:.2f} €")
    vklad_input.delete(0, tk.END)

# funkcia na vyber penazi
def vyber():
    global zostatok
    ciastka = float(vyber_input.get())
    if ciastka <= zostatok:
        cur.execute("UPDATE users SET balance=%s WHERE id=%s", (zostatok - ciastka, user_id))
        conn.commit()
        cur.execute("SELECT balance FROM users WHERE id=%s", (user_id,))
        zostatok = cur.fetchone()[0]
        cur.execute("INSERT INTO transactions (amount, type, user_id) VALUES (%s, %s, %s)", (ciastka, "Vyber", user_id))
        conn.commit()
        zostatok_label.config(text=f"Zostatok: {zostatok:.2f} €")
        vyber_input.delete(0, tk.END)
        error_label.pack_forget()
    else:
        error_label.pack()
        error_label.config(text="Chyba: Nedostatok prostriedkov")

# zoznam transakcii
def zoznam_transakcii():
    transakcie_window = tk.Toplevel(window)
    transakcie_window.geometry("400x400")
    tk.Label(transakcie_window, text="Historia transakcii").pack()

    # ziskat transakcie z databazy
    cur.execute("SELECT amount, type FROM transactions WHERE user_id=%s", (user_id,))
    transakcie = cur.fetchall()

    for transaction in transakcie:
        tk.Label(transakcie_window, text=f"{transaction[1]}: {transaction[0]:.2f} €").pack()

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
def save_changes(novy_email, nove_heslo):
    cur.execute("UPDATE users SET email=%s, password=%s WHERE id=%s", (novy_email, nove_heslo, user_id))
    conn.commit()
    success_label.config(text="Zmeny ulozene")

window = tk.Tk()
window.geometry("400x400")

email_label = tk.Label(text="Email")
email_label.pack()

email_input = tk.Entry()
email_input.pack()
email_input.config(width=30)

password_label = tk.Label(text="Heslo")
password_label.pack()

password_input = tk.Entry(show="*")
password_input.pack(pady=5)
password_input.config(width=30)

login_button = tk.Button(text="Prihlasenie", command=handle_login)
login_button.pack()

register_button = tk.Button(text="Registracia", command=handle_register)
register_button.pack(pady=5)

error_label = tk.Label(fg="red")
error_label.pack()

success_label = tk.Label(fg="green")
success_label.pack()


# hlavna stranka
button_vklad = tk.Button(text="Vklad", command=vklad)
vklad_input = tk.Entry()
button_vyber = tk.Button(text="Vyber", command=vyber)
vyber_input = tk.Entry()
logout_button = tk.Button(text="Odhlasenie", command=logout)

view_transactions_button = tk.Button(text="Historia transakcii", command=zoznam_transakcii)
change_details_button = tk.Button(text="Upravit udaje", command=show_change_details)

zostatok_label = tk.Label(text=f"Zostatok: {zostatok:.2f} €")

window.mainloop()
