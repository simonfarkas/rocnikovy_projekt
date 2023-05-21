import tkinter as tk

zostatok = 0
transakcie = []
email_login = "admin"
heslo_login = "admin"

success_label = None   # globalna premenna

# funkcia na vklad penazi
def vklad():
    global zostatok
    if input.get() == "":
        error_label.config(text="Chyba: Zadajte kladnu hodnotu")
        error_label.pack()
        return
    ciastka = float(input.get())
    zostatok += ciastka
    transakcie.append((ciastka, "Vklad"))
    zostatok_label.config(text=f"Zostatok: ${zostatok:.2f}")
    input.delete(0, tk.END)
    error_label.pack_forget()

# funkcia na vyber penazi
def vyber():
    global zostatok
    if input.get() == "":
        error_label.config(text="Chyba: Zadajte kladnu hodnotu")
        error_label.pack()
        return
    ciastka = float(input.get())
    if ciastka <= zostatok:
        zostatok -= ciastka
        transakcie.append((ciastka, "Vyber"))
        zostatok_label.config(text=f"Zostatok: ${zostatok:.2f}")
        input.delete(0, tk.END)
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
        input.pack()
        buttons.pack()
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
    buttons.pack_forget()
    input.pack_forget()
    zobrazit_transakcie_button.pack_forget()
    zmenit_udaje_button.pack_forget()
    logout_button.pack_forget()
    error_label.pack_forget()

window = tk.Tk()
window.title("Bankomat")
window.geometry("400x400")

# prihlasenie
login_label = tk.Label(window, text="Prihlasenie")
login_label.pack()

email_label = tk.Label(window, text="Email")
email_label.pack()

email_input = tk.Entry(window)
email_input.pack()

password_label = tk.Label(window, text="Heslo")
password_label.pack()

password_input = tk.Entry(window, show="*")
password_input.pack()

login_button = tk.Button(window, text="Prihlasenie", command=handle_login)
login_button.pack()

# hlavna stranka
buttons = tk.Frame(window)

button_vklad = tk.Button(buttons, text="Vklad", command=vklad)
button_vklad.grid(row=0, column=0, padx=5, pady=5)

button_vyber = tk.Button(buttons, text="Vyber", command=vyber)
button_vyber.grid(row=0, column=1, padx=5, pady=5)

input = tk.Entry(window)

zostatok_label = tk.Label(window, text=f"Zostatok: ${zostatok:.2f}")
zobrazit_transakcie_button = tk.Button(window, text="Historia transakcii", command=zoznam_transakcii)
zmenit_udaje_button = tk.Button(window, text="Upravit udaje", command=show_change_details)
logout_button = tk.Button(window, text="Odhlasenie", command=logout)
error_label = tk.Label(window, fg="red")

window.mainloop()
