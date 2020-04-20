from parser_of_arguments_for_authors import parser
from flask import jsonify
from flask_restful import abort, Resource
from data import db_session
from data.author import Author


def abort_if_author_not_found(author_id):
    session = db_session.create_session()
    author = session.query(Author).get(author_id)
    if not author:
        abort(404, message=f"Author {author_id} not found")


class AuthorResource(Resource):
    def get(self, author_id):
        abort_if_author_not_found(author_id)
        session = db_session.create_session()
        author = session.query(Author).get(author_id)
        return jsonify({'author': author.to_dict(only=['name'])})

    def delete(self, author_id):
        abort_if_author_not_found(author_id)
        session = db_session.create_session()
        author = session.query(Author).get(author_id)
        session.delete(author)
        session.commit()
        return jsonify({'success': 'OK'})


class AuthorListResource(Resource):
    def get(self):
        session = db_session.create_session()
        author = session.query(Author).all()
        return jsonify({'author': [item.to_dict(only=['name']) for item in author]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        author = Author(
            name=args['name']
        )
        session.add(author)
        session.commit()
        return jsonify({'success': 'OK'})