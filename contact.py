from flask import Flask,request, jsonify,g
from utilities.db import Database
import config
from contact_meta import getMetaData
from authentication import authenticator

app = Flask(__name__)


app.register_blueprint(getMetaData, url_prefix="/getMetaData")

@app.route('/addContact', methods=['POST'])
@authenticator.authenticate
def addContact():
    # read and validate inputs
    firstName = request.args['FirstName']
    lastName = request.args['LastName']
    email = request.args['Email']
    phone = request.args['Phone']
    if len(firstName) < 2 and len(lastName) < 2 and email.count('@') != 1 and len(phone) < 8:
        response = 'Invalid Parameters'
    else:
        response = 'Unable to add contact,Please check the details entered'
        db_conn = Database()
        cursor = db_conn.getcursor()
        values = (firstName,lastName,email,phone)
        sql_check_dup = "SELECT * FROM ContactBook WHERE email = %s"
        cursor.execute(sql_check_dup,(email,))
        if cursor.rowcount == 0:
            sql_insert = "INSERT INTO ContactBook (FirstName,LastName,Email,Phone) Values (%s,%s,%s,%s)"
            cursor.execute(sql_insert, values)
            if cursor.rowcount > 0: response = "Saved Contact Successfully"
        else:
            response = 'Contact with same Email address already exists'
        db_conn.closeConn()
    return jsonify(response)


@app.route('/updateContact', methods=['POST'])
@authenticator.authenticate
def updateContact():
    email = request.args['Email']
    firstName = request.args['FirstName'] if 'FirstName' in request.args and len(request.args['FirstName'])>=2  else None
    lastName = request.args['LastName'] if 'LastName' in request.args and len(request.args['LastName'])>=2 else None
    phone = request.args['Phone'] if 'Phone' in request.args and len(request.args['Phone'])>=8 else None
    if firstName is None and lastName is None and phone is None:
        response = "No parameter found to update"
    else:
        values = ()
        join_clause = ''
        response = 'No User found with given email id'
        db_conn = Database()
        cursor = db_conn.getcursor()
        sql = "SELECT * FROM ContactBook WHERE email = %s"
        cursor.execute(sql,(email,))
        if cursor.rowcount > 0:
            sql_update = " UPDATE ContactBook SET " 
            if firstName is not None:
                sql_update += " FirstName = %s "
                values += (firstName,)
                join_clause = ','
            if lastName is not None:
                sql_update += join_clause + " LastName = %s "
                values += (lastName,)
                join_clause = ','
            if phone is not None:
                sql_update += join_clause + " Phone = %s "
                values += (phone,)
            sql_update += "WHERE email = %s"
            values += (email,)
            cursor.execute(sql_update,values)
            if cursor.rowcount > 0: response = "Contact Updated Successfully"
            else: response = "Could not Update User details"
    return jsonify(response)

@app.route('/deleteContact', methods=['DELETE'])
@authenticator.authenticate
def deleteContact():
    email = request.args['Email'] if 'Email' in request.args else None
    db_conn = Database()
    cursor = db_conn.getcursor()
    sql = "SELECT * FROM ContactBook WHERE email = %s"
    cursor.execute(sql,(email,))
    if cursor.rowcount > 0:
        response = 'Unable to Delete Contact'
        sql_delete = "DELETE FROM ContactBook WHERE email = %s"
        cursor.execute(sql_delete,(email,))
        if cursor.rowcount > 0: response = "Contact Deleted"
    else:
        response = 'No User found with given email id'
    db_conn.closeConn()
    return jsonify(response)

@app.route('/search', methods=['GET'])
@authenticator.authenticate
def searchContact():
    searchText = request.args['query'] if 'query' in request.args else None
    if searchText is not None and (searchText.count('@') > 1 or len(searchText) < 2):
        response = 'Invalid Parameters'
    else:
        db_conn = Database()
        cursor = db_conn.getcursor()
        response = 'User not found'
        value = "'%" + str(searchText) +"%'"
        sql_search = "SELECT * FROM contactbook WHERE "
        if '@' in searchText:
            sql_search +=  "email LIKE " + value
        else:
            sql_search += "FirstName LIKE " + value + "OR LastName LIKE " + value
        cursor.execute(sql_search)
        if cursor.rowcount > 0: response = cursor.fetchall()
        db_conn.closeConn()
    return jsonify(response)



@app.route('/view', methods=['GET'])
@authenticator.authenticate
def showContacts(page=1):
    db_conn = Database()
    cursor = db_conn.getcursor()
    page  = int(request.args['page']) if 'page' in request.args and request.args['page'] else page
    if page <= 0: page=1
    response = "No Contacts found"
    # sql = "SELECT COUNT(*) AS rows FROM ContactBook"
    # cursor.execute(sql)
    # numOfRows = cursor.fetchone()['rows']
    # index = 0
    # if numOfRows < ((page-1) * config.LIMT_ROWS): index = 
    sql = "SELECT Concat(Concat(FirstName, ' '),LastName) as Name, Email,Phone FROM ContactBook ORDER BY email LIMIT %s,%s"
    cursor.execute(sql,((page-1) * config.LIMT_ROWS,config.LIMT_ROWS))
    if cursor.rowcount > 0: response = cursor.fetchall()
    db_conn.closeConn()
    return jsonify(response)
 

@app.before_request
def validateParams():
    params = request.values
    target = str(request.url_rule)
    print(target)
    if target =='/view':
        if len(params) > 1:
            return jsonify("Missing or Invalid Parameters,please refer to the '\metadata' API")
    elif target =='/addContact':
        reqParams = ['FirstName','LastName','Email','Phone']
        if len(params) > len(reqParams): return jsonify("Missing or Invalid Parameters,please refer to the '\metadata' API")
        for param in reqParams:
            if param not in params:
                return jsonify("Missing or Invalid Parameters,please refer to the '\metadata' API")  
    elif target =='/updateContact':
        reqParams = ['FirstName','LastName','Phone']
        if 'Email' not in params or len(params) < 2:
            return jsonify("Missing or Invalid Parameters,please refer to the '\metadata' API")
    elif target =='/deleteContact':
        if 'Email' not in params or len(params) > 1:
            return jsonify("Missing or Invalid Parameters,please refer to the '\metadata' API")
    elif target =='/search':
        if 'query' not in params or len(params) > 1:
            return jsonify("Missing or Invalid Parameters,please refer to the '\metadata' API")
            


if __name__ == "__main__":
    app.run(debug=True)