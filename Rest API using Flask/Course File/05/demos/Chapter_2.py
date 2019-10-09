# So in the last video video, we went ahead and defined the URI that will be used to allow
# clients to update a book and showed how to pass in different parameters to the route
# method so it can handle the HTTP verb PUT

# In this video, we went ahead and explained how our client will go ahead
# and PUT to our Rest Endpoint to create a book

# We will then write some code to get the request body that was sent by our client.

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

# So the first thing we need to is define how the clients of our API will actually
# update new books to our store

# So what we intend to happen is the following
# We want them to send them a PUT request to our /books/isbn endpoint

# In that PUT, they need to send us the ALL of the details of the book they want us to
# add in the response body as an object.

# We will then update the book object with the data that they send us.

# Their request will look like the following

# PUT /books/9785040381791
# {
#	'name': 'The Odyssey',
#	'price': 0.99
# }

# Note here that the client sends us all the data needed for that resource

# This is the definition of what a PUT request is in REST.

# When using PUT, it is assumed that you are sending the complete entity,
# and that complete entity replaces any existing entity at that URI.

# To make a a partial update, (let's say if we only wanted to update the book
# price and not its' name we can use the PATCH, which will be discussed in
# a later video.

# So one thing to keep in mind here is they will be sending this book data back
# to us from their perspective as a JSON object.

# So the first thing we need to do is be able to get the json request body
# that our client will send us.

# We can do this by using the request.get_json() methods

# Let's test that this works by returning back the data our client returns us
# (to verify that we did indeed get it).

#PUT /books/page/<int:page_number>
@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
	return jsonify(request.get_json())

app.run(port=5000)

# So in this video, we went ahead and defined the URI that will be used to update an individual
# book in our book collection and showed how to pass in different parameters to the route
# method so it can handle the HTTP Put method

# In the next video, we will go ahead and implement this replace_book method.
