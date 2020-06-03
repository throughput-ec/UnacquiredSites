# README

## Input Data

The input data can be done either by a text file or by connecting a Postgresql server.

If the latter is used, the data will be loaded using the `config` and `database.ini` as initialization files.

`database.ini` holds all the credentials to log in to the postgresql server and should be included in the `.gitignore` file.  `database.ini` is located in the src directory.

To do your own `database.ini` file, just copy and paste the text bellow and change the credentials accordingly.

[postgresql]  
user = user  
password = pwd  
host = localhost  
port = 5432  
database = database


On the config.py file, you should also edit the route you are loading `database.ini` from.
