import sqlite3
import tkinter as tk
from tkinter import simpledialog
from tkinter import ttk
from tkinter import messagebox

def inicjalizuj_baze():
    polaczenie = sqlite3.connect('ksiazka_kucharska.db')
    kursor = polaczenie.cursor()
    kursor.execute('''CREATE TABLE IF NOT EXISTS przepisy
                      (id INTEGER PRIMARY KEY,
                       tytul TEXT NOT NULL,
                       skladniki TEXT NOT NULL,
                       instrukcje TEXT NOT NULL,
                       kategoria TEXT NOT NULL)''')
    polaczenie.commit()
    polaczenie.close()

def dodaj_przepis(id_przepisu, tytul, skladniki, instrukcje, kategoria):
    polaczenie = sqlite3.connect('ksiazka_kucharska.db')
    kursor = polaczenie.cursor()
    kursor.execute("INSERT INTO przepisy (id, tytul, skladniki, instrukcje, kategoria) VALUES (?, ?, ?, ?, ?)",
                   (id_przepisu, tytul, skladniki, instrukcje, kategoria))
    polaczenie.commit()
    polaczenie.close()

def edytuj_przepis(id_przepisu, tytul, skladniki, instrukcje, kategoria):
    polaczenie = sqlite3.connect('ksiazka_kucharska.db')
    kursor = polaczenie.cursor()
    kursor.execute("UPDATE przepisy SET tytul = ?, skladniki = ?, instrukcje = ?, kategoria = ? WHERE id = ?",
                   (tytul, skladniki, instrukcje, kategoria, id_przepisu))
    polaczenie.commit()
    polaczenie.close()

def usun_przepis(id_przepisu):
    polaczenie = sqlite3.connect('ksiazka_kucharska.db')
    kursor = polaczenie.cursor()
    kursor.execute("DELETE FROM przepisy WHERE id = ?", (id_przepisu,))
    polaczenie.commit()
    polaczenie.close()

def pobierz_przepisy():
    polaczenie = sqlite3.connect('ksiazka_kucharska.db')
    kursor = polaczenie.cursor()
    kursor.execute("SELECT id, tytul, kategoria FROM przepisy ORDER BY id")
    przepisy = kursor.fetchall()
    polaczenie.close()
    return przepisy

def pobierz_szczegoly_przepisu(id_przepisu):
    polaczenie = sqlite3.connect('ksiazka_kucharska.db')
    kursor = polaczenie.cursor()
    kursor.execute("SELECT tytul, skladniki, instrukcje, kategoria FROM przepisy WHERE id = ?", (id_przepisu,))
    przepis = kursor.fetchone()
    polaczenie.close()
    return przepis

