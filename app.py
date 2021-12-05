from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


def database_connection():
    connection = sqlite3.connect("digikala.sqlite")
    connection.row_factory = sqlite3.Row
    return connection


def products():
    return database_connection().execute("SELECT * FROM products").fetchall()


@app.route('/')
def main():
    return render_template('index.html', products=products())


if __name__ == '__main__':
    app.run()
