# So in the last video, we finished up code to allow a client to also update
# a book with a price as well.

# In this video, we will cover what happens if our client sends invalid requests.

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

# So what happens if our client sends us an empty body as a request like this

# PATCH /books/9780394800165
# {}

# So here, the client sending us an empty object.

# Here we could assume that this means that the client wants to update no fields

# Some REST APis would allow a client to send in an empty object and return a 204,
# but for here we will actually go ahead and return a 400 error.

# The reason being is that for our API, we don't want our client to send in a response
# like this since it doesn't really make sense for our application.

# Let's see what happens when our client sends an empty object.

# We get a 204 - NO Content response which indicates a resource has been
# updated.

# As we can see, this is not working as expected.

# Lets say, also, that our client also sends us an object with invalid keys such as this.

# {
# 	"invalidKey1": "invalid value 1",
# 	"invalidKey2": "invalud value 2"
# }

# What should happen here.

# So right now let's try this out in POSTMAN and see what happens.

# We get a 204 - NO Content response which indicates a resource has been
# updated, clearly is incorrect since no values were updated.

# Using the location header to see the updated book object,
# we don't see any updated values.

# What we can do here is add a check so that if we don't receive either a
# price or name key from the client, to throw a 400 bad request.

# So similar to the code we wrote before, let's add a invalid patch request
# method

# This time if either the name or price is received, then we know we have a valid
# patch request. If not, then we must have an invalid patch request.

# Now we will check, if we have an invalid patch request, to automatically throw
# a 400 error.

# We will also throw in a helpful error message here for our clients.

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
app.run(port=5000)

# That should be it.

# Now let's go ahead and test this out by sending the following over.

# PATCH /books/9780394800165
# {}

# PATCH /books/9780394800165
# {
# 	"invalidKey1": "invalid value 1"
# }

# PATCH /books/9780394800165
# {
# 	"invalidKey1": "invalid value 1",
# 	"invalidKey2": "invalud value 2"
# }

# As we can see, this all works correctly.

# So in this video, we went ahead start coding this PATCH route up and if our client passes
# us an object with a name property, we will be able to properly update it.

# In the next video, we will handle what happens if our client sends us an invalid request.