class AplikacjaKsiazkaKucharska:
    def __init__(self, okno_glowne):
        self.okno_glowne = okno_glowne
        self.okno_glowne.title("Elektroniczna Książka Kucharska")

        self.drzewo = ttk.Treeview(okno_glowne, columns=('Numer', 'Tytul', 'Kategoria'), show='headings')
        self.drzewo.heading('Numer', text='Numer')
        self.drzewo.heading('Tytul', text='Tytuł')
        self.drzewo.heading('Kategoria', text='Kategoria')
        self.drzewo.pack(fill=tk.BOTH, expand=True)

        self.drzewo.bind('<Double-1>', self.pokaz_szczegoly_przepisu)

        self.wczytaj_przepisy()

        przycisk_dodaj = tk.Button(okno_glowne, text="Dodaj Przepis", command=self.dodaj_przepis)
        przycisk_dodaj.pack(side=tk.LEFT)

        przycisk_edytuj = tk.Button(okno_glowne, text="Edytuj Przepis", command=self.edytuj_przepis)
        przycisk_edytuj.pack(side=tk.LEFT)

        przycisk_usun = tk.Button(okno_glowne, text="Usuń Przepis", command=self.usun_przepis)
        przycisk_usun.pack(side=tk.LEFT)

    def wczytaj_przepisy(self):
        for przepis in self.drzewo.get_children():
            self.drzewo.delete(przepis)
        for przepis in pobierz_przepisy():
            self.drzewo.insert('', tk.END, values=przepis)

    def dodaj_przepis(self):
        try:
            id_przepisu = simpledialog.askinteger("Dodaj Przepis", "Podaj numer:", parent=self.okno_glowne)
            if id_przepisu is not None:
                tytul = simpledialog.askstring("Dodaj Przepis", "Podaj tytuł:", parent=self.okno_glowne)
                if tytul:
                    skladniki = simpledialog.askstring("Dodaj Przepis", "Podaj składniki:", parent=self.okno_glowne)
                    instrukcje = simpledialog.askstring("Dodaj Przepis", "Podaj instrukcje:", parent=self.okno_glowne)
                    kategoria = simpledialog.askstring("Dodaj Przepis", "Podaj kategorię:", parent=self.okno_glowne)
                    if skladniki and instrukcje and kategoria:
                        dodaj_przepis(id_przepisu, tytul, skladniki, instrukcje, kategoria)
                        self.wczytaj_przepisy()
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd podczas dodawania przepisu: {e}")

    def edytuj_przepis(self):
        wybrany_element = self.drzewo.selection()
        if wybrany_element:
            try:
                id_przepisu = self.drzewo.item(wybrany_element)['values'][0]
                tytul = simpledialog.askstring("Edytuj Przepis", "Podaj tytuł:", parent=self.okno_glowne)
                if tytul:
                    skladniki = simpledialog.askstring("Edytuj Przepis", "Podaj składniki:", parent=self.okno_glowne)
                    instrukcje = simpledialog.askstring("Edytuj Przepis", "Podaj instrukcje:", parent=self.okno_glowne)
                    kategoria = simpledialog.askstring("Edytuj Przepis", "Podaj kategorię:", parent=self.okno_glowne)
                    if skladniki and instrukcje and kategoria:
                        edytuj_przepis(id_przepisu, tytul, skladniki, instrukcje, kategoria)
                        self.wczytaj_przepisy()
            except Exception as e:
                messagebox.showerror("Błąd", f"Wystąpił błąd podczas edytowania przepisu: {e}")

    def usun_przepis(self):
        wybrany_element = self.drzewo.selection()
        if wybrany_element:
            try:
                id_przepisu = self.drzewo.item(wybrany_element)['values'][0]
                usun_przepis(id_przepisu)
                self.wczytaj_przepisy()
            except Exception as e:
                messagebox.showerror("Błąd", f"Wystąpił błąd podczas usuwania przepisu: {e}")

    def pokaz_szczegoly_przepisu(self, event):
        wybrany_element = self.drzewo.selection()
        if wybrany_element:
            try:
                id_przepisu = self.drzewo.item(wybrany_element)['values'][0]
                przepis = pobierz_szczegoly_przepisu(id_przepisu)
                if przepis:
                    tytul, skladniki, instrukcje, kategoria = przepis
                    okno_szczegolow = tk.Toplevel(self.okno_glowne)
                    okno_szczegolow.title(f"Przepis: {tytul}")
                    tekst_szczegolow = f"Tytuł: {tytul}\n\nSkładniki:\n{skladniki}\n\nInstrukcje:\n{instrukcje}"
                    etykieta = tk.Label(okno_szczegolow, text=tekst_szczegolow, justify=tk.LEFT)
                    etykieta.pack(padx=10, pady=10)
                    
                    okno_szerokosc = 300
                    okno_wysokosc = 200
                    szerokosc_ekranu = self.okno_glowne.winfo_width()
                    wysokosc_ekranu = self.okno_glowne.winfo_height()
                    x_pozycja = self.okno_glowne.winfo_rootx() + (szerokosc_ekranu // 2) - (okno_szerokosc // 2)
                    y_pozycja = self.okno_glowne.winfo_rooty() + (wysokosc_ekranu // 2) - (okno_wysokosc // 2)
                    okno_szczegolow.geometry(f"{okno_szerokosc}x{okno_wysokosc}+{x_pozycja}+{y_pozycja}")

                    okno_szczegolow.transient(self.okno_glowne)
                    okno_szczegolow.grab_set()
            except Exception as e:
                messagebox.showerror("Błąd", f"Wystąpił błąd podczas wyświetlania szczegółów przepisu: {e}")

if __name__ == '__main__':
    try:
        inicjalizuj_baze()
        okno_glowne = tk.Tk()
        aplikacja = AplikacjaKsiazkaKucharska(okno_glowne)
        okno_glowne.mainloop()
    except Exception as e:
        messagebox.showerror("Błąd", f"Wystąpił błąd podczas uruchamiania aplikacji: {e}")
