# So in the last video, we went ahead and used POSTMAN to send a PUT request to our server

# We then verified that we were able to get the request body from the client
# Because we were able to return the same data back to them.

# In this video, we will start adding the code that allows clients to add a book.

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

# So let's talk about the different situations that can occur here.
# First is the client does send us a valid book object.

# In this scenario, we go ahead and add that book to the store.

# A valid book object for a PUT request would have all the information
# needed to replace the current book entity with a new one.

# This would mean this book object would have both a price and a name field.

# We will code this scenario up in this video.

# The other scenario is where the client does not send us a valid book object.
# This would mean that either the price or name field was missing.

# We will handle this scenario thoroughly in the next couple of videos.

# So what have now is the request_data sent by the client.

# Okay so now let's go ahead and update the book with the data sent by our client

# So what we are going to do is once we receive the request data from a client,
# we go ahead and grab the 'name' and 'price' from their request and create
# a new book from it.

# We create a new book here because we want to handle the case we only add the
# data that we need to our book store, and not unnecessary data that the client
# could possibly send us.

# We don't need to take the isbn from the client because we already have it From
# the resource URI that the client is posting from.

# Now we go ahead and create a loop here and check all the books that we currently
# have in our store.

# We will check if the book matches by checking the ISBN numbers of the books.

# If the ISBN numbers match, we can assume that key is unique and to update
# that book.

# And let's have our API return a 204: No-Content response, which is the standard
# to indicate that a Put operation successfully updated a resource.

# Let's go ahead and test this out using Postman.

#PUT /books/page/<int:page_number>
@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
	request_data = request.get_json()
	new_book = {
		'name': request_data['name'],
		'price': request_data['price'],
		'isbn': isbn
	}

	i = 0
	for book in books:
		currentIsbn = book["isbn"]
		if currentIsbn == isbn:
			books[i] = new_book
		i += 1
	response = Response("", status=204)
	return response

app.run(port=5000)

# So in this video, we finished implementing the PUT request and allow users to
# fully replace a book given a ISBN number

# In the next video, we will go ahead and handle what happens if the user enters
# an invalid input.
