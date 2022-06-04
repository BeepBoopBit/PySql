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
        return self.cursor.fetchall()
    
    ########## Table Stuff ##########
    def createTable(self, tableName, command):
        tempStr = ""
        if(isinstance(command, set) or isinstance(command, list)):
            for data in command:
                tempStr += data + ',';
            tempStr = tempStr[:-1];
        else:
            tempStr = command;
        if self.currentDatabase == "":
            print("No Database Currently in-use");
            exit(-1);
        else:
            self.__safeExecution(f"CREATE TABLE {tableName} ({tempStr});", "Creating Table")
    
    def getTables(self):
        self.__safeExecution("SHOW TABLES;", "Getting Tables")
        return self.cursor.fetchall()
    
    def deleteTable(self, tableName):
        self.__safeExecution(f"DROP TABLE {tableName}", "Deleting Table")
    
    def addTableColumn(self, tableName, command):
        tempStr = ""
        if(isinstance(command, set) or isinstance(command, list)):
            for data in command:
                tempStr += data + ',';
            tempStr = tempStr[:-1];
        else:
            tempStr = command;
        if self.currentDatabase == "":
            print("No Database Currently in-use");
            exit(-1);
        else:
            self.__safeExecution(f"ALTER TABLE {tableName} ADD {command};", "Adding Table Column")
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
            