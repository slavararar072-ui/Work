def validate_movie(title, genre, year, rating):
    if not title:
        return False, "Название не может быть пустым"
    if not genre:
        return False, "Жанр не может быть пустым"
    
    # Год
    try:
        year_int = int(year)
        if year_int < 1888 or year_int > 2030:
            return False, "Год должен быть от 1888 до 2030"
    except ValueError:
        return False, "Год должен быть числом"
    
    # Рейтинг
    try:
        rating_float = float(rating)
        if rating_float < 0 or rating_float > 10:
            return False, "Рейтинг должен быть от 0 до 10"
    except ValueError:
        return False, "Рейтинг должен быть числом"
    
    return True, "OK"