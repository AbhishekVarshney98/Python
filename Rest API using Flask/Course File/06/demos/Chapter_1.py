# In the last module, we went ahead and finished implementing the PUT and PATCH
# http methods, which allowed clients to update books that were already created
# in the store.

# In this video, we will go ahead and implement the DELETE HTTP method, which
# will allow clients to actually be able to delete a book.

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

# So the first thing we will do is add a new route
# This route will point to the same endpoint as our /books/isbn route that allowed
# users to get a single book from our store

# By sending a DELETE request to this route, this will allow users to delete the current book from
# this collection of books.

# This is a very normal idea in rest.

# When you do a get request to an individual sub-resource, you get back that sub-resource
# When you do a put delete request to an individual sub-resource resources, you delete that
# sub-resource

# So how we go about doing this is by defining the route the same as before
# But now we add a methods= part to it
# By default, without adding a method, the route defaults to HTTP Get requests

# By adding this methods=, This tells Flask that whenever the route /books/isbn_number is reached
# and the HTTP method is DELETE, then call the delete_book method.

# We will put in a pass for this method for now and define it later.

#DELETE /books/page/<int:page_number>
@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
	pass

app.run(port=5000)


# So in this video, we went ahead start coding this DELETE route up

# In the next video, we will handle what happens if our client sends us an invalid request.
