import tkinter as tk
"""
Program na simulaciu bankomatu
1. prihlasenie
2. hlavna stranka
    - vklad
    - vyber
    - zoznam transakcii
    - zmena udajov
    - odhlasenie
3. zmena udajov
    - novy email
    - nove heslo
    - ulozit
    
Autor: Patrik Gašpar - I.SB , René Havrila - I.SB , Šimon Farkaš - I.SB
"""

#TODO:
# 1. vylepsit design
# 2. vylepsit vypis transakcii
# 3. diakritika
# 4. po logine zadat pin
# 5. najst pripadne chyby
# 6. optimalizovat kod

zostatok = 0
transakcie = []
email_login = "admin"
heslo_login = "admin"

success_label = None   # globalna premenna

# funkcia na vklad penazi

def vklad():
    global zostatok
    if vklad_input.get() == "":
        error_label.config(text="Chyba: Zadajte kladnu hodnotu")
        error_label.pack()
        return
    ciastka = float(vklad_input.get())
    zostatok += ciastka
    transakcie.append((ciastka, "Vklad"))
    zostatok_label.config(text=f"Zostatok: ${zostatok:.2f}")
    vklad_input.delete(0, tk.END)
    error_label.pack_forget()

# funkcia na vyber penazi
def vyber():
    global zostatok
    if vyber_input.get() == "":
        error_label.config(text="Chyba: Zadajte kladnu hodnotu")
        error_label.pack()
        return
    ciastka = float(vyber_input.get())
    if ciastka <= zostatok:
        zostatok -= ciastka
        transakcie.append((ciastka, "Vyber"))
        zostatok_label.config(text=f"Zostatok: ${zostatok:.2f}")
        vyber_input.delete(0, tk.END)
        error_label.pack_forget()
    else:
        error_label.config(text="Chyba: Nedostatok prostriedkov")
        error_label.pack()

# zoznam transakcii
def zoznam_transakcii():
    transakcie_window = tk.Toplevel(window)
    transakcie_window.geometry("400x400")
    tk.Label(transakcie_window, text="Historia transakcii").pack()
    for transaction in transakcie:
        tk.Label(transakcie_window, text=f"{transaction[1]} - ${transaction[0]:.2f}").pack()

# zmena udajov
def show_change_details():
    global success_label
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
    success_label = tk.Label(change_window, text="Udaje boli uspesne zmenene", fg="green")

# ulozenie zmien
def save_changes(new_email, new_password):
    global email_login
    global heslo_login
    email_login = new_email
    heslo_login = new_password
    success_label.pack()

# login funkcia
def handle_login():
    email = email_input.get()
    password = password_input.get()
    if email == email_login and password == heslo_login:
        zostatok_label.pack()
        button_vklad.pack()
        vklad_input.pack()
        button_vyber.pack()
        vyber_input.pack()
        zobrazit_transakcie_button.pack()
        zmenit_udaje_button.pack()
        logout_button.pack()
        login_label.pack_forget()
        email_label.pack_forget()
        email_input.pack_forget()
        password_label.pack_forget()
        password_input.pack_forget()
        login_button.pack_forget()
        error_label.pack_forget()
    else:
        error_label.config(text="Chyba: Nespravne udaje")
        error_label.pack()

#odhlasenie
def logout():
    email_input.delete(0, tk.END)
    password_input.delete(0, tk.END)
    email_label.pack()
    email_input.pack()
    password_label.pack()
    password_input.pack()
    login_button.pack()
    error_label.pack()
    zostatok_label.pack_forget()
    button_vklad.pack_forget()
    vklad_input.pack_forget()
    button_vyber.pack_forget()
    vyber_input.pack_forget()
    zobrazit_transakcie_button.pack_forget()
    zmenit_udaje_button.pack_forget()
    logout_button.pack_forget()
    error_label.pack_forget()

window = tk.Tk()
window.title("Bankomat")
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

# hlavna stranka
button_vklad = tk.Button(text="Vklad", command=vklad)
vklad_input = tk.Entry()
button_vyber = tk.Button(text="Vyber", command=vyber)
vyber_input = tk.Entry()

zobrazit_transakcie_button = tk.Button(text="Historia transakcii", command=zoznam_transakcii)
zmenit_udaje_button = tk.Button(text="Upravit udaje", command=show_change_details)
logout_button = tk.Button(text="Odhlasenie", command=logout)
zostatok_label = tk.Label(text=f"Zostatok: ${zostatok:.2f}")

error_label = tk.Label(fg="red")
error_label.pack()

window.mainloop()
