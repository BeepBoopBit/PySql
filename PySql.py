import mysql.connector
class PySql:
    def __init__(self, username, userPassword):
        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user=username,
                password=userPassword
            )
            self.cursor = self.db.cursor();
        except:
            print("Invalid Credentials")
            exit(-1)
    
    
    ########## Database Stuffs ##########
    def useDatabase(self, databaseName):
        self.__safeExecution(f"USE {databaseName}", "Database Using")

    def createDatabase(self, databaseName):
        self.__safeExecution(f"CREATE DATABASE{databaseName}", "Database Creation")

        
    def __safeExecution(self, command, typeOfCommand="Unknown"):
        try:
            self.cursor.execute(command)
        except:
            print(f"Problem: {typeOfCommand}");
            exit(-1)