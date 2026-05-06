import tkinter as tk
from tkinter import ttk, messagebox
from data_manager import DataManager
from validator import validate_movie

class MovieLibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library - Личная кинотека")
        self.root.geometry("800x500")

        self.data_manager = DataManager("movies.json")
        self.movies = self.data_manager.load_movies()

        # Интерфейс
        self.create_input_fields()
        self.create_buttons()
        self.create_table()
        self.update_table()

    def create_input_fields(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        # Название
        tk.Label(frame, text="Название:").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = tk.Entry(frame, width=30)
        self.title_entry.grid(row=0, column=1)

        # Жанр
        tk.Label(frame, text="Жанр:").grid(row=0, column=2, padx=5)
        self.genre_entry = tk.Entry(frame, width=15)
        self.genre_entry.grid(row=0, column=3)

        # Год
        tk.Label(frame, text="Год:").grid(row=0, column=4, padx=5)
        self.year_entry = tk.Entry(frame, width=10)
        self.year_entry.grid(row=0, column=5)

        # Рейтинг
        tk.Label(frame, text="Рейтинг (0-10):").grid(row=0, column=6, padx=5)
        self.rating_entry = tk.Entry(frame, width=10)
        self.rating_entry.grid(row=0, column=7)

    def create_buttons(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=5)

        tk.Button(frame, text="Добавить фильм", command=self.add_movie, bg="lightblue").pack(side=tk.LEFT, padx=5)

        # Фильтры
        tk.Label(frame, text="Фильтр по жанру:").pack(side=tk.LEFT, padx=(20,5))
        self.filter_genre_entry = tk.Entry(frame, width=15)
        self.filter_genre_entry.pack(side=tk.LEFT)
        
        tk.Label(frame, text="Год:").pack(side=tk.LEFT, padx=(10,5))
        self.filter_year_entry = tk.Entry(frame, width=10)
        self.filter_year_entry.pack(side=tk.LEFT)

        tk.Button(frame, text="Применить фильтр", command=self.apply_filter).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Сбросить фильтр", command=self.reset_filter).pack(side=tk.LEFT)

    def create_table(self):
        self.tree = ttk.Treeview(self.root, columns=("Название", "Жанр", "Год", "Рейтинг"), show="headings")
        for col in ("Название", "Жанр", "Год", "Рейтинг"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def add_movie(self):
        title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()
        year = self.year_entry.get().strip()
        rating = self.rating_entry.get().strip()

        is_valid, error = validate_movie(title, genre, year, rating)
        if not is_valid:
            messagebox.showerror("Ошибка ввода", error)
            return

        # Добавляем
        movie = {
            "title": title,
            "genre": genre,
            "year": int(year),
            "rating": float(rating)
        }
        self.movies.append(movie)
        self.data_manager.save_movies(self.movies)
        self.update_table()
        self.clear_inputs()

    def update_table(self, movies_to_show=None):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        data = movies_to_show if movies_to_show is not None else self.movies
        for m in data:
            self.tree.insert("", tk.END, values=(m["title"], m["genre"], m["year"], m["rating"]))

    def apply_filter(self):
        genre_filter = self.filter_genre_entry.get().strip().lower()
        year_filter = self.filter_year_entry.get().strip()

        filtered = self.movies[:]
        if genre_filter:
            filtered = [m for m in filtered if genre_filter in m["genre"].lower()]
        if year_filter:
            try:
                year_int = int(year_filter)
                filtered = [m for m in filtered if m["year"] == year_int]
            except ValueError:
                messagebox.showwarning("Некорректный год", "Год фильтра должен быть числом")
                return
        self.update_table(filtered)

    def reset_filter(self):
        self.filter_genre_entry.delete(0, tk.END)
        self.filter_year_entry.delete(0, tk.END)
        self.update_table()

    def clear_inputs(self):
        self.title_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibraryApp(root)
    root.mainloop()