from flask import Blueprint, jsonify
getMetaData = Blueprint("getMetaData", __name__)

@getMetaData.route('/', methods=['GET'])
def getMeta():
    endpoints = {
        'view' : {
            'params': [],
            'method': 'GET'
        },
        'addContact' :{
            'params': ['FirstName','LastName','Email','Phone'],
            'method': 'GET' 
        },
        'deleteContact' :{
            'params': ['Email'],
            'method': 'DELETE' 
        },
        'updateContact' :{
            'params': ['FirstName','LastName','Email','Phone'],
            'Note' : 'Email cannot be modified.Atleast one of the above params (along with Email) needed',
            'method': 'POST' 
        },
        'search' :{
            'params': ['query'],
            'method': 'GET' 
        }
    }
    return jsonify(endpoints)
