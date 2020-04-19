from parser_of_arguments import parser
from flask import jsonify
from flask_restful import abort, Resource
from data import db_session
from data.books import Books


def abort_if_books_not_found(books_id):
    session = db_session.create_session()
    books = session.query(Books).get(books_id)
    if not books:
        abort(404, message=f"Books {books_id} not found")


class BooksResource(Resource):
    def get(self, books_id):
        abort_if_books_not_found(books_id)
        session = db_session.create_session()
        books = session.query(Books).get(books_id)
        return jsonify({'books': books.to_dict()})

    def delete(self, books_id):
        abort_if_books_not_found(books_id)
        session = db_session.create_session()
        books = session.query(Books).get(books_id)
        session.delete(books)
        session.commit()
        return jsonify({'success': 'OK'})


class BooksListResource(Resource):
    def get(self):
        session = db_session.create_session()
        books = session.query(Books).all()
        return jsonify({'books': [item.to_dict() for item in books]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        books = Books(
            title=args['title'],
            description=args['description'],
            price=args['price'],
            count=args['count'],
            author_id=args['author_id']
        )
        session.add(books)
        session.commit()
        return jsonify({'success': 'OK'})