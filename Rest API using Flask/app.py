from flask import Flask, jsonify, request, Response
import jwt
import datetime


app=Flask(__name__)
print(__name__+"HAHAHAH")

books=[
    {
        'name':'What the dont teach you in Harvard Business School',
        'price':50,
        'isbn':12345432
    },

    {
        'name':'Castle of glass',
        'price':79,
        'isbn':12324355
    }
] 

DEFAULT_PAGE_LIMIT = 3
app.config['SECRET_KEY'] = 'meow'

@app.route('/login')
def get_token():
    try:
        expiration_date=datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
        token=jwt.encode({'exp':expiration_date}, app.config['SECRET_KEY'], algorithm='HS256')
        return token
    except Exception as e:
        print(e)


#add the books
def validBookObject(bookObject):
    if("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
        return True
    else:
        return False

@app.route('/books',methods=['POST'])
def add_book():
    request_data=request.get_json()
    if(validBookObject(request_data)):
        newbook={
            "name":request_data['name'],
            "price":request_data['price'],
            "isbn":request_data['isbn']
        }
        books.insert(0, newbook)
        response=Response("you have inserted a value", 201, mimetype='application/json')
        #print(books)
        return response
    else:
        return "False"



#request for root 
@app.route('/')
def hello_work():
    return "Hello World"

#getall the books
@app.route('/books')
def get_books():
    token=request.args.get('token')
    print(token,"_______________________________________________")
    try:
        jwt.decode(token, app.config['SECRET_KEY'])
    except:
        return jsonify({'error':'need a valid token to view this page'}), 401
    return jsonify({'books': books})                                        

#get books from ISBN number
@app.route('/books/<int:isbn>')
def get_book_isbn(isbn):
    return_value={}
    for book in books:
        if book['isbn']==isbn:
            return_value={
                'name':book['name'],
                'price':book['price']
            }
    
    return jsonify(return_value)

#PUT 
@app.route('/books/<int:isbn>',methods=['PUT'])
def replace_book(isbn):
    try:
        request_data=request.get_json()
        new_book={
            'name':request_data['name'],
            'price':request_data['price'],
            'isbn': isbn
        }

        i=0
        for book in books:
            currentIsbn=book["isbn"]
            if currentIsbn == isbn:
                books[i] = new_book
            i+=1
        response=Response("Sucessfully updated",status=204)
        print(books)
        
        return response

    except Exception as e:
        print(e)

@app.route('/books/<int:isbn>',methods=['PATCH'])
def update_book(isbn):
    request_data=request.get_json()
    updated_book={}
    if("name" in request_data):
        updated_book["name"]=request_data['name']
    for book in books:
        if book["isbn"]==isbn:
            book.update(updated_book)
    response=Response("",status=204)
    response.headers['Location']="/books/"+str(isbn)
    return response

@app.route('/books/<int:isbn>',methods=['DELETE'])
def delete_book(isbn):
    try:
        i=0
        for book in books:
            if book["isbn"]==isbn:
                books.pop(i)
            i+=1
        return "book is deleted"
    except Exception as e:
        print(e)


app.run(port=5000)