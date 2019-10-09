def validBookObject(bookObject):
    if("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
        return True
    else:
        return False

valid_object={
    'name':'F',
    'price':6.99,
    'isbn':123123123
}

missing_price={
    'name':'F',
    'isbn':12341234
}

missing_name={
    'price':4.99,
    'isbn':123456123
}
empty_object={}
