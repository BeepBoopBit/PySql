from lib2to3.pytree import convert
import mysql.connector
from API.GoogleSheet import *
from os.path import exists


class PySql:
    def __init__(self, username, userPassword):
        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user=username,
                password=userPassword
            )
            self.cursor = self.db.cursor()
        except:
            print("Invalid Credentials")
            exit(-1)
        self.currentDatabase = "";
        #self.gSheetAPI = GoogleSheetAPI();
    
    ########## Database Stuffs ##########
    def useDatabase(self, databaseName):
        self.__safeExecution(f"USE {databaseName};", "Using Database")
        self.currentDatabase = databaseName

    def createDatabase(self, databaseName):
        self.__safeExecution(
            f"CREATE DATABASE {databaseName};", "Database Creation")

    def deleteDatabase(self, databaseName):
        self.__safeExecution(
            f"DROP DATABASE {databaseName};", "Database Deletion")

    def getDatabaseList(self):
        self.__safeExecution(f"SHOW DATABASES;", "Getting Database List")
        return self.cursor.fetchall()

    ########## Table Stuff ##########

    # Command parameter can accept a set of list in a form of
    #   - {"columnName Type CONSTRAINTS","CONSTRAINTS"}

    def createTable(self, tableName, command):
        tempStr = ""
        if(isinstance(command, set) or isinstance(command, list)):
            for data in command:
                tempStr += data + ','
            tempStr = tempStr[:-1]
        else:
            tempStr = command
        if self.currentDatabase == "":
            print("No Database Currently in-use")
            exit(-1)
        else:
            self.__safeExecution(
                f"CREATE TABLE {tableName} ({tempStr});", "Creating Table")

    def getTables(self):
        self.__safeExecution("SHOW TABLES;", "Getting Tables")
        return self.cursor.fetchall()

    def deleteTable(self, tableName):
        self.__safeExecution(f"DROP TABLE {tableName}", "Deleting Table")

    def addTableColumn(self, tableName, command):
        tempStr = ""
        if(isinstance(command, set) or isinstance(command, list)):
            for data in command:
                tempStr += data + ','
            tempStr = tempStr[:-1]
        else:
            tempStr = command
        if self.currentDatabase == "":
            print("No Database Currently in-use")
            exit(-1)
        else:
            self.__safeExecution(
                f"ALTER TABLE {tableName} ADD {command};", "Adding Table Column")

    def deleteTableColumn(self, tableName, columnName):
        self.__safeExecution(
            f"ALTER TABLE {tableName} DROP COLUMN {columnName};", "Deleting a Table")

    ########## Selecting ##########

    # Returns a list of tuples

    def getTableData(self, tableName):
        self.__safeExecution(
            f"SELECT * FROM {tableName}", "Getting Table Data")
        return self.cursor.fetchall()

    def getTableData(self, tableName, columnName, value, operator="="):
        self.__safeExecution(
            f"SELECT * FROM {tableName} WHERE {columnName} {operator} {value}", "Getting Table Data")
        return self.cursor.fetchall()

    ########## Other Methods ##########

    def getCurrentUser(self):
        """Return a List of Tuples"""
        self.__safeExecution(f"SELECT CURRENT_USER();", "Getting Current User")
        return self.cursor.fetchall()

    def getCurrentDatabaseName(self):
        return self.currentDatabase

    def exportToCSV(self, tableName, fileName):
        self.__safeExecution(f"SELECT * FROM {tableName} INTO OUTFILE '{fileName}.csv' FIELDS TERMINATED BY ','", "Exporting to CSV")
    
    ########## API ##########
    
    def exportToGoogleSheet(self, tableName):
        tableValue = self.__convertTuplesToList(self.getTableData(tableName));
        # API STUFF
        pass
    
    ########## Private Methods ##########

    def __convertTuplesToList(self, tupleValue):
        # Finish the Function
        pass

    def __convertToList(self, path):
        if (not exists(path)):
            raise Exception("[ ! ] File does not exist")

        if (not path.endswith(".txt")):
            raise Exception("[ ! ] Specified path is not a txt file.")

        file = open(path)
        csv = file.read()
        lines = csv.split('\n')
        rows = []

        for line in lines:
            items = line.split(',')
            rows.append(items)

        return rows

    def __safeExecution(self, command, typeOfCommand="Unknown"):
        try:
            self.cursor.execute(command)
        except:
            print(f"Problem: {typeOfCommand}")
            exit(-1)
