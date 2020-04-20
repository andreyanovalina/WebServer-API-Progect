from requests import get, post, delete

# print(get('http://localhost:5000/api/books').json())
# print(get('http://localhost:5000/api/books/1').json())
#
# print(get('http://localhost:5000/api/books/999').json())
# ----------------------------------------------------------------------------------------------------------------------
# print(post('http://localhost:5000/api/books',
#            json={'title': 'Евгений Онегин',
#                  'description': '.',
#                  'price': 130,
#                  'count': 100,
#                  'author_id': 5}).json())
#
# print(post('http://localhost:5000/api/books').json())
# print(post('http://localhost:5000/api/books',
#            json={'title': 'МЫ'}).json())
# ----------------------------------------------------------------------------------------------------------------------
# print(delete('http://localhost:5000/api/books/27').json())
#
# print(delete('http://localhost:5000/api/books/999').json())
# ======================================================================================================================
# print(get('http://localhost:5000/api/authors').json())
# print(get('http://localhost:5000/api/authors/1').json())
#
# print(get('http://localhost:5000/api/authors/999').json())
# ----------------------------------------------------------------------------------------------------------------------
# print(post('http://localhost:5000/api/authors',
#            json={'name': 'Фёдор Достоевский'}).json())
#
# print(post('http://localhost:5000/api/authors').json())
# ----------------------------------------------------------------------------------------------------------------------
# print(delete('http://localhost:5000/api/authors/8').json())
#
# print(delete('http://localhost:5000/api/authors/999').json())