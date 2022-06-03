import mysql.connector
class MySQLAPI:
    def __init__(self, username, userPassword):
        self.db = mysql.connector.connect(
            host="localhost",
            user=username,
            password=userPassword
        )
        self.cursor = self.db.cursor;
    
    
    ########## Database Stuffs ##########
    def useDatabase(self, databaseName):
        try:
            self.cursor.execute(f"USE {databaseName}");
        except:
            print("Can't find the Database Name");
            exit(-1)
    
