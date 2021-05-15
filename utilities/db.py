import mysql.connector
import config

class Database:
    def __init__(self):
        self.db = mysql.connector.connect(
            host = config.DB_HOST,
            user = config.DB_ROOT_USER,
            passwd = config.DB_ROOT_PW,
            database = "contacts"
        )
        self.db.autocommit = True
        self.cursor = ""
    
    def getcursor(self, dictmode=True):
        if dictmode:
            self.cursor = self.db.cursor(buffered=True, dictionary=True)
        else:
            self.cursor = self.db.cursor(buffered=True)
        return self.cursor


    def closeConn(self):
        self.cursor.close()
        self.db.close()
