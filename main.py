"""
Autor: Šimon Farkaš I.SB, Patrik Gašpar I.SB, René Havrila I.SB
Popis: Bankomat

Premenne:
    zostatok - premenna, ktora uchovava aktualny zostatok na ucte
    transakcie - premenna, ktora uchovava zoznam transakcii
    email_login - premenna, ktora uchovava email prihlaseneho pouzivatela
    heslo_login - premenna, ktora uchovava heslo prihlaseneho pouzivatela

Funckie:
    prihlasit() - prihlasi pouzivatela
    odhlasit() - odhlasi pouzivatela
    transakcia(hodnota, typ) - vykona transakciu
    zoznam_transakcii() - zobrazi zoznam transakcii
    zmenit_udaje() - zmeni udaje pouzivatela
    ulozit_zmeny(zmenit_udaje_okno, novy_email, nove_heslo) - ulozi zmeny udajov pouzivatela

"""

import tkinter as tk

zostatok = 0
transakcie = []
email_login = "admin"
heslo_login = "admin"

def prihlasit():
    email = email_input.get()
    heslo = heslo_input.get()
    if email == email_login and heslo == heslo_login:
        for widget in [login_label, email_label, email_input, heslo_label, heslo_input, login_button, chyba]:
            widget.pack_forget()
        for widget in [zostatok_label,input,buttons,zobrazit_transakcie_button,zmenit_udaje_button,odhlasit_button]:
            widget.pack()
    else:
        chyba.config(text="Chyba: Nespravne udaje")
        chyba.pack()

def odhlasit():
    email_input.delete(0, tk.END)
    heslo_input.delete(0, tk.END)
    for widget in [zostatok_label, buttons, input, zobrazit_transakcie_button, zmenit_udaje_button, odhlasit_button, chyba]:
        widget.pack_forget()
    for widget in [login_label, email_label, email_input, heslo_label, heslo_input, login_button]:
        widget.pack()
def transakcia(hodnota, typ):
    global zostatok
    if hodnota <= 0 or hodnota == "":
        chyba.config(text="Chyba: Zadajte kladnu hodnotu")
        chyba.pack()
    elif typ == "Vklad":
        zostatok += hodnota
        transakcie.append((hodnota, typ))
        zostatok_label.config(text=f"Zostatok: {zostatok:.2f} €")
        input.delete(0, tk.END)
        chyba.pack_forget()
    elif typ == "Vyber":
        if hodnota <= zostatok:
            zostatok -= hodnota
            transakcie.append((hodnota, typ))
            zostatok_label.config(text=f"Zostatok: {zostatok:.2f} €")
            input.delete(0, tk.END)
            chyba.pack_forget()
        else:
            chyba.config(text="Chyba: Nedostatok prostriedkov")
            chyba.pack()
def zoznam_transakcii():
    transakcie_okno = tk.Toplevel(okno)
    transakcie_okno.geometry("400x400")
    tk.Label(transakcie_okno, text="Historia transakcii").pack()
    for hodnota, typ in transakcie:
        tk.Label(transakcie_okno, text=f"{typ} - {hodnota:.2f} €").pack()
def zmenit_udaje():
    zmenit_udaje_okno = tk.Toplevel(okno)
    zmenit_udaje_okno.geometry("400x400")
    tk.Label(zmenit_udaje_okno, text="Upravit udaje").pack()
    tk.Label(zmenit_udaje_okno, text="Novy email").pack()
    novy_email = tk.Entry(zmenit_udaje_okno)
    novy_email.pack()
    tk.Label(zmenit_udaje_okno, text="Nove heslo").pack()
    nove_heslo = tk.Entry(zmenit_udaje_okno, show="*")
    nove_heslo.pack()
    tk.Button(zmenit_udaje_okno, text="Ulozit", command=lambda: ulozit_zmeny(zmenit_udaje_okno, novy_email.get(), nove_heslo.get())).pack()
def ulozit_zmeny(zmenit_udaje_okno, novy_email, nove_heslo):
    global email_login, heslo_login
    email_login = novy_email
    heslo_login = nove_heslo
    success_label = tk.Label(zmenit_udaje_okno, text="Udaje boli uspesne zmenene", fg="green")
    success_label.pack()

okno = tk.Tk()
okno.title("Bankomat")
okno.geometry("400x400")

login_label = tk.Label(okno, text="Prihlasenie")
email_label = tk.Label(okno, text="Email")
email_input = tk.Entry(okno)
heslo_label = tk.Label(okno, text="Heslo")
heslo_input = tk.Entry(okno, show="*")
login_button = tk.Button(okno, text="Prihlasenie", command=prihlasit)

for widget in [login_label, email_label, email_input, heslo_label, heslo_input, login_button]:
    widget.pack()

buttons = tk.Frame(okno)

def handle_vklad():
    hodnota = input.get()
    if hodnota:
        transakcia(float(hodnota), "Vklad")
    else:
        chyba.config(text="Chyba: Zadajte hodnotu")
        chyba.pack()
def handle_vyber():
    hodnota = input.get()
    if hodnota:
        transakcia(float(hodnota), "Vyber")
    else:
        chyba.config(text="Chyba: Zadajte hodnotu")
        chyba.pack()

button_vklad = tk.Button(buttons, text="Vklad", command=handle_vklad)
button_vklad.grid(row=0, column=0, padx=5, pady=5)

button_vyber = tk.Button(buttons, text="Vyber", command=handle_vyber)
button_vyber.grid(row=0, column=1, padx=5, pady=5)

input = tk.Entry(okno)

zostatok_label = tk.Label(okno, text=f"Zostatok: {zostatok:.2f} €")
zobrazit_transakcie_button = tk.Button(okno, text="Historia transakcii", command=zoznam_transakcii)
zmenit_udaje_button = tk.Button(okno, text="Upravit udaje", command=zmenit_udaje)
odhlasit_button = tk.Button(okno, text="Odhlasenie", command=odhlasit)
chyba = tk.Label(okno, fg="red")

okno.mainloop()