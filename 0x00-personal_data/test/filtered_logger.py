import logging
import re  # needed 2
from mysql.connector import connection 
from os import environ

def get_db() -> connection.MySQLConnection:
    """
    Connect to mysql server with environmental using environment variables.
    Returns a MySQLConnection object.
    """

    # Fetch the credentials from the environment variables, with defaults if not set
 
    username = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = environ.get("PERSONAL_DATA_DB_PASSWORD", "") # leave empty
    db_host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = environ.get("PERSONAL_DATA_DB_NAME", "holberton") # if local include: ,"holberton"
    connector = connection.MySQLConnection(
        user=username,
        password=password,
        host=db_host,
        database=db_name)
    return connector
