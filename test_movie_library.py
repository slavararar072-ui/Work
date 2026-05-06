import unittest
import os
from validator import validate_movie
from data_manager import DataManager

class TestMovieLibrary(unittest.TestCase):
    
    def test_validate_movie_positive(self):
        result, msg = validate_movie("Интерстеллар", "Фантастика", "2014", "8.6")
        self.assertTrue(result)
    
    def test_validate_movie_empty_title(self):
        result, _ = validate_movie("", "Драма", "2020", "7.5")
        self.assertFalse(result)
    
    def test_validate_invalid_year_format(self):
        result, _ = validate_movie("Фильм", "Комедия", "abv", "5")
        self.assertFalse(result)
    
    def test_validate_year_out_of_range_low(self):
        result, _ = validate_movie("Старый фильм", "История", "1800", "5")
        self.assertFalse(result)
    
    def test_validate_year_out_of_range_high(self):
        result, _ = validate_movie("Будущий фильм", "Фантастика", "2050", "9")
        self.assertFalse(result)
    
    def test_validate_rating_too_low(self):
        result, _ = validate_movie("Плохой фильм", "Ужасы", "2022", "-1")
        self.assertFalse(result)
    
    def test_validate_rating_too_high(self):
        result, _ = validate_movie("Отличный фильм", "Боевик", "2023", "11")
        self.assertFalse(result)
    
    def test_validate_rating_string(self):
        result, _ = validate_movie("Фильм", "Драма", "2021", "abc")
        self.assertFalse(result)
    
    def test_data_manager_save_load(self):
        test_file = "test_movies.json"
        dm = DataManager(test_file)
        test_data = [{"title": "Тест", "genre": "Триллер", "year": 2023, "rating": 7.5}]
        dm.save_movies(test_data)
        loaded = dm.load_movies()
        self.assertEqual(loaded, test_data)
        if os.path.exists(test_file):
            os.remove(test_file)

if __name__ == "__main__":
    unittest.main()