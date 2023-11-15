from flask import Flask, request, render_template, redirect, url_for, jsonify, make_response, abort
import json

from models import books
from forms import BookForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "asdjflaksdjfl"
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/books/", methods=["GET", "POST"])
def books_all():
    form = BookForm()
    error = ""
    if request.method == "POST":
        if form.validate_on_submit():
            books.create(form.data)
            books.save_all()
        return redirect(url_for("books_all"))

    return render_template("books.html", form=form, books=books.all(), error=error)


@app.route("/books/<int:book_id>/", methods=["GET", "POST"])
def book_details(book_id):
    book = books.get(book_id - 1)
    form = BookForm(data=book)

    if request.method == "POST":
        if form.validate_on_submit():
            books.update(book_id - 1, form.data)
        return redirect(url_for("books_all"))
    return render_template("book_details.html", form=form, book_id=book_id)


@app.route("/api/v1/books/", methods=["GET"])
def api_v1_books():
    return jsonify(books.all())


@app.route("/api/v1/books/<int:book_id>/", methods=["GET"])
def api_v1_book(book_id):
    book = books.get(book_id)
    if book is None:
        abort(404)
    return jsonify(books.get(book_id))


@app.route("/api/v1/books/", methods=["POST"])
def api_v1_book_new():
    books.add(json.loads(request.data))
    return "Success"


@app.route("/api/v1/books/<int:book_id>/", methods=["DELETE"])
def api_v1_book_delete(book_id):
    result = books.delete(book_id)
    if not result:
        abort(404)
    return jsonify({'result': result})


@app.route("/api/v1/books/<int:book_id>/", methods=["PUT"])
def update_todo(book_id):
    book = books.get(book_id)
    if not book:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'title' in data and not isinstance(data.get('title'), str),
        'author' in data and not isinstance(data.get('author'), str),
        'genre' in data and not isinstance(data.get('genre'), str),
        'publisher' in data and not isinstance(data.get('publisher'), str),
        'publication_year' in data and not isinstance(data.get('publication_year'), str)
    ]):
        abort(400)
    book = {
        'title': data.get('title', book['title']),
        'author': data.get('author', book['author']),
        'genre': data.get('genre', book['genre']),
        'publisher': data.get('publisher', book['publisher']),
        'publication_year': data.get('publication_year', book['publication_year'])
    }
    books.update(book_id, book)
    return jsonify({'book': book})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)


if __name__ == "__main__":
    app.run(debug=True)