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
        self.currentDatabase = "";
    
    ########## Database Stuffs ##########
    def useDatabase(self, databaseName):
        self.__safeExecution(f"USE {databaseName};", "Using Database")
        self.currentDatabase = databaseName;
        
    def createDatabase(self, databaseName):
        self.__safeExecution(f"CREATE DATABASE{databaseName};", "Database Creation")

    def deleteDatabase(self, databaseName):
        self.__safeExecution(f"DROP DATABASE {databaseName};", "Database Deletion")
    
    def getDatabaseList(self):
        self.__safeExecution(f"SHOW DATABASES;", "Getting Database List")
        return self.cursor.fetchall();
        
    ########## Other Methods ##########
    def getCurrentUser(self):
        """Return a List of Tuples"""
        self.__safeExecution(f"SELECT CURRENT_USER();", "Getting Current User");
        return self.cursor.fetchall();
    
    def getCurrentDatabaseName(self):
        return self.currentDatabase;
    
    ########## Private Methods ##########
    
    def __safeExecution(self, command, typeOfCommand="Unknown"):
        try:
            self.cursor.execute(command)
        except:
            print(f"Problem: {typeOfCommand}");
            exit(-1)
            