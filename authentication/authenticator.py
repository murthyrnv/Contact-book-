from flask import request,jsonify
from functools import wraps
import base64
from utilities.db import Database


def check(encodedCred):
    credentials = base64.b64decode(encodedCred).decode('UTF-8').split(':')
    db_conn = Database()
    cursor = db_conn.getcursor()
    sql = "SELECT password, role FROM users WHERE email = %s"
    cursor.execute(sql,(credentials[0],))
    if cursor.rowcount > 0:
        user = cursor.fetchone()
        if user['password'] == credentials[1]:
            if request.url_rule in ['/deleteContact','/updateContact'] and user['role'] == 'user':
                return 'Not Authorized to perform this operation'
            else:
                return 'Authentication Successfull'
    return 'Authentication Failed'

def authenticate(f):
    @wraps(f)
    def verify(*args, **kwargs):
        encodedCredentials = request.headers.get('Authorization').split()[1]
        authStatus = check(encodedCredentials)
        if authStatus == 'Authentication Successfull':
            return f(*args, **kwargs)
        else:
            return jsonify(authStatus),401
        return f(*args, **kwargs)
    return verify 