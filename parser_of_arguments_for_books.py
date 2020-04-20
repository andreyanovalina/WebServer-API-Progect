from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('description', required=True)
parser.add_argument('price', required=True, type=int)
parser.add_argument('count', required=True, type=int)
parser.add_argument('author_id', required=True, type=int)
