import sqlite3
import tkinter as tk
from tkinter import simpledialog
from tkinter import ttk
from tkinter import messagebox


# Funkcje zarządzania bazą danych
def init_db():
    conn = sqlite3.connect('cookbook.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS recipes
                 (id INTEGER PRIMARY KEY,
                  title TEXT NOT NULL,
                  ingredients TEXT NOT NULL,
                  instructions TEXT NOT NULL,
                  category TEXT NOT NULL)''')
    conn.commit()
    conn.close()


def add_recipe(recipe_id, title, ingredients, instructions, category):
    conn = sqlite3.connect('cookbook.db')
    c = conn.cursor()
    c.execute("INSERT INTO recipes (id, title, ingredients, instructions, category) VALUES (?, ?, ?, ?, ?)",
              (recipe_id, title, ingredients, instructions, category))
    conn.commit()
    conn.close()


def edit_recipe(recipe_id, title, ingredients, instructions, category):
    conn = sqlite3.connect('cookbook.db')
    c = conn.cursor()
    c.execute("UPDATE recipes SET title = ?, ingredients = ?, instructions = ?, category = ? WHERE id = ?",
              (title, ingredients, instructions, category, recipe_id))
    conn.commit()
    conn.close()


def delete_recipe(recipe_id):
    conn = sqlite3.connect('cookbook.db')
    c = conn.cursor()
    c.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
    conn.commit()
    conn.close()


def get_recipes():
    conn = sqlite3.connect('cookbook.db')
    c = conn.cursor()
    c.execute("SELECT id, title, category FROM recipes ORDER BY id")
    recipes = c.fetchall()
    conn.close()
    return recipes


def get_recipe_details(recipe_id):
    conn = sqlite3.connect('cookbook.db')
    c = conn.cursor()
    c.execute("SELECT title, ingredients, instructions, category FROM recipes WHERE id = ?", (recipe_id,))
    recipe = c.fetchone()
    conn.close()
    return recipe


# Klasa aplikacji GUI
class CookbookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Elektroniczna Książka Kucharska")

        self.tree = ttk.Treeview(root, columns=('Numer', 'Title', 'Category'), show='headings')
        self.tree.heading('Numer', text='Numer')
        self.tree.heading('Title', text='Tytuł')
        self.tree.heading('Category', text='Kategoria')
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.bind('<Double-1>', self.show_recipe_details)

        self.load_recipes()

        add_button = tk.Button(root, text="Dodaj Przepis", command=self.add_recipe)
        add_button.pack(side=tk.LEFT)

        edit_button = tk.Button(root, text="Edytuj Przepis", command=self.edit_recipe)
        edit_button.pack(side=tk.LEFT)

        delete_button = tk.Button(root, text="Usuń Przepis", command=self.delete_recipe)
        delete_button.pack(side=tk.LEFT)

    def load_recipes(self):
        for recipe in self.tree.get_children():
            self.tree.delete(recipe)
        for recipe in get_recipes():
            self.tree.insert('', tk.END, values=recipe)

    def add_recipe(self):
        recipe_id = simpledialog.askinteger("Dodaj Przepis", "Podaj numer:")
        if recipe_id is not None:
            title = simpledialog.askstring("Dodaj Przepis", "Podaj tytuł:")
            if title:
                ingredients = simpledialog.askstring("Dodaj Przepis", "Podaj składniki:")
                instructions = simpledialog.askstring("Dodaj Przepis", "Podaj instrukcje:")
                category = simpledialog.askstring("Dodaj Przepis", "Podaj kategorię:")
                if ingredients and instructions and category:
                    add_recipe(recipe_id, title, ingredients, instructions, category)
                    self.load_recipes()

    def edit_recipe(self):
        selected_item = self.tree.selection()
        if selected_item:
            recipe_id = self.tree.item(selected_item)['values'][0]
            title = simpledialog.askstring("Edytuj Przepis", "Podaj tytuł:")
            if title:
                ingredients = simpledialog.askstring("Edytuj Przepis", "Podaj składniki:")
                instructions = simpledialog.askstring("Edytuj Przepis", "Podaj instrukcje:")
                category = simpledialog.askstring("Edytuj Przepis", "Podaj kategorię:")
                if ingredients and instructions and category:
                    edit_recipe(recipe_id, title, ingredients, instructions, category)
                    self.load_recipes()

    def delete_recipe(self):
        selected_item = self.tree.selection()
        if selected_item:
            recipe_id = self.tree.item(selected_item)['values'][0]
            delete_recipe(recipe_id)
            self.load_recipes()

    def show_recipe_details(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            recipe_id = self.tree.item(selected_item)['values'][0]
            recipe = get_recipe_details(recipe_id)
            if recipe:
                title, ingredients, instructions, category = recipe
                detail_window = tk.Toplevel(self.root)
                detail_window.title(f"Przepis: {title}")
                detail_text = f"Tytuł: {title}\n\nSkładniki:\n{ingredients}\n\nInstrukcje:\n{instructions}"
                label = tk.Label(detail_window, text=detail_text, justify=tk.LEFT)
                label.pack(padx=10, pady=10)


if __name__ == '__main__':
    init_db()
    root = tk.Tk()
    app = CookbookApp(root)
    root.mainloop()
