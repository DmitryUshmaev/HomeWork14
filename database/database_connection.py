import sqlite3


# Класс для подключения и поиска по базе данных

class DatabaseConnection:

    def __init__(self, database):
        self.database = database

    def _get_db_cursor(self):
        """Получение курсора """

        try:
            with sqlite3.connect(self.database) as connection:
                cursor = connection.cursor()

            return cursor
        except sqlite3.Error:
            print("Ошибка подключения к sqlite")

    def _get_query(self, query):
        """Создание запроса и возвращение результата по запросу"""

        cursor = self._get_db_cursor()
        cursor.execute(query)
        fetched = cursor.fetchall()

        return fetched

    def get_title_by_name(self, title_name):
        """Поиск фильма по названию"""

        title_name = str(title_name).lower().strip()
        titles = {}
        fetched = self._get_query(f"SELECT title, country, release_year, listed_in, description "
                                  f"FROM netflix "
                                  f"WHERE title LIKE '%{title_name}%' "
                                  f"ORDER BY release_year DESC "
                                  f"LIMIT 1")

        for row in fetched:
            titles["title"] = row[0]
            titles["country"] = row[1]
            titles["release_year"] = row[2]
            titles["genre"] = row[3]
            titles["description"] = row[4]

        return titles

    def get_by_release_year(self, year_one, year_two):
        """Поиск фильмов по датам"""

        year_one = str(year_one)
        year_two = str(year_two)

        fetched = self._get_query(f"SELECT title, release_year "
                                  f"FROM netflix "
                                  f"WHERE release_year IN ('{year_one}', '{year_two}') "
                                  f"ORDER BY release_year DESC "
                                  f"LIMIT 100")
        titles = []
        for row in fetched:
            titles.append({"title": row[0], "release_year": row[1]})

        return titles

    def get_by_rating(self):
        """Поиск фильмов по рейтингу"""

        fetched = self._get_query("SELECT title, rating, description FROM netflix")
        titles = []
        for row in fetched:
            titles.append({"title": row[0], "rating": row[1], "description": row[2]})

        return titles

    def get_by_genre(self, genre):
        """Поиск фильмов по жанру"""

        genre = str(genre)

        fetched = self._get_query(f"SELECT title, description "
                                  f"FROM netflix "
                                  f"WHERE listed_in LIKE '%{genre}%' "
                                  f"ORDER by release_year DESC "
                                  f"LIMIT 10")
        titles = []
        for row in fetched:
            titles.append({"title": row[0], "description": row[1]})

        return titles

    def get_by_genre_type_year(self, type_movie, release_year, listed_in):
        """Поиск фильмов по их типу, году выпуска и жанру"""

        type_movie = str(type_movie).lower().strip()
        release_year = str(release_year)
        listed_in = str(listed_in).lower().strip()

        fetched = self._get_query(f"SELECT title, release_year, listed_in, type "
                                  f"FROM netflix "
                                  f"WHERE type LIKE '%{type_movie}%'"
                                  f"AND release_year LIKE '%{release_year}%'"
                                  f"AND listed_in LIKE '%{listed_in}%'"
                                  f"LIMIT 10")

        titles = []
        for row in fetched:
            titles.append({"title": row[0], "release_year": row[1], "listed_in": row[2], "type": row[3]})

        return titles

    def get_by_names(self, name_one, name_two):
        """Поиск актеров"""

        name_one = str(name_one).lower()
        name_two = str(name_two).lower()

        fetched = self._get_query(f"SELECT cast "
                                  f"FROM netflix "
                                  f"WHERE cast LIKE '%{name_one}%' "
                                  f"AND cast LIKE '%{name_two}%' "
                                  f"LIMIT 10")

        titles = []

        for row in fetched:
            titles.append(row)

        return titles
