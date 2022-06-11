import mysql.connector
from API.GoogleSheet import *


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
        self.gSheetAPI = None;
    
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

    def getAllTableData(self, tableName):
        self.__safeExecution(f"SELECT * FROM {tableName}", "Getting Table Data")
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
    
    def initGoogleSheet(self, SCOPE, TOKEN_PATH):
        self.gSheetAPI = GoogleSheetAPI(SCOPE, TOKEN_PATH);
    
    def exportToGoogleSheet(self, tableName, RANGE_VALUE, SHEET_ID):
        tableValue = self.__tupleToListOfList(self.getAllTableData(tableName))
        values = [
            ["water", "melon"],
            ["asdfadsf", "aasdkfjsdfk"]
        ]
        
        # API STUFF
        self.gSheetAPI.updateSpreadsheetData(RANGE_VALUE,SHEET_ID, tableValue);
        pass
    
    ########## Private Methods ##########



    def __safeExecution(self, command, typeOfCommand="Unknown"):
        try:
            self.cursor.execute(command)
        except:
            print(f"Problem: {typeOfCommand}")
            exit(-1)
