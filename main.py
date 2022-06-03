import mysql.connector
class MySQLAPI:
    def __init__(self, username, userPassword):
        self.db = mysql.connector.connect(
            host="localhost",
            user=username,
            password=userPassword
        )
        self.cursor = self.db.cursor;
    