# PySQL

An API for Python To MySQL with some addons.

## Supported API

- Google Sheet


## Getting Started

- Make sure you have MySQL Server running in your system, if not, download it here:

```
https://dev.mysql.com/downloads/windows/installer/8.0.html
```
> make sure that you remember your **USERNAME** and **PASSWORD**. You'll need it later

- Install MySQL Connector 

```python
pip install mysql-connector-python
```

- Install Google Modules (Optional)

```python
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### Using PySQL
- You can use this code to test if everything is working propertly

####  Without GoogleSheetAPI

```python
from PySQL import *

# changer the placeholder with your own values
pysql = PySQL("USERNAME", "PASSWORD")

pysql.createDatabase("TestDatabase00")
pysql.useDatabase("TestDatabase00")
pysql.createTable("TestTable00",["SOME_ID int PRIMARY KEY", "SOME_DATA VARCHAR(255)"])

# Print all the table inside the current database
print(pysql.getTables());  
```

####  With GoogleSheetAPI

```python
from PySql import *

# Read and Write Access
# You can refer here: https://developers.google.com/sheets/api/guides/authorizing
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The Name of the Sheet (not the file)
RANGE_VALUE = "Sheet1"

# You can see in your URL
# Example: https://docs.google.com/spreadsheets/d/SPREADSHEETID/edit#gid=0
SHEET_ID = "spreadsheetId"

# replace with placeholder
TOKEN_PATH = "token.json";

# changer the placeholder with your own values
pysql = PySql("USERNAME","PASSWORD")

# Initialize the Google Sheet
pysql.initGoogleSheet(SCOPES,TOKEN_PATH);

# Change the placeholder
pysql.useDatabase("DATABASE_NAME");

# Export the whole TABLE_NAME data in the google sheet
pysql.exportToGoogleSheet("TABLE_NAME", RANGE_VALUE,SHEET_ID)
    
```
