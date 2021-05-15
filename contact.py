from flask import Flask,request, jsonify
from utilities.db import Database
import config
from contact_meta import getMetaData

app = Flask(__name__)


app.register_blueprint(getMetaData, url_prefix="/getMetaData")

# authentication decorator
@app.route('/addContact', methods=['POST'])
def addContact():
    # read and validate inputs
    response = 'Unable to add contact,Please check the details entered'
    db_conn = Database()
    cursor = db_conn.getcursor()
    firstName = request.args['FirstName']
    lastName = request.args['LastName']
    email = request.args['Email']
    phone = request.args['Phone']
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

# authentication decorator
@app.route('/updateContact', methods=['POST'])
def updateContact():
    if 'Email' not in request.args:
        response = "email is mandatory"
    else:
        email = request.args['Email']
        firstName = request.args['FirstName'] if 'FirstName' in request.args else None
        lastName = request.args['LastName'] if 'LastName' in request.args else None
        phone = request.args['Phone'] if 'Phone' in request.args else None
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

# authentication decorator
@app.route('/deleteContact', methods=['DELETE'])
def deleteContact():
    db_conn = Database()
    cursor = db_conn.getcursor()
    email = request.args['email']
    response = 'Unable to Delete Contact'
    sql_delete = "DELETE FROM ContactBook WHERE email = %s"
    cursor.execute(sql_delete,(email,))
    if cursor.rowcount > 0: response = "Contact Deleted"
    db_conn.closeConn()
    return jsonify(response)

# authentication decorator
@app.route('/search', methods=['GET'])
def searchContact():
    db_conn = Database()
    cursor = db_conn.getcursor()
    response = 'User not found'
    searchText = request.args['query']
    value = "'%" + str(searchText) +"%'"
    sql_search = "SELECT * FROM contactbook WHERE "
    if '@' in searchText:
        sql_search +=  "email LIKE " + value
    else:
        sql_search += "FirstName LIKE " + value + "OR LastName LIKE " + value
    cursor.execute(sql_search)
    if cursor.rowcount > 0:
        response = cursor.fetchall()
    db_conn.closeConn()
    return jsonify(response)

@app.route('/', methods=['GET'])
@app.route('/view', methods=['GET'])
def showContacts():
    db_conn = Database()
    cursor = db_conn.getcursor()
    response = "No Contacts found"
    sql = "SELECT * FROM ContactBook ORDER BY email LIMIT %s"
    cursor.execute(sql,(config.LIMT_ROWS,))
    if cursor.rowcount > 0: response = cursor.fetchall()
    db_conn.closeConn()
    return jsonify(response)
 

@app.before_request
def validateInputs():
    for val in request.values.values():
        if len(val) < 2 or val.count('@') > 1:
            return jsonify("Invalid input(s),please refer to the '\metadata' API")


if __name__ == "__main__":
    app.run(debug=True)