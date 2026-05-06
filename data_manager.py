import json
import os

class DataManager:
    def __init__(self, filename):
        self.filename = filename

    def load_movies(self):
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_movies(self, movies):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(movies, f, ensure_ascii=False, indent=4)