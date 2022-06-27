from database.database_connection import DatabaseConnection
from flask import Flask, jsonify

database = DatabaseConnection("database/netflix.db")

app = Flask(__name__)


@app.route('/')
def index_page():
    return "Главная страница"


@app.route('/movie/<title>')
def title_page(title):
    return database.get_title_by_name(title)


@app.route('/movie/<year_one>/to/<year_two>')
def year_page(year_one, year_two):
    return jsonify(database.get_by_release_year(year_one, year_two))


@app.route('/rating/children')
def rating_children_page():
    rating_children = [row for row in database.get_by_rating() if row.get('rating') == 'G']

    return jsonify(rating_children)


@app.route('/rating/family')
def rating_family_page():
    rating_family = [row for row in database.get_by_rating() if row.get('rating') in ('G', 'PG', 'PG-13')]

    return jsonify(rating_family)


@app.route('/rating/adult')
def rating_adult_page():
    rating_adult = [row for row in database.get_by_rating() if row.get('rating') in ('R', 'NC-17')]

    return jsonify(rating_adult)


@app.route('/movie/<genre>')
def genre_page(genre):
    return jsonify(database.get_by_genre(genre))


@app.errorhandler(404)
def page_error_404(error):
    return "Такой страницы нет", 404


@app.errorhandler(500)
def server_error_500(error):
    return f"На сервере произошла ошибка {error}", 500


if __name__ == '__main__':
    app.run()
