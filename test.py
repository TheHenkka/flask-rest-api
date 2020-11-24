import requests

######################################
#   API calls. Prints out responses. #
######################################

def getAPI(id):
    response = requests.get('http://127.0.0.1:5000/cart/'+str(id) )
    return(response.json())
    #return(response.headers)

print(getAPI(2))


def putAPI(data):
    response = requests.put('http://127.0.0.1:5000/cart', data )
    return(response.json())
    #return(response.headers)

print(putAPI( {'items': '[1,3,4,4,4]', 'country': 'Estonia'}))
#putAPI( {'items': '[1,3,4,4,4]', 'country': 'Estonia'})
#putAPI( {'items': '[0,1]', 'country': 'Estonia'})
#putAPI( {'items': '[1,3,4,4,4,1,2,3,4]', 'country': 'Finland'})


def updateAPI(id, data):
    response = requests.patch('http://127.0.0.1:5000/cart/'+ str(id), data )
    return(response)
    #return(response.headers)

print(updateAPI(1, {'items': '[1,3,4,4,4]'}))


def deleteAPI(id):
    response = requests.delete('http://127.0.0.1:5000/cart/' + str(id) )
    return(response)
    #return(response.headers)

print(deleteAPI(13))
print(getAPI(4))


#######################################################
#   Tests. Read database before running or check IDs  #
#######################################################

def test_get1():
    existingCartID =1
    assert getAPI(existingCartID) == [{'cart_id': 1, 'country': 'Finland', 'items': [{'id': 1, 'name': 'item1', 'price': 9.99}, 
                            {'id': 3, 'name': 'item3', 'price': 14}, {'id': 4, 'name': 'item4', 'price': 49}, 
                            {'id': 4, 'name': 'item4', 'price': 49}, 
                            {'id': 4, 'name': 'item4', 'price': 49}]}]

def test_delete1():
    existingCartIDtoDelete =  4
    assert deleteAPI(existingCartIDtoDelete).status_code ==  204

def test_get2():
    deletedCartID =4
    assert getAPI(deletedCartID) == {'message': "Cart {} doesn't exist".format(deletedCartID)}

def test_get3():
    existingCartID =1
    assert getAPI(existingCartID) != {'message': "Cart {} doesn't exist".format(existingCartID)}

def test_put1():
    newCart =  {'items': '[1,4,4,2,2,2]', 'country': 'Russia'}
    assert putAPI(newCart) == {'id': 7}

def test_put2():
    newCart =  {'country': 'Russia'}
    assert putAPI(newCart) == {'message': {'items': 'Cannot save/update empty cart'}}

def test_put3():
    newCart =  {'items': '[1,4,4,2,2,2]'}
    assert putAPI(newCart) == {'message': {'country': 'Country is required for VAT purposes'}}

def test_delete2():
    deletedCartIDtoDelete =  4
    assert deleteAPI(deletedCartIDtoDelete).status_code ==  304

def test_update1():
    deletedCartIDtoUpdate =  4
    data=  {'items': '[1,3,4,4,4]'}
    assert updateAPI(deletedCartIDtoUpdate, data).status_code ==  404

def test_update2():
    cartIDtoUpdate =  3
    data=  {'items': '[1,3,4,4,4]'}
    assert updateAPI(cartIDtoUpdate, data).status_code ==  200

def test_update3():
    cartIDtoUpdate =  1
    data=  []
    assert updateAPI(cartIDtoUpdate, data).json() ==  {'message': {'items': 'Cannot save/update empty cart'}}

def test_update4():
    cartIDtoUpdate =  1
    data=  []
    assert updateAPI(cartIDtoUpdate, data).status_code ==  400
