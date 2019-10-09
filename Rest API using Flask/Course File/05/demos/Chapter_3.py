# So in the last video, we went ahead and explained how our client will go ahead
# and PUT to our Rest Endpoint to update a book

# We then wrote some code to get the request body that was sent by our client.

# In this video, we went will go ahead and test that we do infact get the request
# body that was sent by our client.

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

# Okay so the first thing we need to do is create a sample body that our
# client may send to us.

# Remember that earlier I placed placeholder names for the books like "A", "B", etc. to
# show that pagination was indeed working.

# Now let's replace these placeholder book names with actual names.

# Let's go with this one.
# PUT /books/9780394800165
#	{
#		"name": "The Odyssey",
#		"price": 0.99
#	}

# This REST API endpoint will eventually swap out the book with the name "A"
# with the name "The Odyssey" once we are done with it.

# The second thing we need to do is go ahead and start this server so that
# It can listen to our post requests.

# I will go ahead and do this now.

# Now I will start Postman and send the PUT request
# The main thing to remember here is as the client, you are going to want to
# Content-Type Header to 'application/json'

# And when you are sending the body, you make sure the data type you choose is
# raw

# So let's go ahead and run this and we see that we get back the same request data
# the client sent

# So we know this works.

#PUT /books/page/<int:page_number>
@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
	return jsonify(request.get_json())

app.run(port=5000)

# So in this video, we went ahead and defined the URI that will be used to update an individual
# book in our book collection and showed how to pass in different parameters to the route
# method so it can handle the HTTP Put method

# In the next video, we will go ahead and implement this replace_book method.
