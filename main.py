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

    def createDatabase(self, databaseName):
        try:
            self.cursor.execute(f"CREATE database {databaseName}")
        except:
            print("Problem when creating your database. There might be a database with the same name exists");
            exit(-1)
