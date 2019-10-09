# So in the last video, we finished implementing the PUT request and allow users to
# fully replace a book given a ISBN number. We also handled what happens if the user enters
# an invalid input.

# In this video, we will go ahead and handle the case where a client only
# wants to update a certain attribute and not have them send all book properties back to us.

from flask import Flask, jsonify, request, Response
import json
app = Flask(__name__)

books = [
	{
		'name': 'A',
		'price': 7.99,
		'isbn': 9780394800165
	},
	{
		'name': 'B',
		'price': 6.99,
		'isbn': 9792371000193
	},
	{
		'name': 'C',
		'price': 7.99,
		'isbn': 9800394800165
	},
	{
		'name': 'D',
		'price': 6.99,
		'isbn': 9812371000193
	},
	{
		'name': 'E',
		'price': 7.99,
		'isbn': 9820394800165
	},
	{
		'name': 'F',
		'price': 6.99,
		'isbn': 9832371000193
	},
	{
		'name': 'G',
		'price': 7.99,
		'isbn': 9840394800165
	},
	{
		'name': 'H',
		'price': 6.99,
		'isbn': 9852371000193
	},
	{
		'name': 'I',
		'price': 7.99,
		'isbn': 9860394800165
	},
	{
		'name': 'K',
		'price': 6.99,
		'isbn': 9872371000193
	},
	{
		'name': 'L',
		'price': 7.99,
		'isbn': 9880394800165
	},
	{
		'name': 'M',
		'price': 6.99,
		'isbn': 9892371000193
	},
	{
		'name': 'N',
		'price': 7.99,
		'isbn': 9900394800165
	},
	{
		'name': 'O',
		'price': 6.99,
		'isbn': 9912371000193
	},
	{
		'name': 'P',
		'price': 7.99,
		'isbn': 9920394800165
	},
	{
		'name': 'Q',
		'price': 6.99,
		'isbn': 9932371000193
	},
	{
		'name': 'R',
		'price': 7.99,
		'isbn': 9940394800165
	},
	{
		'name': 'S',
		'price': 6.99,
		'isbn': 9952371000193
	}
]

DEFAULT_PAGE_LIMIT = 3;

#GET /books
@app.route('/books')
def get_books():
  	return jsonify({'books': books})

@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
	return_value = {}
	for book in books:
	  if book["isbn"] == isbn:
	  	return_value = {
			'name': book["name"],
			'price': book["price"]
		}
	return jsonify(return_value)

#GET /books/page/<int:page_number>
@app.route('/books/page/<int:page_number>')
def get_paginated_books(page_number):
	print(type(request.args.get('limit')))
	LIMIT = request.args.get('limit', DEFAULT_PAGE_LIMIT, int)
	return jsonify({'books': books[page_number*LIMIT-LIMIT:page_number*LIMIT]})


def validBookObject(bookObject):
	if ("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
		return True
	else:
		return False

#POST /books
@app.route('/books', methods=['POST'])
def add_book():
	request_data = request.get_json()
	if(validBookObject(request_data)):
		new_book = {
			"name": request_data['name'],
			"price": request_data['price'],
			"isbn": request_data['isbn']
		}
		books.insert(0, new_book)
		response = Response("", status=201, mimetype='application/json')
		response.headers['Location'] = "/books/" + str(new_book['isbn'])
		return response
	else:
		invalidBookObjectErrorMsg = {
			"error": "Invalid book object passed in request",
			"helpString": "Data passed in similar to this {'name': 'bookname', 'price': 7.99, 'isbn': 9780394800165 }"
		}
		response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
		return response;


def valid_put_request_data(request_data):
	if("name" in request_data and "price" in request_data):
		return True;
	else:
		return False;

#PUT /books/page/<int:page_number>
@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
	request_data = request.get_json()
	if(not valid_put_request_data(request_data)):
		invalidBookObjectErrorMsg = {
			"error": "Invalid book object passed in request",
			"helpString": "Data should be passed in similar to this {'name': 'bookname', 'price': 7.99 }"
		}
		response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
		return response

	new_book = {
		'name': request_data['name'],
		'price': request_data['price'],
		'isbn': isbn
	}
	i = 0;
	for book in books:
		currentIsbn = book["isbn"]
		if currentIsbn == isbn:
			books[i] = new_book
		i += 1
	response = Response("", status=204)
	return response

app.run(port=5000)

# So in the last couple of videos, we gave our clients the ability to, given an
# isbn number for a book, to be able to replace that entire book entry with a
# new one.

# So far we only had three properties for a given book: it's isbn number,
# it's price and the book's name.

# Using a PUT request, a client would be required to send us all three of these pieces
# of information, even if they only wanted to update one property.

# So let's say a client wanted to only update only the name of a book, let's say from 'A'
# to 'Harry Potter and the Chamber Of Secrets'

# Right now, they would have to also send us the book price in the request body, even if
# The price hasn't changed.

# PUT /books/9780394800165
# {
# 	'name': 'Harry Potter and the Chamber Of Secrets',
# 	'price': 7.99,
# }

# This is not so bad, but it is inconvient for the client to have to send in data
# that they know isn't going to change.

# But they only have to send one extra piece of data so it's maneagble for them.

# In an enterprise environment, however, a book would most likely have a lot more than
# two properties.

# It could in fact have anywhere from 20-40 different properties.

# Things like the whether the book is available as an ebook, hard cover or soft cover.
# How many units of the book are in stock.
# How many stars does this book have out of 5 from customer views, etc.

# In this scenario, it is unreasonable for us to require a client to send us an entire
# book's information just to update one or a few properties.

# You may be thinking to yourself, there must be a better way.

# And there is.

# So the protocol we used, PUT requires in REST for a client to send us an entire entity
# so we can update it.

# There is another HTTP protocol, called PATCH, which allows a client to only send us
# the piece to update and then we just update that portion.

# This protocol is called PATCH and we will discuss it in-depth in the next couple of videos.

# For now, let's just define the route to handle this and for now just place a pass
# within in.

@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
	pass

# So in this video, we defined the use case for why we would need a PATCH request.

# This would be when  a client only to update a certain attribute and not have them
# send all book properties back to us.

# In the next video, we will go ahead and start coding this route up.
