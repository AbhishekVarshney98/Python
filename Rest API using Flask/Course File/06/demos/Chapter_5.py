# Okay so in the last video we went ahead and finished up the DELETE route.

# In this video we will try various test inputs and to make sure things work as expected.

# We will also discuss what happens if we try to delete the same resource twice
# and how this relates to method idempotence

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

def valid_patch_request_data(request_data):
	if("name" in request_data or "price" in request_data):
		return True;
	else:
		return False;

@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
	request_data = request.get_json()
	if(not valid_patch_request_data(request_data)):
		invalidBookObjectErrorMsg = {
			"error": "Invalid book object passed in request",
			"helpString": "Data should be passed in similar to this {'name': 'bookname', 'price': 7.99 }"
		}
		response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
		return response
	updated_book = {}
	if("price" in request_data):
		updated_book["price"] = request_data['price']
	if("name" in request_data):
		updated_book["name"] = request_data['name']
	for book in books:
		if book["isbn"] == isbn:
			book.update(updated_book)
	response = Response("", status=204)
	response.headers['Location'] = "/books/" + str(isbn)
	return response

# So let's go ahead first start the server up and do a GET request
# and see all the books we have.

# We see that the first book is named 'A', so let's go ahead and
# grab this books ISBN.

# Okay now that we have it, let's send a DELETE request to /books/isbn
# and pass this ISBN in

# So we are getting a 204 status code so that should mean this book was deleted.
# Let's now do a Get Request and see that this is indeed the case.

# Okay so we can see that this book is indeed deleted now.

# So now what happens if we run the Delete method again on that same ISBN?

# Take a second to pause the video and think about this.

# Okay so if we do a DELETE request, you would expect since that ISBN doesn't exist
# that translates to this file not existing in HTTP so we should expect to get back a 404.

# So let's run this again. We do see that we get a 404.

# But if you notice, we ran the same DELETE method twice but got different status codes.

# There is requirement when building a REST API that the DELETE protocol should be
# idempotent.

# What idempotence means is that if you do something to a system multiple times, the system
# remains the same.

# An example of this would be doing a GET request over and over again. Doing the same request
# over and over doesn't change the state of the server.

# The end result of this is you get back the same response over and over.

# This DELETE method needs to be indempotent as well, but as you see the first time
# you run this call you get a 204 response and then the second time you get a 404.

# So how can this be idempotent?

# So the thing to realize is that the server's state (whether the file exists or not) is
# different than the status codes we receive, and idempotence refers to the server state.

# So after that first DELETE, the book is deleted from the server.
# And regardless of how many times you run this this DELETE, the book will still be
# removed from the server.

# The status codes we receive back from the SERVER could also be indempotent (meaning)
# you receive the same status code after each request, but this is NOT necessary
# for the DELETE protocol.

# Since the server's state is the same, the method we developed is indeed indempotent.

# I wanted to clear this up in this video, because it's a fairly tricky concept that
# a lot of people have trouble with and that I haven't seen covered in any other tutorials/
# videos.

#DELETE /books/page/<int:page_number>
@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
	i = 0;
	for book in books:
		if book["isbn"] == isbn:
			books.pop(i)
			response = Response("", status=204)
			return response
		i += 1
	invalidBookObjectErrorMsg = {
		"error": "Book with ISBN number provided not found, so unable to delete.",
	}
	response = Response(json.dumps(invalidBookObjectErrorMsg), status=404, mimetype='application/json')
	return response
app.run(port=5000)

# Okay so in this video we ran some test cases and discussed what happens if we
# try to delete the same resource twice.

# We showed that our delete request was idempotent, which is a requirement for building
# a restful API. 
