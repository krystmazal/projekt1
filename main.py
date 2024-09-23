import tkinter as tk
from tkinter import ttk, messagebox
from baza import Database

baza = Database(host="localhost", user="root", password="", database="notatnik")
baza.create_tables()

def rejestracja():
    login = login_entry.get().strip()
    password = haslo_entry.get().strip()

    if login and password:
        if baza.check_user(login, password):
            messagebox.showerror(title="Error", message="Taki użytkownik już istnieje")
        else:
            baza.insert_user(login, password)
            otworz_notatnik(login)
    else:
        messagebox.showerror(title="Error", message="Podaj login i hasło")

def logowanie():
    login = login_entry.get().strip()
    password = haslo_entry.get().strip()

    user = baza.check_user(login, password)

    if user:
        otworz_notatnik(login)
    else:
        messagebox.showerror(title="Error", message="Błędny login lub hasło")

def otworz_notatnik(login):
    login_frame.destroy()
    root.geometry("1100x600")
    notatnik_frame = tk.Frame(root)
    notatnik_frame.grid(padx=20, pady=20)

    tk.Label(notatnik_frame, text=f"Witaj, {login}", font=("Arial", 16)).grid(row=1, column=0, columnspan=2, sticky="w", padx=10, pady=10)

 
    tk.Label(notatnik_frame, text="Twoje notatki", font=("Arial", 16)).grid(row=1, column=1, sticky="w", padx=10, pady=5)

    note_entry = tk.Text(notatnik_frame, height=15, width=40, font=("Arial", 16))
    note_entry.grid(row=2, column=0, padx=10, pady=10, sticky="n")

    notes_listbox = tk.Listbox(notatnik_frame, height=15, width=50, font=("Arial", 14))
    notes_listbox.grid(row=2, column=1, padx=10, pady=10, sticky="n")

    notes_listbox.bind('<<ListboxSelect>>', lambda event: wyswietl_zaznaczona_note(notes_listbox, note_entry, login))

    # Buttons aligned on the same row
    dodaj_btn = ttk.Button(notatnik_frame, text="Dodaj notatkę", command=lambda: dodaj_notatke(note_entry, login, notes_listbox))
    dodaj_btn.grid(row=3, column=0, padx=10, pady=5, sticky="w")

    usun_notatke_btn = ttk.Button(notatnik_frame, text="Usuń notatkę", command=lambda: usun_wybrana_note(notes_listbox, note_entry, login))
    usun_notatke_btn.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    wyloguj_btn = ttk.Button(notatnik_frame, text="Wyloguj", command=lambda: wyloguj(notatnik_frame))
    wyloguj_btn.grid(row=4, column=1, padx=10, pady=20, sticky="e")

    wyswietl_notes(notes_listbox, login)

def dodaj_notatke(note_entry, login, notes_listbox):
    text = note_entry.get("1.0", tk.END).strip()
    if text:
        user_id = baza.get_user_id(login)
        baza.insert_note(text, user_id)
        note_entry.delete("1.0", tk.END)
        wyswietl_notes(notes_listbox, login)
    else:
        messagebox.showerror(title="Error", message="Notatka nie może być pusta")

def wyswietl_notes(notes_listbox, login):
    notes_listbox.delete(0, tk.END)
    user_id = baza.get_user_id(login)
    notes = baza.select_notes_by_user(user_id)

    if not notes:
        notes_listbox.insert(tk.END, "Brak notatek")
    else:
        for note in notes:
            short_text = (note[1][:41] + '...') if len(note[1]) > 30 else note[1]
            timestamp = note[3].strftime('%d-%m-%Y')
            notes_listbox.insert(tk.END, f"{short_text}  {timestamp}")

def wyswietl_zaznaczona_note(notes_listbox, note_entry, login):
    selected_index = notes_listbox.curselection()
    if selected_index:
        selected_index = selected_index[0]
        user_id = baza.get_user_id(login)
        notes = baza.select_notes_by_user(user_id)
        if selected_index < len(notes):
            note_entry.delete("1.0", tk.END)
            note_entry.insert(tk.END, notes[selected_index][1])

def usun_wybrana_note(notes_listbox, note_entry, login):
    selected_index = notes_listbox.curselection()
    if selected_index:
        selected_index = selected_index[0]
        user_id = baza.get_user_id(login)
        notes = baza.select_notes_by_user(user_id)
        if selected_index < len(notes):
            note_id = notes[selected_index][0]
            baza.delete_note(note_id)
            note_entry.delete("1.0", tk.END)
            wyswietl_notes(notes_listbox, login)

def wyloguj(notatnik_frame):
    notatnik_frame.destroy()
    root.geometry("250x200")
    zaladuj_okno_logowania()

def zaladuj_okno_logowania():
    global login_frame

    login_frame = tk.Frame(root)
    login_frame.grid(pady=20)

    login_label = ttk.Label(login_frame, text="Login:")
    login_label.grid(row=0, column=0, padx=10, pady=5)

    global login_entry
    login_entry = ttk.Entry(login_frame)
    login_entry.grid(row=0, column=1, padx=10, pady=5)

    haslo_label = ttk.Label(login_frame, text="Hasło:")
    haslo_label.grid(row=1, column=0, padx=10, pady=5)

    global haslo_entry
    haslo_entry = ttk.Entry(login_frame, show="*")
    haslo_entry.grid(row=1, column=1, padx=10, pady=5)

    logowanie_btn = ttk.Button(login_frame, text="Zaloguj", command=logowanie)
    logowanie_btn.grid(row=2, column=1, padx=10, pady=1)

    rejestracja_btn = ttk.Button(login_frame, text="Zarejestruj", command=rejestracja)
    rejestracja_btn.grid(row=3, column=1, padx=10, pady=1)

root = tk.Tk()
root.title("Notatnik")
root.geometry("250x200")

zaladuj_okno_logowania()

root.mainloop()
